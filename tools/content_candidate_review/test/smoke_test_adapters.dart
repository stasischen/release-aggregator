import 'dart:convert';
import 'dart:io';
import '../lib/models/candidate_review_item.dart';
import '../lib/utils/export_adapters.dart';

void main() {
  print('--- Adapter Smoke Test ---');

  // 1. Mock Input Data (Review Results)
  final mockJson = [
    {
      "candidate_id": "CAND-001",
      "batch_id": "BATCH-2026-02-24",
      "candidate_type": "lesson",
      "target_level": "A1",
      "target_unit_id": "U04",
      "target_position": 1,
      "title_zh_tw": "在咖啡廳點餐",
      "subtitle_zh_tw": "學習如何用韓文點拿鐵和甜點",
      "can_do_zh_tw": ["能聽懂店員詢問內用或外帶", "能表達點餐需求並完成支付"],
      "review_summary_zh_tw": "這是一個標準的咖啡廳對話，適合 A1 初級學習者。",
      "novelty_rationale_zh_tw": "加入了當前韓國受歡迎的「冰美式」文化元素。",
      "risk_flags_zh_tw": [],
      "agent_recommendation": "accept",
      "scores": {"fit": 0.9, "novelty": 0.7, "learnability": 0.8},
      "foreign_preview": {
        "lines": ["어떤 걸로 드릴까요?"],
      },
      "human_decision": "accept",
      "human_notes_zh_tw": "內容紮實，符合 A1 難度。",
      "updated_at": "2026-02-25T10:00:00Z",
    },
    {
      "candidate_id": "CAND-002",
      "batch_id": "BATCH-2026-02-24",
      "candidate_type": "grammar_note",
      "target_level": "A1",
      "target_unit_id": "U04",
      "target_position": 2,
      "title_zh_tw": "-주세요 (請給我...)",
      "subtitle_zh_tw": "請求與命令的禮貌表達",
      "can_do_zh_tw": ["能使用 -주세요 進行禮貌請求"],
      "review_summary_zh_tw": "結合咖啡廳場景的用法解釋。",
      "novelty_rationale_zh_tw": "範例直接引用 U04 對話。",
      "risk_flags_zh_tw": [],
      "agent_recommendation": "accept",
      "scores": {"fit": 0.95, "novelty": 0.5},
      "foreign_preview": {"explanation": "'-주세요' ..."},
      "human_decision": "accept",
      "human_notes_zh_tw": "非常實用。",
      "updated_at": "2026-02-25T10:05:00Z",
    },
  ];

  final items = mockJson.map((j) => CandidateReviewItem.fromJson(j)).toList();

  // 2. Test Catalog Draft Export
  print('\n[Output: catalog_draft.json]');
  final catalogDraft = ExportAdapters.toCatalogDraft(items);
  print(catalogDraft);

  // 3. Test Backlog Seed Export
  print('\n[Output: backlog_seed.json]');
  final backlogSeed = ExportAdapters.toBacklogSeed(items);
  print(backlogSeed);

  print('\n--- Smoke Test Completed ---');
}
