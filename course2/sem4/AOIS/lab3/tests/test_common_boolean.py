import unittest

from src.common.boolean import (
    assignment_to_index,
    build_sknf,
    evaluate_sop,
    index_to_assignment,
    minimize_sop,
)


class BooleanUtilsTestCase(unittest.TestCase):
    def test_assignment_index_roundtrip(self) -> None:
        assignment = (1, 0, 1, 1)
        index = assignment_to_index(assignment)
        self.assertEqual(index, 11)
        self.assertEqual(index_to_assignment(index, 4), assignment)

    def test_index_to_assignment_raises_for_invalid_index(self) -> None:
        with self.assertRaises(ValueError):
            index_to_assignment(8, 3)

    def test_build_sknf(self) -> None:
        expression = build_sknf(("A", "B"), (0, 1, 1, 0))
        self.assertEqual(expression, "(A + B) * (!A + !B)")

    def test_minimize_or_function(self) -> None:
        minimized = minimize_sop(("A", "B"), ones=(1, 2, 3))
        self.assertEqual(set(minimized.patterns), {"1-", "-1"})

    def test_minimize_with_dont_care(self) -> None:
        minimized = minimize_sop(("A", "B", "C"), ones=(1, 3), dont_cares=(5, 7))
        self.assertEqual(minimized.patterns, ("--1",))
        self.assertEqual(minimized.expression, "C")

    def test_minimize_constant_one(self) -> None:
        minimized = minimize_sop(("A", "B"), ones=(0,), dont_cares=(1, 2, 3))
        self.assertEqual(minimized.patterns, ("--",))
        self.assertEqual(minimized.expression, "1")

    def test_minimize_conflicting_sets_raises(self) -> None:
        with self.assertRaises(ValueError):
            minimize_sop(("A",), ones=(0,), dont_cares=(0,))

    def test_evaluate_sop(self) -> None:
        minimized = minimize_sop(("A", "B"), ones=(1, 2))
        self.assertEqual(evaluate_sop(minimized.terms, {"A": 0, "B": 0}), 0)
        self.assertEqual(evaluate_sop(minimized.terms, {"A": 0, "B": 1}), 1)
        self.assertEqual(evaluate_sop(minimized.terms, {"A": 1, "B": 0}), 1)
        self.assertEqual(evaluate_sop(minimized.terms, {"A": 1, "B": 1}), 0)


if __name__ == "__main__":
    unittest.main()

