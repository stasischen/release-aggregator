# Batch Process Remaining Video Pilot Content (V5 Gate)

This plan outlines the batch processing of 4 pilot videos using the `qa_v5_gate.py` script to migrate them to the V5 morphological standard.

## Proposed Changes

### [content-ko](file:///d:/Githubs/lingo/content-ko)

#### [MODIFY] [content/core/video_atoms/](file:///d:/Githubs/lingo/content-ko/content/core/video_atoms/)
- New V5 atomized files will be promoted here upon success.

#### [NEW] [artifacts/v5_scratch/](file:///d:/Githubs/lingo/content-ko/artifacts/v5_scratch/)
- Audit logs and registry coverage tables for each video.

## Target Videos
1. `79Pwq7MTUPE`
2. `9lOJxJBRj1I`
3. `IGEj-oDKyw8`
4. `paToZla2CK8`

## Execution Plan

For each video ID in the target list:

1. **Dry-Run Validation**:
   ```powershell
   python scripts/ops/qa_v5_gate.py --video <video_id> --dry-run
   ```
2. **Actual Promotion**:
   ```powershell
   python scripts/ops/qa_v5_gate.py --video <video_id>
   ```

## Verification Plan

### Automated Tests
- The `qa_v5_gate.py` script itself performs round-trip validation and content hashing.

### Manual Verification
- Review the `activation_log.json` for each video.
