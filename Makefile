
# Lingo Release Aggregator Makefile
# -------------------------------

PYTHON = python
SCRIPTS = scripts

.PHONY: help gsd sync-tasks ingest-ko check check-tlg

help:
	@echo "Available commands:"
	@echo "  make gsd          - Run the GSD protocol shim"
	@echo "  make sync-tasks   - Sync task JSONs with TASK_INDEX.md"
	@echo "  make ingest-ko    - Unified ingestion for Korean (pull lllo -> ingest -> pipeline)"
	@echo "  make check        - Run dictionary and content quality gates"
	@echo "  make check-tlg    - Run TLG pattern library gate (TLG-004/TLG-006)"

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
