# S1: Ingestion (`content-ko`)

## Goal
Normalize upstream source materials into canonical language source data.

## Main Work
1. Import raw lesson source.
2. Normalize structure into canonical content layout.
3. Prepare source for segmentation/mapping.

## Tools
- `content-ko/scripts/import_lllo_raw.py` (primary ingestion script)

## Exit Gate
- Canonical source files are generated and ready for stage S2.
