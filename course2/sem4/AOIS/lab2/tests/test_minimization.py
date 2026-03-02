from __future__ import annotations

import unittest

from src.minimization import (
    implicant_covers_minterm,
    minimize_by_calculation,
    minimize_by_calculation_table,
)
from src.truth_table import truth_table_from_vector


class MinimizationTests(unittest.TestCase):
    def test_example_from_description(self) -> None:
        table = truth_table_from_vector(("a", "b", "c"), (0, 0, 0, 1, 1, 1, 1, 1))

        calculation = minimize_by_calculation(table)
        table_method = minimize_by_calculation_table(table)

        self.assertEqual(calculation.expression, "a|(b&c)")
        self.assertEqual(table_method.expression, "a|(b&c)")
        self.assertEqual(calculation.selected_implicants, ("1--", "-11"))
        self.assertTrue(any(stage.records for stage in calculation.stages))
        self.assertIsNotNone(table_method.chart)

    def test_zero_and_one_functions(self) -> None:
        zero_table = truth_table_from_vector(("a", "b"), (0, 0, 0, 0))
        one_table = truth_table_from_vector(("a", "b"), (1, 1, 1, 1))

        zero_result = minimize_by_calculation(zero_table)
        one_result = minimize_by_calculation(one_table)

        self.assertEqual(zero_result.expression, "0")
        self.assertEqual(one_result.expression, "1")

    def test_implicant_coverage(self) -> None:
        self.assertTrue(implicant_covers_minterm("1-0", 4, 3))
        self.assertFalse(implicant_covers_minterm("1-0", 5, 3))


if __name__ == "__main__":
    unittest.main()

