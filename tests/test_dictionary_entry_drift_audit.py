import unittest

from scripts import audit_dictionary_entry_drift as audit


class DictionaryEntryDriftAuditTest(unittest.TestCase):
    def test_audit_keeps_homonym_inside_single_atom_row(self) -> None:
        rows = [
            {
                "atom_id": "ko:n:밤",
                "lemma": "밤",
                "pos": "n",
                "surface_forms": ["밤"],
                "definitions": {
                    "zh_tw": [
                        {"entry_no": 1, "sense_id": "s1", "gloss": "夜晚"},
                        {"entry_no": 2, "sense_id": "s2", "gloss": "栗子"},
                    ]
                },
            },
            {
                "atom_id": "ko:adv:밤",
                "lemma": "밤",
                "pos": "adv",
                "surface_forms": ["밤"],
                "definitions": {"zh_tw": [{"entry_no": 1, "sense_id": "s1", "gloss": "夜間"}]},
            },
        ]

        result = audit.audit(rows)

        self.assertEqual(len(result.same_row_multi_entry), 1)
        self.assertEqual(audit.atom_id(result.same_row_multi_entry[0]), "ko:n:밤")
        self.assertEqual(len(result.same_surface_pos_multi_rows), 0)
        self.assertEqual(len(result.same_surface_cross_pos), 1)

    def test_audit_flags_same_surface_same_pos_multi_row_collision(self) -> None:
        rows = [
            {
                "atom_id": "ko:n:밤",
                "lemma": "밤",
                "pos": "n",
                "surface_forms": ["밤"],
                "definitions": {"zh_tw": [{"entry_no": 1, "sense_id": "s1", "gloss": "夜晚"}]},
            },
            {
                "atom_id": "ko:n:밤_2",
                "lemma": "밤",
                "pos": "n",
                "surface_forms": ["밤"],
                "definitions": {"zh_tw": [{"entry_no": 1, "sense_id": "s1", "gloss": "栗子"}]},
            },
        ]

        result = audit.audit(rows)

        self.assertEqual(len(result.same_surface_pos_multi_rows), 1)
        (surface, pos), collision_rows = result.same_surface_pos_multi_rows[0]
        self.assertEqual((surface, pos), ("밤", "n"))
        self.assertEqual([audit.atom_id(row) for row in collision_rows], ["ko:n:밤", "ko:n:밤_2"])


if __name__ == "__main__":
    unittest.main()
