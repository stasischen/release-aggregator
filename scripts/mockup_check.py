#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, List, Dict, Optional

# Constants for validation
MIN_NODE_COUNT = 10
INPUT_ROLES = {"immersion_input", "structure_pattern", "structure_grammar"}
OUTPUT_ROLES = {"controlled_output", "immersion_output", "review_retrieval"}

MIXED_PATTERNS = [
    (re.compile(r"7時"), "Found Chinese 時 in Korean string; likely should be '7시'."),
    (re.compile(r"二\s*잔"), "Found Chinese 二 in Korean quantity; likely should be '두 잔'."),
    (re.compile(r"하端"), "Found Chinese 端 in Korean word; likely should be '하단'."),
    (re.compile(r"外部\s*음식"), "Found Chinese 外部 mixed into Korean phrase; likely should be '외부 음식'."),
]

# Supported values based on unit_blueprint_v0 schema and UNITFAC upgrades
SUPPORTED_LEARNING_ROLES = {
    "immersion_input", "structure_pattern", "structure_grammar",
    "controlled_output", "immersion_output", "review_retrieval",
    "cross_unit_transfer"
}

SUPPORTED_OUTPUT_MODES = {
    "none", "chunk_assembly", "frame_fill", "response_builder",
    "pattern_transform", "guided", "guided_typing", "guided_speaking",
    "open_task", "retell", "transform", "review_retrieval"
}

SUPPORTED_INTERACTION_MODES = {
    "response_builder", "guided_typing", "guided_speaking",
    "chunk_assembly", "frame_fill", "pattern_transform"
}

SUPPORTED_CARD_POLICY_TYPES = {
    "recognition", "recall", "response"
}

SUPPORTED_SPACING_INTENSITY = {
    "high", "medium", "low"
}

SUPPORTED_SPACING_PROFILES = {
    "same_day_plus_1_plus_3", "long_term_retention"
}

SUPPORTED_CUE_SOURCES = {
    "carrier_context", "sentence_surface", "grammar_rule", "pattern_frame"
}

SUPPORTED_PASS_POLICIES = {
    "manual_mark_after_required_modes"
}

SUPPORTED_SENTENCE_ACTIONS = {
    "listen", "repeat", "shadow", "type"
}

# Anchor Support (CMOD-011)
SUPPORTED_ANCHOR_LEVELS = {"token", "chunk", "sentence"}
SUPPORTED_LINK_TARGETS = {"dictionary_atom_ref", "topic_ref", "grammar_ref"}
DICT_ATOM_REGEX = re.compile(r"^[a-z]{2,3}:[a-z0-9\-]+:.+$")


SUPPORTED_CONTENT_FORMS = {
    "dialogue", "notice", "message_thread", "comparison_card",
    "pattern_card", "grammar_note", "functional_phrase_pack",
    "practice_card", "roleplay_prompt", "message_prompt",
    "review_card", "comprehension_check", "article", "video_transcript"
}

class MockupChecker:
    def __init__(self, schema_path: Optional[Path] = None):
        self.errors = []
        self.warnings = []
        self.schema = None
        if schema_path and schema_path.exists():
            try:
                with open(schema_path, "r", encoding="utf-8") as f:
                    self.schema = json.load(f)
            except Exception as e:
                self.errors.append(f"Failed to load schema: {e}")

    def log_error(self, msg: str, node_id: str = None, path: str = None):
        prefix = f"[{node_id}]" if node_id else ""
        suffix = f" (at {path})" if path else ""
        self.errors.append(f"{prefix} ERROR: {msg}{suffix}")

    def log_warning(self, msg: str, node_id: str = None, path: str = None):
        prefix = f"[{node_id}]" if node_id else ""
        suffix = f" (at {path})" if path else ""
        self.warnings.append(f"{prefix} WARN: {msg}{suffix}")

    def iter_strings(self, obj: Any, path: str = "$"):
        if isinstance(obj, dict):
            for k, v in obj.items():
                yield from self.iter_strings(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                yield from self.iter_strings(v, f"{path}[{i}]")
        elif isinstance(obj, str):
            yield path, obj

    def check_fixture(self, fixture_path: Path):
        self.errors = []
        self.warnings = []
        
        try:
            with open(fixture_path, "r", encoding="utf-8") as f:
                fixture = json.load(f)
        except Exception as e:
            self.log_error(f"Failed to parse JSON: {e}")
            return False

        unit_version = fixture.get("version", "unit_blueprint_v0")
        is_v0_1 = unit_version == "unit_blueprint_v0.1"

        # A. Basic Shape
        if unit_version not in ["unit_blueprint_v0", "unit_blueprint_v0.1"]:
            self.log_error("fixture.version must be 'unit_blueprint_v0' or 'unit_blueprint_v0.1'")
        
        sequence = fixture.get("sequence", [])
        if not isinstance(sequence, list):
            self.log_error("fixture.sequence must be an array")
            return False

        # B. Data Hygiene & Mixed Script
        for s_path, value in self.iter_strings(fixture):
            for pattern, msg in MIXED_PATTERNS:
                if pattern.search(value):
                    self.log_error(f"{msg} Value={value!r}", path=s_path)
            
            # ERR_MISSING_ZH_TW (Basic check for empty strings in TW fields)
            if "_zh_tw" in s_path.lower() or s_path.endswith(".zh_tw"):
                if not value or value.strip() == "" or "TODO" in value:
                     self.log_warning(f"Field seems empty or contains TODO: {value!r}", path=s_path)

        # C. Sequence Rules (UNITFAC-002 & PEDOPT-009)

        if len(sequence) < MIN_NODE_COUNT:
            self.log_error(f"ERR_MIN_NODE_COUNT: Unit has {len(sequence)} nodes, minimum {MIN_NODE_COUNT} required for PR.")

        found_input = False
        found_output = False
        first_input_idx = -1
        found_comp_check = False
        cc_types = []

        # 0. Global Modular V1 Detection
        def deep_has_contract(n):
            if "interaction_contract" in n: return True
            p = n.get("payload", {})
            if not isinstance(p, dict): return False
            # Check dialogue turns
            turns = p.get("dialogue_turns") or p.get("turns") or []
            if any("interaction_contract" in t for t in turns if isinstance(t, dict)): return True
            
            # Check dialogue scenes
            scenes = p.get("dialogue_scenes") or []
            for scene in scenes:
                if not isinstance(scene, dict): continue
                s_turns = scene.get("turns") or []
                if any("interaction_contract" in t for t in s_turns if isinstance(t, dict)): return True

            # Check article paragraphs -> sentences
            paragraphs = p.get("paragraphs", [])
            for pg in paragraphs:
                if not isinstance(pg, dict): continue
                sentences = pg.get("sentences", [])
                if any("interaction_contract" in s for s in sentences if isinstance(s, dict)): return True
            # Check video lines
            lines = p.get("lines", [])
            if any("interaction_contract" in l for l in lines if isinstance(l, dict)): return True
            return False

        has_modular_marker = any(
            "interaction_modes" in n or 
            "review_policy" in n or 
            "completion_rules" in n or 
            deep_has_contract(n) 
            for n in sequence
        ) or "review_policy" in fixture
        is_modular_v1 = fixture.get("version", "") >= "unit_blueprint_v0.1" and has_modular_marker

        for i, node in enumerate(sequence):
            node_id = node.get("id", f"node_{i}")
            role = node.get("learning_role")
            form = node.get("content_form")
            mode = node.get("output_mode")
            payload = node.get("payload") or {}

            # 0. Presence check for required fields
            if mode is None:
                self.log_error("MISSING_FIELD: output_mode is required", node_id=node_id)
                # We do not coerce to 'none' here to allow schema-level error propagation
            skip_mode_checks = mode is None

            # 1. Contract checks
            if role not in SUPPORTED_LEARNING_ROLES:
                self.log_error(f"Unsupported learning_role: {role}", node_id=node_id)
            if form not in SUPPORTED_CONTENT_FORMS:
                self.log_error(f"Unsupported content_form: {form}", node_id=node_id)
            if mode not in SUPPORTED_OUTPUT_MODES:
                self.log_error(f"Unsupported output_mode: {mode}", node_id=node_id)

            # 2. Order Violation
            if role in INPUT_ROLES:
                found_input = True
                if first_input_idx == -1:
                    first_input_idx = i
            if role in OUTPUT_ROLES:
                found_output = True
                if not found_input:
                    self.log_error("ERR_ORDER_VIOLATION: Output node appeared before any input/structure node.", node_id=node_id)

            # 3. Pedagogy Metadata (PEDOPT-009)
            
            # Comprehension Check
            if form == "comprehension_check":
                found_comp_check = True
                q_type = payload.get("question_type")
                if not q_type:
                    self.log_warning("PED_MISSING_TYPE: comprehension_check missing 'question_type'", node_id=node_id)
                else:
                    cc_types.append(q_type)

            # Pattern Transform
            if not skip_mode_checks and mode == "pattern_transform":
                t_type = payload.get("transform_type")
                if not t_type:
                    self.log_warning("PED_MISSING_TYPE: transform node missing 'transform_type'", node_id=node_id)

            # Repair Practice
            if not skip_mode_checks and mode == "repair_practice":
                if not payload.get("trigger_type") or not payload.get("repair_goal"):
                    self.log_warning("PED_MISSING_TYPE: repair_practice missing 'trigger_type' or 'repair_goal'", node_id=node_id)

            # Review Retrieval
            if form == "review_card":
                if not payload.get("target_type"):
                    self.log_warning("PED_MISSING_TYPE: review_card missing 'target_type'", node_id=node_id)
                if not payload.get("retrieval_focus"):
                    self.log_warning("PED_MISSING_RETRIEVAL_FOCUS: review_card missing 'retrieval_focus'", node_id=node_id)

            # Listening Discrimination (Experimental)
            if form == "listening_discrimination_micro":
                if not payload.get("discrimination_target") or not payload.get("distractor_rationale"):
                    self.log_warning("PED_LISTENING_NO_RATIONALE: missing 'discrimination_target' or 'distractor_rationale'", node_id=node_id)

            # 4. Miscellaneous Payload Checks
            if "answers_ko" in payload:
                self.log_warning("Uses legacy payload.answers_ko; prefer reference_answers_ko", node_id=node_id)
            
            # 5. CMOD Modular Metadata Checks (Blockers/Errors)
            # Mandatory for v0.1+ that have opted into modularity, optional for legacy
            
            # 5.1 Interaction Modes & Dispatcher
            interaction_modes = node.get("interaction_modes")
            if is_modular_v1 and role in ["immersion_output", "controlled_output"] and interaction_modes is None:
                self.log_error("CMOD_MISSING_INTERACTION_MODES: Output/Drill nodes MUST declare capability list in v0.1+", node_id=node_id)
            
            if interaction_modes is not None:
                if not isinstance(interaction_modes, list):
                    self.log_error("CMOD_INVALID_SCHEMA: interaction_modes must be a list", node_id=node_id)
                else:
                    for m in interaction_modes:
                        if m not in SUPPORTED_INTERACTION_MODES:
                            self.log_error(f"CMOD_UNSUPPORTED_INTERACTION_MODE: {m}", node_id=node_id)
                    # Dispatcher-Capability membership check (CMOD-003 precedence rule)
                    if mode != "none" and mode not in interaction_modes:
                        self.log_error(f"CMOD_DISPATCH_MISMATCH: output_mode '{mode}' is not in interaction_modes capability list", node_id=node_id)

            # 5.2 Completion Rules
            comp_rules = node.get("completion_rules")
            if is_modular_v1 and role in ["immersion_output", "controlled_output"] and comp_rules is None:
                self.log_error("CMOD_MISSING_COMPLETION_RULES: Output/Drill nodes MUST declare completion gating in v0.1+", node_id=node_id)
            
            if comp_rules is not None:
                if not isinstance(comp_rules, dict):
                    self.log_error("CMOD_INVALID_SCHEMA: completion_rules must be an object", node_id=node_id)
                else:
                    # Validate required_modes subset
                    req_modes = comp_rules.get("required_modes", [])
                    if not isinstance(req_modes, list):
                        self.log_error("CMOD_INVALID_SCHEMA: completion_rules.required_modes must be a list", node_id=node_id)
                    else:
                        target_modes = interaction_modes if interaction_modes is not None else []
                        for rm in req_modes:
                            if rm not in target_modes:
                                self.log_error(f"CMOD_CRITICAL_MISMATCH: required_mode '{rm}' is not in interaction_modes", node_id=node_id)
                    
                    # Validate pass_policy
                    pass_policy = comp_rules.get("pass_policy")
                    if not pass_policy or pass_policy not in SUPPORTED_PASS_POLICIES:
                        self.log_error(f"CMOD_INVALID_PASS_POLICY: {pass_policy}", node_id=node_id)
                    
                    # Validate min_attempts (Type and Range)
                    if "min_attempts" in comp_rules:
                        min_att = comp_rules.get("min_attempts")
                        if not isinstance(min_att, int):
                            self.log_error("CMOD_INVALID_SCHEMA: min_attempts must be an integer", node_id=node_id)
                        elif min_att < 1:
                            self.log_error(f"CMOD_OUT_OF_RANGE: min_attempts must be >= 1 (found {min_att})", node_id=node_id)

            # 5.3 Review Policy
            policy = node.get("review_policy") or fixture.get("review_policy")
            if is_modular_v1 and (form == "review_card" or role == "review_retrieval") and policy is None:
                self.log_error("CMOD_MISSING_REVIEW_POLICY: Review nodes MUST declare retrieval strategy in v0.1+", node_id=node_id)
            
            if policy is not None:
                if not isinstance(policy, dict):
                    self.log_error("CMOD_INVALID_SCHEMA: review_policy must be an object", node_id=node_id)
                else:
                    # Validate policy_id (Required string)
                    if not policy.get("policy_id") or not isinstance(policy.get("policy_id"), str):
                        self.log_error("CMOD_MISSING_POLICY_ID: review_policy MUST have a string policy_id", node_id=node_id)

                    # Validate enabled (Required boolean)
                    if "enabled" not in policy or not isinstance(policy.get("enabled"), bool):
                        self.log_error("CMOD_INVALID_SCHEMA: review_policy.enabled must be a boolean", node_id=node_id)
                    
                    # Validate card_source (Required dict with inner fields)
                    card_svc = policy.get("card_source")
                    if not card_svc or not isinstance(card_svc, dict):
                        self.log_error("CMOD_MISSING_CARD_SOURCE: review_policy MUST have a card_source object", node_id=node_id)
                    else:
                        if "prefer_carrier" not in card_svc or not isinstance(card_svc.get("prefer_carrier"), bool):
                            self.log_error("CMOD_INVALID_SCHEMA: card_source.prefer_carrier must be a boolean", node_id=node_id)
                        if "include_support" not in card_svc or not isinstance(card_svc.get("include_support"), list):
                            self.log_error("CMOD_INVALID_SCHEMA: card_source.include_support must be a list", node_id=node_id)
                    
                    # Validate card_policies keys and entry shape
                    card_policies = policy.get("card_policies", {})
                    seen_priorities = set()
                    for p_type, p_val in card_policies.items():
                        if p_type not in SUPPORTED_CARD_POLICY_TYPES:
                            self.log_error(f"CMOD_UNSUPPORTED_CARD_POLICY: {p_type}", node_id=node_id)
                        else:
                            if not isinstance(p_val, dict):
                                self.log_error(f"CMOD_INVALID_SCHEMA: card_policies.{p_type} must be an object", node_id=node_id)
                            else:
                                if "priority" not in p_val or not isinstance(p_val.get("priority"), int):
                                    self.log_error(f"CMOD_MISSING_ENTRY_FIELD: card_policies.{p_type} MUST have an integer 'priority'", node_id=node_id)
                                if "cue_type" not in p_val or not isinstance(p_val.get("cue_type"), str):
                                    self.log_error(f"CMOD_MISSING_ENTRY_FIELD: card_policies.{p_type} MUST have a string 'cue_type'", node_id=node_id)
                                priority = p_val.get("priority")
                                if isinstance(priority, int):
                                    if priority in seen_priorities:
                                        self.log_error(f"CMOD_DUPLICATE_PRIORITY: duplicate card_policies priority {priority}", node_id=node_id)
                                    else:
                                        seen_priorities.add(priority)
                    
                    # Validate spacing_semantics
                    spacing = policy.get("spacing_semantics", {})
                    profile = spacing.get("profile")
                    if not profile or profile not in SUPPORTED_SPACING_PROFILES:
                        self.log_error(f"CMOD_INVALID_SPACING_PROFILE: {profile}", node_id=node_id)
                    
                    intensity = spacing.get("intensity")
                    if intensity and intensity not in SUPPORTED_SPACING_INTENSITY:
                        self.log_error(f"CMOD_UNSUPPORTED_INTENSITY: {intensity}", node_id=node_id)
                        
                    # Validate cue_source_preference (Strict list and element check)
                    csp = policy.get("cue_source_preference")
                    if "cue_source_preference" not in policy:
                        self.log_error("CMOD_MISSING_CUE_PREFERENCE: review_policy MUST define cue_source_preference", node_id=node_id)
                    elif not isinstance(csp, list) or len(csp) == 0:
                        self.log_error("CMOD_INVALID_SCHEMA: cue_source_preference MUST be a non-empty list", node_id=node_id)
                    else:
                        for source in csp:
                            if source not in SUPPORTED_CUE_SOURCES:
                                self.log_error(f"CMOD_UNSUPPORTED_CUE_SOURCE: {source}", node_id=node_id)

            # 5.4 Interaction Contract (CMOD-013)
            # This can appear in turns or lines within payload, or at node level
            def check_contract(contract, context_id, parent_text=None):
                if not isinstance(contract, dict):
                    self.log_error("CMOD_INVALID_SCHEMA: interaction_contract must be an object", node_id=context_id)
                    return
                
                actions = contract.get("actions", [])
                if not isinstance(actions, list):
                    self.log_error("CMOD_INVALID_SCHEMA: interaction_contract.actions must be a list", node_id=context_id)
                else:
                    for act in actions:
                        if act not in SUPPORTED_SENTENCE_ACTIONS:
                            self.log_error(f"CMOD_UNSUPPORTED_ACTION: {act}", node_id=context_id)
                
                c_payload = contract.get("payload", {})
                if not isinstance(c_payload, dict):
                    self.log_error("CMOD_INVALID_SCHEMA: interaction_contract.payload must be an object", node_id=context_id)
                else:
                    # Audio actions can be backed by a prebuilt audio asset or by inline TTS text.
                    if any(a in ["listen", "repeat", "shadow"] for a in actions):
                        has_audio_ref = bool(c_payload.get("audio_ref"))
                        has_tts_text = bool(c_payload.get("tts_text"))
                        if not has_audio_ref and not has_tts_text:
                            self.log_error("CMOD_MISSING_AUDIO_SOURCE: Action requires audio_ref or tts_text", node_id=context_id)
                        if "audio_ref" in c_payload and c_payload.get("audio_ref") is not None and not isinstance(c_payload.get("audio_ref"), str):
                            self.log_error("CMOD_INVALID_SCHEMA: audio_ref must be a string", node_id=context_id)
                        if "tts_text" in c_payload and c_payload.get("tts_text") is not None and not isinstance(c_payload.get("tts_text"), str):
                            self.log_error("CMOD_INVALID_SCHEMA: tts_text must be a string", node_id=context_id)
                    
                    # Require target_surface for type action
                    if "type" in actions and not c_payload.get("target_surface"):
                        self.log_error("CMOD_MISSING_TARGET_SURFACE: Action 'type' requires target_surface", node_id=context_id)

                dive = contract.get("knowledge_dive", {})
                if not isinstance(dive, dict):
                    self.log_error("CMOD_INVALID_SCHEMA: knowledge_dive must be an object", node_id=context_id)
                else:
                    # Legacy flat refs
                    for ref_key in ["dictionary_atom_refs", "grammar_refs"]:
                        refs = dive.get(ref_key, [])
                        if not isinstance(refs, list):
                            self.log_error(f"CMOD_INVALID_SCHEMA: {ref_key} must be a list", node_id=context_id)

                    # CMOD-011: Anchors
                    anchors = dive.get("anchors", [])
                    if not isinstance(anchors, list):
                        self.log_error("CMOD_INVALID_SCHEMA: knowledge_dive.anchors must be a list", node_id=context_id)
                    else:
                        seen_spans = set()
                        for idx, anchor in enumerate(anchors):
                            if not isinstance(anchor, dict):
                                self.log_error(f"CMOD_INVALID_SCHEMA: anchor[{idx}] must be an object", node_id=context_id)
                                continue
                            
                            # Required fields
                            for field in ["surface", "offset", "length", "level", "target", "ref"]:
                                if field not in anchor:
                                    self.log_error(f"CMOD_MISSING_ANCHOR_FIELD: anchor[{idx}] missing '{field}'", node_id=context_id)

                            surface = anchor.get("surface", "")
                            offset = anchor.get("offset")
                            length = anchor.get("length")
                            level = anchor.get("level")
                            target = anchor.get("target")
                            ref = anchor.get("ref", "")

                            # Level and Target validation
                            if level and level not in SUPPORTED_ANCHOR_LEVELS:
                                self.log_error(f"CMOD_UNSUPPORTED_ANCHOR_LEVEL: {level}", node_id=context_id)
                            if target and target not in SUPPORTED_LINK_TARGETS:
                                self.log_error(f"CMOD_UNSUPPORTED_LINK_TARGET: {target}", node_id=context_id)

                            # Ref format validation
                            if target == "dictionary_atom_ref":
                                if not DICT_ATOM_REGEX.match(ref):
                                    self.log_error(f"CMOD_INVALID_DICT_REF: {ref}", node_id=context_id)
                            elif target == "topic_ref" and not ref.startswith("topic:"):
                                self.log_error(f"CMOD_INVALID_TOPIC_REF: {ref}", node_id=context_id)
                            elif target == "grammar_ref" and not ref.startswith("grammar:"):
                                self.log_error(f"CMOD_INVALID_GRAMMAR_REF: {ref}", node_id=context_id)

                            # Boundary and Integrity check
                            if isinstance(offset, int) and isinstance(length, int):
                                # P1: Reject negative or zero anchor spans
                                if offset < 0:
                                    self.log_error(f"CMOD_ANCHOR_NEGATIVE_OFFSET: {surface} (offset {offset} < 0)", node_id=context_id)
                                if length <= 0:
                                    self.log_error(f"CMOD_ANCHOR_INVALID_LENGTH: {surface} (length {length} <= 0)", node_id=context_id)
                                
                                # P2: Duplicate suppression
                                # Hardening: Key on (offset, length, level) to allow multi-level overlap per CMOD-011
                                anchor_key = (offset, length, level)
                                if anchor_key in seen_spans:
                                    self.log_error(f"CMOD_DUPLICATE_ANCHOR: {surface} at offset {offset} (duplicate of previous {level} anchor)", node_id=context_id)
                                seen_spans.add(anchor_key)

                                if parent_text:
                                    if offset >= 0 and offset + length > len(parent_text):
                                        self.log_error(f"CMOD_ANCHOR_OUT_OF_BOUNDS: {surface} (offset {offset} + len {length} > parent len {len(parent_text)})", node_id=context_id)
                                    elif offset >= 0 and length > 0:
                                        actual_text = parent_text[offset:offset+length]
                                        if actual_text != surface:
                                            self.log_warning(f"CMOD_ANCHOR_TEXT_MISMATCH: Expected {surface!r}, found {actual_text!r} at offset {offset}", node_id=context_id)
                                elif not parent_text and offset + length > 0:
                                     self.log_warning("CMOD_ANCHOR_VAL_LIMIT: Cannot validate anchor boundaries without parent text", node_id=context_id)

            # Check top-level contract
            if "interaction_contract" in node:
                check_contract(node["interaction_contract"], node_id, node.get("text"))
            
            # Check nested contracts in payload (dialogue turns, video lines, etc)
            if form == "dialogue":
                turns = payload.get("dialogue_turns") or payload.get("turns") or []
                for j, turn in enumerate(turns):
                    if "interaction_contract" in turn:
                        check_contract(turn["interaction_contract"], f"{node_id}_T{j}", turn.get("text"))
                
                # Support scenes
                scenes = payload.get("dialogue_scenes") or []
                for s_idx, scene in enumerate(scenes):
                    if not isinstance(scene, dict): continue
                    s_turns = scene.get("turns") or []
                    for t_idx, turn in enumerate(s_turns):
                        if "interaction_contract" in turn:
                            check_contract(turn["interaction_contract"], f"{node_id}_S{s_idx}T{t_idx}", turn.get("text"))
            
            elif form == "article":
                paragraphs = payload.get("paragraphs") or payload.get("sections") or []
                for p_idx, paragraph in enumerate(paragraphs):
                    if not isinstance(paragraph, dict):
                        continue
                    sentences = paragraph.get("sentences") or paragraph.get("items") or []
                    for s_idx, sentence in enumerate(sentences):
                        if "interaction_contract" in sentence:
                            check_contract(sentence["interaction_contract"], f"{node_id}_P{p_idx}S{s_idx}", sentence.get("text"))

            elif form == "video_transcript": # Hypothetical future form
                lines = payload.get("lines") or []
                for j, line in enumerate(lines):
                    if "interaction_contract" in line:
                        check_contract(line["interaction_contract"], f"{node_id}_L{j}", line.get("text"))
            


        # 6. Global Sequence Validations
        if found_input and not found_comp_check:
            self.log_error("ERR_MISSING_COMPREHENSION: No comprehension_check found in the sequence.")
        
        if len(cc_types) > 1 and len(set(cc_types)) == 1:
            self.log_warning(f"PED_LOW_CC_DIVERSITY: All {len(cc_types)} CC nodes use the same type: {cc_types[0]}")

        # 6. Followup Validations
        for followup in fixture.get("scheduled_followups", []):
            f_id = followup.get("id", "followup")
            f_type = followup.get("followup_type")
            p_refs = followup.get("transfer_pattern_refs", [])
            
            if f_type == "transfer" and not p_refs:
                self.log_error("PED_FOLLOWUP_INCONSISTENT: followup_type is 'transfer' but 'transfer_pattern_refs' is empty.", node_id=f_id)
            
            if is_v0_1 and not f_type:
                self.log_warning("PED_MISSING_TYPE: followup missing 'followup_type' in v0.1 unit", node_id=f_id)

        return len(self.errors) == 0

def main():
    parser = argparse.ArgumentParser(description="Unified mockup check for unit fixtures.")
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    parser.add_argument("files", nargs="*", help="Fixture JSON files to validate.")
    parser.add_argument("--index", help="Path to fixtures index JSON (e.g. modular/data/fixtures.json)")
    parser.add_argument("--schema", help="Path to unit_blueprint_v0.schema.json")
    
    args = parser.parse_args()
    
    checker = MockupChecker(schema_path=Path(args.schema) if args.schema else None)
    
    files_to_check = [Path(f) for f in args.files]
    
    if args.index:
        idx_path = Path(args.index)
        if idx_path.exists():
            try:
                with open(idx_path, "r", encoding="utf-8") as f:
                    idx_data = json.load(f)
                    for unit in idx_data.get("units", []):
                        rel_path = unit.get("path")
                        if rel_path:
                            # Try relative to index file first
                            candidate = (idx_path.parent / rel_path).resolve()
                            if not candidate.exists():
                                # Heuristic: if index is in a 'data' folder, try one level up (viewer relative)
                                candidate = (idx_path.parent.parent / rel_path).resolve()
                            files_to_check.append(candidate)
            except Exception as e:
                print(f"ERROR: Failed to read index {args.index}: {e}")
                sys.exit(2)

    if not files_to_check:
        print("No files to check. Provide files as arguments or use --index.")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0
    failed_files = 0

    print(f"Running mockup-check on {len(files_to_check)} files...\n")

    for f_path in files_to_check:
        if not f_path.exists():
            print(f"FAILED: File not found: {f_path}")
            failed_files += 1
            continue
        
        print(f"Checking {f_path.name}...")
        is_ok = checker.check_fixture(f_path)
        
        if checker.errors:
            for err in checker.errors:
                print(f"  {err}")
        if checker.warnings:
            for warn in checker.warnings:
                print(f"  {warn}")
        
        total_errors += len(checker.errors)
        total_warnings += len(checker.warnings)
        
        if not is_ok:
            failed_files += 1
            print(f"RESULT: {f_path.name} FAILED ({len(checker.errors)} errors, {len(checker.warnings)} warnings)\n")
        else:
            print(f"RESULT: {f_path.name} PASSED ({len(checker.warnings)} warnings)\n")

    print(f"Summary: {len(files_to_check)} files checked, {failed_files} failed.")
    print(f"Total Blocker Errors: {total_errors}")
    print(f"Total Warnings: {total_warnings}")

    if failed_files > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
