enum HumanDecision {
  unreviewed,
  accept,
  revise,
  reject,
  parked;

  String get label {
    switch (this) {
      case HumanDecision.unreviewed:
        return '未審核';
      case HumanDecision.accept:
        return '接受';
      case HumanDecision.revise:
        return '修改';
      case HumanDecision.reject:
        return '淘汰';
      case HumanDecision.parked:
        return '擱置';
    }
  }

  static HumanDecision fromString(String? value) {
    return HumanDecision.values.firstWhere(
      (e) => e.name == value,
      orElse: () => HumanDecision.unreviewed,
    );
  }
}

class CandidateReviewItem {
  final String candidateId;
  final String batchId;
  final String candidateType;
  final String targetLevel;
  final String targetUnitId;
  final int targetPosition;
  final String titleZhTw;
  final String subtitleZhTw;
  final List<String> canDoZhTw;
  final String reviewSummaryZhTw;
  final String noveltyRationaleZhTw;
  final List<String> riskFlagsZhTw;
  final String agentRecommendation;
  final Map<String, double> scores;
  final Map<String, dynamic> foreignPreview;

  // Review fields
  HumanDecision humanDecision;
  String humanNotesZhTw;
  DateTime updatedAt;

  CandidateReviewItem({
    required this.candidateId,
    required this.batchId,
    required this.candidateType,
    required this.targetLevel,
    required this.targetUnitId,
    required this.targetPosition,
    required this.titleZhTw,
    required this.subtitleZhTw,
    required this.canDoZhTw,
    required this.reviewSummaryZhTw,
    required this.noveltyRationaleZhTw,
    required this.riskFlagsZhTw,
    required this.agentRecommendation,
    required this.scores,
    required this.foreignPreview,
    this.humanDecision = HumanDecision.unreviewed,
    this.humanNotesZhTw = '',
    DateTime? updatedAt,
  }) : updatedAt = updatedAt ?? DateTime.now();

  factory CandidateReviewItem.fromJson(Map<String, dynamic> json) {
    return CandidateReviewItem(
      candidateId: json['candidate_id'] ?? '',
      batchId: json['batch_id'] ?? '',
      candidateType: json['candidate_type'] ?? '',
      targetLevel: json['target_level'] ?? '',
      targetUnitId: json['target_unit_id'] ?? '',
      targetPosition: json['target_position'] ?? 0,
      titleZhTw: json['title_zh_tw'] ?? '',
      subtitleZhTw: json['subtitle_zh_tw'] ?? '',
      canDoZhTw: List<String>.from(json['can_do_zh_tw'] ?? []),
      reviewSummaryZhTw: json['review_summary_zh_tw'] ?? '',
      noveltyRationaleZhTw: json['novelty_rationale_zh_tw'] ?? '',
      riskFlagsZhTw: List<String>.from(json['risk_flags_zh_tw'] ?? []),
      agentRecommendation: json['agent_recommendation'] ?? '',
      scores: Map<String, double>.from(
        (json['scores'] ?? {}).map(
          (k, v) => MapEntry(k, (v as num).toDouble()),
        ),
      ),
      foreignPreview: Map<String, dynamic>.from(json['foreign_preview'] ?? {}),
      humanDecision: HumanDecision.fromString(json['human_decision']),
      humanNotesZhTw: json['human_notes_zh_tw'] ?? '',
      updatedAt: json['updated_at'] != null
          ? DateTime.parse(json['updated_at'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'candidate_id': candidateId,
      'batch_id': batchId,
      'candidate_type': candidateType,
      'target_level': targetLevel,
      'target_unit_id': targetUnitId,
      'target_position': targetPosition,
      'title_zh_tw': titleZhTw,
      'subtitle_zh_tw': subtitleZhTw,
      'can_do_zh_tw': canDoZhTw,
      'review_summary_zh_tw': reviewSummaryZhTw,
      'novelty_rationale_zh_tw': noveltyRationaleZhTw,
      'risk_flags_zh_tw': riskFlagsZhTw,
      'agent_recommendation': agentRecommendation,
      'scores': scores,
      'foreign_preview': foreignPreview,
      'human_decision': humanDecision.name,
      'human_notes_zh_tw': humanNotesZhTw,
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}
