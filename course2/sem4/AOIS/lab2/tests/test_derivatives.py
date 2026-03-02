from __future__ import annotations

import unittest

from src.derivatives import boolean_derivative, build_all_derivatives, find_fictitious_variables
from src.expression_parser import parse_expression
from src.truth_table import build_truth_table


class DerivativesTests(unittest.TestCase):
    def test_fictitious_variable_detection(self) -> None:
        table = build_truth_table(parse_expression("a|(b&!b)"))
        fictitious = find_fictitious_variables(table)
        self.assertEqual(fictitious, ("b",))

    def test_partial_derivatives(self) -> None:
        table = build_truth_table(parse_expression("a|(b&!b)"))
        derivative_a = boolean_derivative(table, ("a",))
        derivative_b = boolean_derivative(table, ("b",))

        self.assertEqual(derivative_a.vector, (1, 1, 1, 1))
        self.assertEqual(derivative_b.vector, (0, 0, 0, 0))

    def test_mixed_derivative(self) -> None:
        table = build_truth_table(parse_expression("a&b&c"))
        derivative_ab = boolean_derivative(table, ("a", "b"))
        self.assertEqual(derivative_ab.index_vector, "01010101")
        self.assertEqual(derivative_ab.index_number, 85)

    def test_build_all_derivatives_count(self) -> None:
        table = build_truth_table(parse_expression("a&b&c"))
        derivatives = build_all_derivatives(table, max_order=2)
        self.assertEqual(len(derivatives), 6)

    def test_derivative_unknown_variable_raises(self) -> None:
        table = build_truth_table(parse_expression("a&b"))
        with self.assertRaises(ValueError):
            boolean_derivative(table, ("c",))


if __name__ == "__main__":
    unittest.main()

