
# Lingo Release Aggregator Makefile
# -------------------------------

PYTHON = python
SCRIPTS = scripts

.PHONY: help gsd sync-tasks ingest-ko check check-tlg check-tlg-unit gen-tlg-unit

help:
	@echo "Available commands:"
	@echo "  make gsd          - Run the GSD protocol shim"
	@echo "  make sync-tasks   - Sync task JSONs with TASK_INDEX.md"
	@echo "  make ingest-ko    - Unified ingestion for Korean (pull lllo -> ingest -> pipeline)"
	@echo "  make check        - Run dictionary and content quality gates"
	@echo "  make check-tlg    - Run TLG pattern library gate (TLG-004/TLG-006)"
	@echo "  make gen-tlg-unit - Generate unit_blueprint_v1 draft from TLG-005 input"
	@echo "  make check-tlg-unit - Validate unit_blueprint_v1 draft with TLG-006 rules"

gsd:
	$(PYTHON) $(SCRIPTS)/gsd_shim.py

sync-tasks:
	$(PYTHON) $(SCRIPTS)/sync_task_index.py

ingest-ko:
	$(PYTHON) $(SCRIPTS)/ingest_ko.py

check:
	$(PYTHON) $(SCRIPTS)/check_quality.py

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
