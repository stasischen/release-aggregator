import 'dart:convert';
import '../models/candidate_review_item.dart';

class ExportAdapters {
  /// Converts accepted candidates to a catalog draft format.
  static String toCatalogDraft(List<CandidateReviewItem> items) {
    final acceptedItems = items
        .where((it) => it.humanDecision == HumanDecision.accept)
        .toList();

    final draft = acceptedItems.map((it) {
      return {
        'id': it.candidateId,
        'type': it.candidateType.toLowerCase(),
        'level': it.targetLevel,
        'unit_id': it.targetUnitId,
        'position': it.targetPosition,
        'title': it.titleZhTw,
        'subtitle': it.subtitleZhTw,
        'can_do': it.canDoZhTw,
        'summary': it.reviewSummaryZhTw,
        'rationale': it.noveltyRationaleZhTw,
        'meta': {
          'scores': it.scores,
          'risk_flags': it.riskFlagsZhTw,
          'agent_recommendation': it.agentRecommendation,
          'human_notes': it.humanNotesZhTw,
          'batch_id': it.batchId,
          'updated_at': it.updatedAt.toIso8601String(),
        },
      };
    }).toList();

    return const JsonEncoder.withIndent('  ').convert(draft);
  }

  /// Converts accepted candidates to a backlog seed format.
  static String toBacklogSeed(List<CandidateReviewItem> items) {
    final acceptedItems = items
        .where((it) => it.humanDecision == HumanDecision.accept)
        .toList();

    final seeds = acceptedItems.map((it) {
      final type = it.candidateType.toLowerCase();
      List<String> suggestedTasks = [];

      if (type.contains('lesson') || type.contains('dialogue')) {
        suggestedTasks = [
          'Generate dialogue/monologue content',
          'Create audio recording tasks',
          'Define comprehension checks',
          'Map vocabulary to dictionary',
        ];
      } else if (type.contains('grammar')) {
        suggestedTasks = [
          'Draft grammar explanation (zh-TW)',
          'Create example sentences with audio',
          'Sync with related lessons',
          'Verify pattern usage',
        ];
      } else if (type.contains('dict')) {
        suggestedTasks = [
          'Verify term POS and meanings',
          'Generate example audio',
          'Verify phrase normalization',
          'Check frequency ranking',
        ];
      } else if (type.contains('path')) {
        suggestedTasks = [
          'Implement interactive logic',
          'Define completion criteria',
          'Create visual assets',
        ];
      } else {
        suggestedTasks = ['Implement content implementation task'];
      }

      return {
        'seed_id': 'seed_${it.candidateId}',
        'candidate_id': it.candidateId,
        'work_type': type,
        'priority': _calculatePriority(it.scores),
        'suggested_tasks': suggestedTasks,
        'dependencies': [],
        'notes_zh_tw': it.humanNotesZhTw.isNotEmpty
            ? it.humanNotesZhTw
            : it.reviewSummaryZhTw,
        'metadata': {
          'target_level': it.targetLevel,
          'target_unit_id': it.targetUnitId,
        },
      };
    }).toList();

    return const JsonEncoder.withIndent('  ').convert(seeds);
  }

  static String _calculatePriority(Map<String, double> scores) {
    final fit = scores['fit'] ?? 0.0;
    if (fit >= 0.9) return 'P0';
    if (fit >= 0.7) return 'P1';
    if (fit >= 0.5) return 'P2';
    return 'P3';
  }
}
