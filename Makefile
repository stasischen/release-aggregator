
# Lingo Release Aggregator Makefile
# -------------------------------

PYTHON = python
SCRIPTS = scripts

.PHONY: help gsd sync-tasks ingest-ko check test-prg check-tlg check-tlg-unit gen-tlg-unit check-tlg-unit-llm emit-gemini-prompts run-gemini-unit-demo

help:
	@echo "Available commands:"
	@echo "  make gsd          - Run the GSD protocol shim"
	@echo "  make sync-tasks   - Sync task JSONs with TASK_INDEX.md"
	@echo "  make ingest-ko    - Unified ingestion for Korean (pull lllo -> ingest -> pipeline)"
	@echo "  make check        - Run dictionary and content quality gates"
	@echo "  make test-prg     - Run PRG contract and provenance tests"
	@echo "  make check-tlg    - Run TLG pattern library gate (TLG-004/TLG-006)"
	@echo "  make gen-tlg-unit - Generate unit_blueprint_v1 draft from TLG-005 input"
	@echo "  make check-tlg-unit - Validate unit_blueprint_v1 draft with TLG-006 rules"
	@echo "  make check-tlg-unit-llm - Validate LLM reasonability review report"
	@echo "  make emit-gemini-prompts - Render Gemini prompt pack for a unit"
	@echo "  make run-gemini-unit-demo - Run one-unit Gemini demo pipeline"

gsd:
	$(PYTHON) $(SCRIPTS)/gsd_shim.py

sync-tasks:
	$(PYTHON) $(SCRIPTS)/sync_task_index.py

ingest-ko:
	$(PYTHON) $(SCRIPTS)/ingest_ko.py

check:
	$(PYTHON) $(SCRIPTS)/check_quality.py

test-prg:
	$(PYTHON) -m unittest discover -s tests -p "test_prg*.py" -v

check-tlg:
	$(PYTHON) $(SCRIPTS)/tlg006_pattern_gate.py \
		--library docs/tasks/pattern_library/ko_survival_pattern_library_v1.json \
		--repair-registry docs/tasks/pattern_library/ko_repair_strategy_registry_v1.json

gen-tlg-unit:
	$(PYTHON) $(SCRIPTS)/tlg005_generate_unit_v1.py \
		--input staging/tlg005_input.sample.json \
		--pattern-library docs/tasks/pattern_library/ko_survival_pattern_library_v1.json \
		--output staging/unit_blueprint_v1.generated.json

check-tlg-unit:
	$(PYTHON) $(SCRIPTS)/tlg006_validate_unit_v1.py \
		--blueprint staging/unit_blueprint_v1.generated.json \
		--repair-registry docs/tasks/pattern_library/ko_repair_strategy_registry_v1.json

check-tlg-unit-llm:
	$(PYTHON) $(SCRIPTS)/tlg006_llm_review_gate.py \
		--blueprint staging/unit_blueprint_v1.generated.json \
		--report staging/unit_blueprint_v1.llm_review_report.json

emit-gemini-prompts:
	$(PYTHON) $(SCRIPTS)/tlg_gemini_emit_prompts.py \
		--unit-input staging/tlg005_input.a1_u01.json \
		--blueprint staging/demo_A1-U01.unit_blueprint_v1.json \
		--outdir staging/gemini_prompts/A1-U01

run-gemini-unit-demo:
	$(PYTHON) $(SCRIPTS)/tlg_gemini_run_unit_demo.py \
		--seed-input staging/tlg005_input.a1_u01.json \
		--theme-zh-tw "校園報到與初次見面（Gemini Demo）" \
		--scenario "new_student_orientation" \
		--primary-outcome "完成報到、認識同學、找到教室" \
		--model gemini-2.5-pro
