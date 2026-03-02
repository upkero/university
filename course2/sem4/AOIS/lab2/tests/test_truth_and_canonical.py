from __future__ import annotations

import unittest

from src.canonical_forms import build_canonical_forms
from src.expression_parser import parse_expression
from src.truth_table import (
    assignment_to_index,
    build_truth_table,
    index_to_assignment,
    truth_table_from_vector,
)


class TruthAndCanonicalTests(unittest.TestCase):
    def test_truth_table_for_or_function(self) -> None:
        parsed = parse_expression("a|b")
        table = build_truth_table(parsed)
        self.assertEqual(table.variables, ("a", "b"))
        self.assertEqual(table.vector, (0, 1, 1, 1))

    def test_canonical_forms(self) -> None:
        parsed = parse_expression("a|b")
        table = build_truth_table(parsed)
        canonical = build_canonical_forms(table)

        self.assertEqual(canonical.sdnf, "(!a&b)|(a&!b)|(a&b)")
        self.assertEqual(canonical.sknf, "(a|b)")
        self.assertEqual(canonical.sdnf_numeric, (1, 2, 3))
        self.assertEqual(canonical.sknf_numeric, (0,))
        self.assertEqual(canonical.index_vector, "0111")
        self.assertEqual(canonical.index_number, 7)

    def test_constant_zero_forms(self) -> None:
        parsed = parse_expression("0")
        table = build_truth_table(parsed)
        canonical = build_canonical_forms(table)
        self.assertEqual(table.variables, tuple())
        self.assertEqual(table.vector, (0,))
        self.assertEqual(canonical.sdnf, "0")
        self.assertEqual(canonical.sknf, "0")
        self.assertEqual(canonical.index_number, 0)

    def test_assignment_index_conversion(self) -> None:
        self.assertEqual(assignment_to_index((1, 0, 1)), 5)
        self.assertEqual(index_to_assignment(5, 3), (1, 0, 1))

    def test_truth_table_from_vector_validation(self) -> None:
        with self.assertRaises(ValueError):
            truth_table_from_vector(("a", "b"), (0, 1, 0))


if __name__ == "__main__":
    unittest.main()

