/**
 * Lingourmet Viewer Adapter
 * Normalizes curriculum-source build artifacts for the modular viewer.
 */

window.LessonAdapter = {
    /**
     * Resolves i18n fields from locale maps or nested `i18n` blocks.
     * Priority: locale key > common locale aliases > translation/text > first string.
     */
    resolveText(obj, locale = 'zh_tw', fallback = '') {
        if (!obj) return fallback;
        if (typeof obj === 'string') return obj;
        if (Array.isArray(obj)) return obj;

        const source = obj.i18n && typeof obj.i18n === 'object' ? obj.i18n : obj;

        // Try direct locale, then common variants
        const keys = [locale, 'zh-TW', 'zh_tw', 'zh_TW', 'zh-tw', 'zh-Hant'];
        for (const k of keys) {
            if (source[k]) return source[k];
        }

        // Try direct translation field set by enrichment
        if (typeof source.translation === 'string') return source.translation;
        if (typeof source.text === 'string') return source.text;

        // Fallback to first non-empty string value
        const first = Object.values(source).find(v => typeof v === 'string' && v);
        return first || fallback;
    },

    /**
     * Resolves and normalizes array fields.
     */
    resolveArray(arr) {
        if (!arr) return [];
        if (Array.isArray(arr)) return arr;
        return [arr];
    },

    /**
     * Normalizes the unit metadata.
     */
    normalizeUnit(unit, locale = 'zh_tw') {
        if (!unit) return {};

        return {
            ...unit,
            displayTitle: this.resolveText(unit.title_i18n, locale, unit.unit_id || ''),
            displayTheme: this.resolveText(unit.theme_i18n, locale, ''),
            displayCanDo: this.resolveArray(unit.can_do_i18n).map(v => this.resolveText(v, locale)).filter(Boolean)
        };
    },

    /**
     * Normalizes a single node.
     */
    normalizeNode(node, locale = 'zh_tw') {
        if (!node) return {};

        const payload = node.payload || {};
        const normalized = {
            ...node,
            displayTitle: this.resolveText(node.title_i18n, locale, this.getFallbackNodeTitle(node)),
            displaySummary: this.resolveText(node.summary_i18n, locale, '先看這一節的內容。'),
            displayExpected: this.resolveText(node.expected_output_i18n, locale, '先理解這一節的重點。'),
            payload: payload || {}
        };

        // Ensure content_form is present
        if (!normalized.content_form && normalized.id) {
            // Some legacy nodes might lack content_form but have hints in ID or role
            normalized.content_form = this.inferContentForm(normalized);
        }

        // 1. Resolve Examples (Precedence: refs > bank)
        normalized.payload.resolved_examples = this.resolveExamples(normalized.payload);

        // 2. Pattern Lab Normalization
        if (normalized.content_form === 'pattern_lab') {
            normalized.payload.pattern_builder_demos = this.resolveArray(payload.pattern_builder_demos || payload.pattern_builder_demo);
            normalized.payload.slot_bank_panels = this.resolveArray(payload.slot_bank_panels);
        }

        // 3. Vocab Normalization
        if (normalized.content_form === 'vocab_summary' || normalized.content_form === 'vocab_note') {
            normalized.payload.items = this.resolveArray(payload.items || payload.vocab_items || []);
        }

        // 4. Subtitle Normalization (Dialogue/Video)
        if (normalized.content_form === 'dialogue' || normalized.content_form === 'video') {
            normalized.payload.normalized_segments = this.normalizeSubtitleSegments(normalized.payload, locale);
        }

        return normalized;
    },

    /**
     * Normalizes dialogue or video payload into a unified subtitle segment model.
     * @param {Object} payload 
     * @param {string} locale 
     * @returns {Object} { surface_type, segments: [...] }
     */
    normalizeSubtitleSegments(payload, locale = 'zh_tw') {
        if (!payload) return { surface_type: 'unknown', segments: [] };

        const segments = [];
        let surfaceType = 'dialogue';

        // 1. Handle V5 Video (nodes and turns) or V1/V4 Video (directly has turns or nodes)
        const turns = (payload.nodes?.Start?.turns) || (payload.turns);
        if (turns && Array.isArray(turns)) {
            surfaceType = 'video';
            turns.forEach((turn, idx) => {
                const koText = typeof turn.text === 'object' ? turn.text.ko : (turn.text || '');
                // Resolve translation: check translations_i18n has actual keys, then fallback to direct field
                const hasI18n = turn.translations_i18n && Object.keys(turn.translations_i18n).length > 0;
                const resolvedTrans = hasI18n
                    ? this.resolveText(turn.translations_i18n, locale, turn.translation || '')
                    : (turn.translation || '');
                segments.push({
                    segment_id: turn.id || `v-${idx}`,
                    speaker: turn.speaker || '',
                    ko: koText,
                    translation: resolvedTrans,
                    start_ms: turn.time?.start ?? 0,
                    end_ms: turn.time?.end ?? 0,
                    anchor_refs: turn.anchor_refs || [],
                    atoms: turn.atoms || [], 
                    alignment_failed: turn.alignment_failed || false,
                    source_meta: { source_type: 'video' }
                });
            });
        }
        // 2. Handle Dialogue V5 (dialogue_scenes)
        else if (payload.dialogue_scenes && Array.isArray(payload.dialogue_scenes)) {
            payload.dialogue_scenes.forEach(scene => {
                const turns = scene.turns || [];
                turns.forEach((turn, idx) => {
                    segments.push({
                        segment_id: turn.id || `scene-${scene.id || '0'}-turn-${idx}`,
                        speaker: turn.speaker || '',
                        ko: turn.text || turn.ko || '',
                        translation: this.resolveText(turn.translations_i18n, locale, turn.translation || ''),
                        anchor_refs: turn.anchor_refs || [],
                        register: turn.register || '',
                        atoms: turn.atoms || [],
                        source_meta: {
                            scene_id: scene.id,
                            scene_title: this.resolveText(scene.title_i18n, locale, ''),
                            source_type: 'dialogue'
                        }
                    });
                });
            }); 
        } 
        // 3. Handle Legacy Dialogue (dialogue_turns)
        else if (payload.dialogue_turns && Array.isArray(payload.dialogue_turns)) {
            payload.dialogue_turns.forEach((turn, idx) => {
                    segments.push({
                        segment_id: turn.id || `turn-${idx}`,
                        speaker: turn.speaker || '',
                        ko: turn.text || turn.ko || '',
                        translation: this.resolveText(turn.translations_i18n, locale, turn.translation || ''),
                        anchor_refs: turn.anchor_refs || [],
                        register: turn.register || '',
                        atoms: turn.atoms || [],
                        source_meta: {
                        source_type: 'dialogue'
                    }
                });
            });
        }
        // 4. Handle Real Core Dialogue (content array)
        else if (payload.content && Array.isArray(payload.content)) {
            payload.content.forEach((turn, idx) => {
                    segments.push({
                        segment_id: turn.id || `turn-${idx}`,
                        speaker: turn.role || turn.speaker || '',
                        ko: turn.text || turn.ko || '',
                        translation: this.resolveText(turn.translations_i18n, locale, turn.translation || ''),
                        anchor_refs: turn.anchor_refs || [],
                        atoms: turn.atoms || [],
                        source_meta: {
                        source_type: 'dialogue'
                    }
                });
            });
        }

        return {
            surface_type: surfaceType,
            segments: segments
        };
    },

    /**
     * Resolves examples from various sources.
     * Precedence: 
     * 1. example_sentence_refs (Global Bank)
     * 2. example_bank (Local Transitional)
     */
    resolveExamples(payload) {
        if (!payload) return [];

        // Try canonical refs first
        const refs = payload.example_sentence_refs || [];
        if (Array.isArray(refs) && refs.length > 0) {
            // In the modular mockup, APP.libSentences holds the global bank
            const bank = window.APP?.libSentences || {};
            const resolved = refs.map(refId => {
                const s = bank[refId];
                if (s) {
                    return {
                        id: refId,
                        ko: s.source?.ko || s.source?.surface_ko || s.ko || "",
                        translation: s.i18n?.translation || s.translation || "(尚無翻譯)",
                        is_canonical: true
                    };
                }
                return null;
            }).filter(Boolean);

            if (resolved.length > 0) return resolved;
        }

        // Fallback to transitional bank
        const bank = payload.example_bank || [];
        if (Array.isArray(bank) && bank.length > 0) {
            return bank.map(ex => ({
                id: ex.id || "transitional",
                ko: ex.ko || "",
                translation: ex.translation || "(尚無翻譯)",
                is_canonical: false
            }));
        }

        return [];
    },

    /**
     * Fallback title logic moved from renderers.js
     */
    getFallbackNodeTitle(node) {
        const id = node.id || '';
        const match = id.match(/-(L1|L2|L3|G1|G2|P1|P2|P5|R1)$/);
        const stage = match ? match[1] : '';

        const role = node.learning_role || '';
        const roleMap = {
            immersion_input: '沉浸輸入',
            structure_pattern: '句型結構',
            structure_grammar: '文法解說',
            explicit_rule: '規則整理',
            controlled_output: '可控輸出',
            immersion_output: '任務輸出',
            review_retrieval: '複習回想'
        };
        const roleName = roleMap[role] || '學習節點';

        return stage ? `${stage} ${roleName}` : roleName;
    },

    /**
     * Infers content form for legacy or incomplete data.
     */
    inferContentForm(node) {
        if (node.content_form) return node.content_form;
        const id = node.id || '';
        const payload = node.payload || {};
        if (payload.dialogue_turns || payload.dialogue_scenes || payload.content) return 'dialogue';
        if (payload.turns || (payload.nodes?.Start?.turns) || id.includes('video')) return 'video';
        if (payload.pattern_builder_demos || payload.pattern_builder_demo) return 'pattern_lab';
        if (payload.items && (id.includes('-V') || id.includes('-D') || node.content_form === 'functional_phrase_pack')) return 'vocab_summary';
        if (node.learning_role === 'structure_grammar') return 'grammar_summary';
        if (node.learning_role === 'structure_usage' || id.includes('-U')) return 'usage';
        return 'unknown';
    }
};

// Global helper for quick access
window.i18nText = window.LessonAdapter.resolveText;
window.currentTeachingLocale = () => window.state?.progress?.prefs?.teachingLocale || 'zh_tw';
