import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/candidate_review_item.dart';

class ReviewProvider extends ChangeNotifier {
  List<CandidateReviewItem> _items = [];
  CandidateReviewItem? _selectedItem;
  bool _isLoading = false;

  String _searchQuery = '';
  String? _filterType;
  HumanDecision? _filterDecision;
  bool _showUnreviewedOnly = false;
  final Set<String> _selectedIds = {};

  List<CandidateReviewItem> get items => _items;
  CandidateReviewItem? get selectedItem => _selectedItem;
  bool get isLoading => _isLoading;
  String get searchQuery => _searchQuery;
  String? get filterType => _filterType;
  HumanDecision? get filterDecision => _filterDecision;
  bool get showUnreviewedOnly => _showUnreviewedOnly;
  Set<String> get selectedIds => _selectedIds;

  void toggleSelection(String id) {
    if (_selectedIds.contains(id)) {
      _selectedIds.remove(id);
    } else {
      _selectedIds.add(id);
    }
    notifyListeners();
  }

  void clearSelection() {
    _selectedIds.clear();
    notifyListeners();
  }

  void batchUpdateDecision(HumanDecision decision) {
    for (var id in _selectedIds) {
      final index = _items.indexWhere((it) => it.candidateId == id);
      if (index != -1) {
        _items[index].humanDecision = decision;
        _items[index].updatedAt = DateTime.now();
      }
    }
    _selectedIds.clear();
    saveToStorage();
    notifyListeners();
  }

  List<CandidateReviewItem> get filteredItems {
    return _items.where((it) {
      if (_showUnreviewedOnly && it.humanDecision != HumanDecision.unreviewed) {
        return false;
      }
      if (_filterDecision != null && it.humanDecision != _filterDecision) {
        return false;
      }
      if (_filterType != null && it.candidateType != _filterType) {
        return false;
      }
      if (_searchQuery.isNotEmpty) {
        final query = _searchQuery.toLowerCase();
        final matchTitle = it.titleZhTw.toLowerCase().contains(query);
        final matchSummary = it.reviewSummaryZhTw.toLowerCase().contains(query);
        final matchCanDo = it.canDoZhTw.any(
          (s) => s.toLowerCase().contains(query),
        );
        if (!matchTitle && !matchSummary && !matchCanDo) {
          return false;
        }
      }
      return true;
    }).toList();
  }

  int get totalCount => _items.length;
  int get reviewedCount => _items
      .where((it) => it.humanDecision != HumanDecision.unreviewed)
      .toList()
      .length;

  void setSearchQuery(String query) {
    _searchQuery = query;
    notifyListeners();
  }

  void setFilterType(String? type) {
    _filterType = type;
    notifyListeners();
  }

  void setFilterDecision(HumanDecision? decision) {
    _filterDecision = decision;
    notifyListeners();
  }

  void setShowUnreviewedOnly(bool value) {
    _showUnreviewedOnly = value;
    notifyListeners();
  }

  Future<void> loadMockData() async {
    _isLoading = true;
    notifyListeners();

    try {
      final String response = await rootBundle.loadString(
        'assets/data/mock_candidate_packs.json',
      );
      final List<dynamic> data = json.decode(response);
      _items = data.map((json) => CandidateReviewItem.fromJson(json)).toList();

      // Load saved decisions from SharedPreferences
      await loadFromStorage();

      if (_items.isNotEmpty && _selectedItem == null) {
        _selectedItem = _items.first;
      }
    } catch (e) {
      debugPrint('Error loading mock data: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void selectItem(CandidateReviewItem item) {
    _selectedItem = item;
    notifyListeners();
  }

  void updateDecision(String id, HumanDecision decision) {
    final index = _items.indexWhere((it) => it.candidateId == id);
    if (index != -1) {
      _items[index].humanDecision = decision;
      _items[index].updatedAt = DateTime.now();
      saveToStorage();
      notifyListeners();
    }
  }

  void updateNotes(String id, String notes) {
    final index = _items.indexWhere((it) => it.candidateId == id);
    if (index != -1) {
      _items[index].humanNotesZhTw = notes;
      _items[index].updatedAt = DateTime.now();
      saveToStorage();
      // No notifyListeners here to avoid rebuild while typing,
      // though typically notes are saved on change.
    }
  }

  Future<void> saveToStorage() async {
    final prefs = await SharedPreferences.getInstance();
    final List<String> encoded = _items
        .map((it) => json.encode(it.toJson()))
        .toList();
    await prefs.setStringList('review_results', encoded);
  }

  Future<void> loadFromStorage() async {
    final prefs = await SharedPreferences.getInstance();
    final List<String>? encoded = prefs.getStringList('review_results');
    if (encoded != null) {
      final Map<String, CandidateReviewItem> savedMap = {
        for (var it in encoded.map(
          (s) => CandidateReviewItem.fromJson(json.decode(s)),
        ))
          it.candidateId: it,
      };

      for (var i = 0; i < _items.length; i++) {
        final saved = savedMap[_items[i].candidateId];
        if (saved != null) {
          _items[i].humanDecision = saved.humanDecision;
          _items[i].humanNotesZhTw = saved.humanNotesZhTw;
          _items[i].updatedAt = saved.updatedAt;
        }
      }
    }
  }

  Future<void> importItems(String jsonString) async {
    try {
      final List<dynamic> data = json.decode(jsonString);
      final List<CandidateReviewItem> newItems = data
          .map((json) => CandidateReviewItem.fromJson(json))
          .toList();

      // Merge with existing decisions if any
      final prefs = await SharedPreferences.getInstance();
      final List<String>? encoded = prefs.getStringList('review_results');
      if (encoded != null) {
        final Map<String, CandidateReviewItem> savedMap = {
          for (var it in encoded.map(
            (s) => CandidateReviewItem.fromJson(json.decode(s)),
          ))
            it.candidateId: it,
        };

        for (var item in newItems) {
          final saved = savedMap[item.candidateId];
          if (saved != null) {
            item.humanDecision = saved.humanDecision;
            item.humanNotesZhTw = saved.humanNotesZhTw;
            item.updatedAt = saved.updatedAt;
          }
        }
      }

      _items = newItems;
      if (_items.isNotEmpty) _selectedItem = _items.first;
      saveToStorage();
      notifyListeners();
    } catch (e) {
      debugPrint('Import error: $e');
      rethrow;
    }
  }

  String getResultsJson() {
    return json.encode(_items.map((it) => it.toJson()).toList());
  }

  String getAcceptedJson() {
    return json.encode(
      _items
          .where((it) => it.humanDecision == HumanDecision.accept)
          .map((it) => it.toJson())
          .toList(),
    );
  }

  String getSummary() {
    final stats = <HumanDecision, int>{};
    for (var d in HumanDecision.values) {
      stats[d] = _items.where((it) => it.humanDecision == d).length;
    }
    return stats.entries.map((e) => '${e.key.label}: ${e.value}').join('\n');
  }
}
