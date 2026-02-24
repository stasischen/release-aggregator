import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../models/candidate_review_item.dart';
import '../providers/review_provider.dart';

class ContentReviewScreen extends StatelessWidget {
  const ContentReviewScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('候選內容中文審核台'),
        actions: [
          IconButton(
            tooltip: '匯入候選 JSON',
            icon: const Icon(Icons.file_upload),
            onPressed: () => _showImportDialog(context),
          ),
          IconButton(
            tooltip: '匯出審核結果',
            icon: const Icon(Icons.file_download),
            onPressed: () => _showExportDialog(context),
          ),
          const SizedBox(width: 8),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => context.read<ReviewProvider>().loadMockData(),
          ),
        ],
      ),
      body: Consumer<ReviewProvider>(
        builder: (context, provider, child) {
          if (provider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (provider.items.isEmpty) {
            return const Center(child: Text('暫無候選內容'));
          }

          return Column(
            children: [
              // Top Bar: Search and Filters
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Row(
                  children: [
                    Expanded(
                      flex: 2,
                      child: TextField(
                        decoration: const InputDecoration(
                          hintText: '搜尋標題、摘要或 Can-do...',
                          prefixIcon: Icon(Icons.search),
                          border: OutlineInputBorder(),
                        ),
                        onChanged: (val) => provider.setSearchQuery(val),
                      ),
                    ),
                    const SizedBox(width: 8),
                    DropdownButton<HumanDecision?>(
                      value: provider.filterDecision,
                      hint: const Text('所有狀態'),
                      items: [
                        const DropdownMenuItem(
                          value: null,
                          child: Text('所有狀態'),
                        ),
                        ...HumanDecision.values.map(
                          (d) =>
                              DropdownMenuItem(value: d, child: Text(d.label)),
                        ),
                      ],
                      onChanged: (val) => provider.setFilterDecision(val),
                    ),
                    const SizedBox(width: 8),
                    FilterChip(
                      label: const Text('只看未審核'),
                      selected: provider.showUnreviewedOnly,
                      onSelected: (val) => provider.setShowUnreviewedOnly(val),
                    ),
                    const SizedBox(width: 8),
                    if (provider.selectedIds.isNotEmpty) ...[
                      const VerticalDivider(width: 20),
                      Text('選取 ${provider.selectedIds.length} 筆:'),
                      const SizedBox(width: 8),
                      OutlinedButton(
                        onPressed: () =>
                            provider.batchUpdateDecision(HumanDecision.reject),
                        child: const Text('批次淘汰'),
                      ),
                      const SizedBox(width: 4),
                      OutlinedButton(
                        onPressed: () =>
                            provider.batchUpdateDecision(HumanDecision.parked),
                        child: const Text('批次擱置'),
                      ),
                      const SizedBox(width: 4),
                      TextButton(
                        onPressed: () => provider.clearSelection(),
                        child: const Text('清除選取'),
                      ),
                    ],
                    const Spacer(),
                    Text(
                      '進度: ${provider.reviewedCount} / ${provider.totalCount}',
                    ),
                    const SizedBox(width: 16),
                  ],
                ),
              ),
              const Divider(height: 1),
              Expanded(
                child: Row(
                  children: [
                    // Left: List
                    SizedBox(
                      width: 350,
                      child: ListView.builder(
                        itemCount: provider.filteredItems.length,
                        itemBuilder: (context, index) {
                          final item = provider.filteredItems[index];
                          final isSelected = provider.selectedIds.contains(
                            item.candidateId,
                          );
                          return ListTile(
                            leading: Checkbox(
                              value: isSelected,
                              onChanged: (_) =>
                                  provider.toggleSelection(item.candidateId),
                            ),
                            selected:
                                provider.selectedItem?.candidateId ==
                                item.candidateId,
                            title: Text(item.titleZhTw),
                            subtitle: Text(
                              '${item.candidateType} | ${item.targetLevel} | ${item.targetUnitId}',
                            ),
                            trailing: _buildDecisionBadge(item.humanDecision),
                            onTap: () => provider.selectItem(item),
                          );
                        },
                      ),
                    ),
                    const VerticalDivider(width: 1),
                    // Right: Details
                    Expanded(
                      child: provider.selectedItem == null
                          ? const Center(child: Text('請選擇一個項目進行審核'))
                          : _DetailView(item: provider.selectedItem!),
                    ),
                  ],
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  void _showImportDialog(BuildContext context) {
    final controller = TextEditingController();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('匯入候選 JSON'),
        content: TextField(
          controller: controller,
          maxLines: 15,
          decoration: const InputDecoration(
            hintText: '將 candidate_packs.json 的內容貼在此處...',
            border: OutlineInputBorder(),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('取消'),
          ),
          ElevatedButton(
            onPressed: () async {
              try {
                await context.read<ReviewProvider>().importItems(
                  controller.text,
                );
                if (context.mounted) Navigator.pop(context);
              } catch (e) {
                if (context.mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('匯入失敗: $e'),
                      backgroundColor: Colors.red,
                    ),
                  );
                }
              }
            },
            child: const Text('匯入'),
          ),
        ],
      ),
    );
  }

  void _showExportDialog(BuildContext context) {
    final provider = context.read<ReviewProvider>();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('匯出審核結果'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('目前進度：${provider.reviewedCount} / ${provider.totalCount}'),
            const SizedBox(height: 16),
            const Text('請選擇匯出類型：'),
            const SizedBox(height: 8),
            ListTile(
              title: const Text('review_results.json (完整)'),
              onTap: () => _copyToClipboard(context, provider.getResultsJson()),
            ),
            ListTile(
              title: const Text('accepted_candidates.json (僅 accept)'),
              onTap: () =>
                  _copyToClipboard(context, provider.getAcceptedJson()),
            ),
            ListTile(
              title: const Text('審核統計摘要'),
              onTap: () => _copyToClipboard(context, provider.getSummary()),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('關閉'),
          ),
        ],
      ),
    );
  }

  void _copyToClipboard(BuildContext context, String text) {
    Clipboard.setData(ClipboardData(text: text));
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('內容已複製到剪貼簿')));
  }

  Widget _buildDecisionBadge(HumanDecision decision) {
    Color color;
    switch (decision) {
      case HumanDecision.unreviewed:
        color = Colors.grey;
        break;
      case HumanDecision.accept:
        color = Colors.green;
        break;
      case HumanDecision.revise:
        color = Colors.orange;
        break;
      case HumanDecision.reject:
        color = Colors.red;
        break;
      case HumanDecision.parked:
        color = Colors.blue;
        break;
    }
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withAlpha(25),
        border: Border.all(color: color),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Text(decision.label, style: TextStyle(color: color, fontSize: 12)),
    );
  }
}

class _DetailView extends StatefulWidget {
  final CandidateReviewItem item;
  const _DetailView({required this.item});

  @override
  State<_DetailView> createState() => _DetailViewState();
}

class _DetailViewState extends State<_DetailView> {
  late TextEditingController _notesController;

  @override
  void initState() {
    super.initState();
    _notesController = TextEditingController(text: widget.item.humanNotesZhTw);
  }

  @override
  void didUpdateWidget(_DetailView oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.item.candidateId != widget.item.candidateId) {
      _notesController.text = widget.item.humanNotesZhTw;
    }
  }

  @override
  void dispose() {
    _notesController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<ReviewProvider>();
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      widget.item.titleZhTw,
                      style: Theme.of(context).textTheme.headlineMedium,
                    ),
                    Text(
                      widget.item.subtitleZhTw,
                      style: Theme.of(
                        context,
                      ).textTheme.titleMedium?.copyWith(color: Colors.grey),
                    ),
                  ],
                ),
              ),
              _buildDecisionButtons(context),
            ],
          ),
          const SizedBox(height: 24),
          // Content Scrollable
          Expanded(
            child: ListView(
              children: [
                _buildSection(
                  'Agent 建議',
                  Text(widget.item.agentRecommendation),
                ),
                _buildSection('中文摘要', Text(widget.item.reviewSummaryZhTw)),
                _buildSection(
                  'Novelty 理由',
                  Text(widget.item.noveltyRationaleZhTw),
                ),
                _buildSection(
                  'Can-Do',
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: widget.item.canDoZhTw
                        .map((s) => Text('• $s'))
                        .toList(),
                  ),
                ),
                _buildSection(
                  '風險備註',
                  widget.item.riskFlagsZhTw.isEmpty
                      ? const Text('無')
                      : Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: widget.item.riskFlagsZhTw
                              .map(
                                (s) => Text(
                                  '• $s',
                                  style: const TextStyle(color: Colors.red),
                                ),
                              )
                              .toList(),
                        ),
                ),
                const Divider(),
                _buildSection(
                  '人工備註 (繁體中文)',
                  TextField(
                    controller: _notesController,
                    maxLines: 5,
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      hintText: '輸入審核備註...',
                    ),
                    onChanged: (val) =>
                        provider.updateNotes(widget.item.candidateId, val),
                  ),
                ),
                const Divider(),
                // Foreign Content (Collapsible)
                ExpansionTile(
                  title: const Text('外語原始內容預覽'),
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(12),
                        color: Colors.grey[100],
                        child: Text(
                          const JsonEncoder.withIndent(
                            '  ',
                          ).convert(widget.item.foreignPreview),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSection(String title, Widget content) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
          ),
          const SizedBox(height: 8),
          content,
        ],
      ),
    );
  }

  Widget _buildDecisionButtons(BuildContext context) {
    final provider = context.read<ReviewProvider>();
    return Wrap(
      spacing: 8,
      children: [
        ElevatedButton(
          onPressed: () => provider.updateDecision(
            widget.item.candidateId,
            HumanDecision.accept,
          ),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.green,
            foregroundColor: Colors.white,
          ),
          child: const Text('接受'),
        ),
        ElevatedButton(
          onPressed: () => provider.updateDecision(
            widget.item.candidateId,
            HumanDecision.revise,
          ),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.orange,
            foregroundColor: Colors.white,
          ),
          child: const Text('修改'),
        ),
        ElevatedButton(
          onPressed: () => provider.updateDecision(
            widget.item.candidateId,
            HumanDecision.reject,
          ),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.red,
            foregroundColor: Colors.white,
          ),
          child: const Text('淘汰'),
        ),
        ElevatedButton(
          onPressed: () => provider.updateDecision(
            widget.item.candidateId,
            HumanDecision.parked,
          ),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.blue,
            foregroundColor: Colors.white,
          ),
          child: const Text('擱置'),
        ),
      ],
    );
  }
}
