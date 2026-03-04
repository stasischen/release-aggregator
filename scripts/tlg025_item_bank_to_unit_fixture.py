#!/usr/bin/env python3
"""Convert TLG-025 item bank JSON to modular viewer unit fixture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')


def item_to_node(item: dict, idx: int) -> dict:
    item_id = item.get('item_id', f'IB-{idx:03d}')
    item_type = item.get('item_type', 'unknown')
    skill = item.get('skill', 'reading')
    return {
        'id': item_id,
        'candidate_type': 'lesson',
        'content_form': 'quiz_item',
        'learning_role': 'review_retrieval',
        'skill_focus': [skill],
        'output_mode': 'none',
        'duration_min': 1,
        'title_zh_tw': f"題目 {idx:02d} · {item_type}",
        'summary_zh_tw': item.get('prompt_zh_tw', ''),
        'expected_output_zh_tw': '先作答再自我核對答案。',
        'payload': {'item': item},
        'adapter_hints': {
            'content_renderer_key': 'quiz_item',
            'interaction_renderer_key': None
        }
    }


def to_unit_fixture(bank: dict):
    bank_id = bank.get('bank_id', 'KO-IBANK-UNKNOWN')
    source_unit_id = bank.get('source_unit_id', 'UNKNOWN')
    level = bank.get('level', 'A1')
    target_lang = bank.get('target_lang', 'ko')
    support_langs = bank.get('support_langs', ['zh_tw', 'en'])
    items = bank.get('items', [])

    unit_id = f"{source_unit_id}-IBANK-V1"
    sequence = [item_to_node(item, idx + 1) for idx, item in enumerate(items)]

    return {
        'version': 'unit_blueprint_v0.1',
        'adapter_contract': {
            'adapter_version': 'frontend_unit_adapter_v0',
            'stability': 'item_bank_preview',
            'fallback_locale_order': support_langs,
            'notes': f'Generated from {bank_id} for viewer preview.'
        },
        'unit': {
            'unit_id': unit_id,
            'title_zh_tw': f'題庫複習 {source_unit_id}',
            'target_language': target_lang,
            'learner_locale_source': support_langs[0] if support_langs else 'zh_tw',
            'level': level,
            'theme_zh_tw': '題庫式複習（Item Bank）',
            'output_ratio_target': 0.8,
            'can_do_zh_tw': [
                '完成題庫複習並核對答案',
                '針對錯題進行重複回想'
            ]
        },
        'sequence': sequence
    }


def main():
    ap = argparse.ArgumentParser(description='Convert item bank JSON to unit fixture for modular viewer')
    ap.add_argument('--input', required=True, help='Input item bank JSON path')
    ap.add_argument('--output', required=True, help='Output viewer unit fixture JSON path')
    args = ap.parse_args()

    bank = load_json(Path(args.input))
    fixture = to_unit_fixture(bank)
    save_json(Path(args.output), fixture)
    print(f"generated nodes={len(fixture.get('sequence', []))} -> {args.output}")


if __name__ == '__main__':
    main()
