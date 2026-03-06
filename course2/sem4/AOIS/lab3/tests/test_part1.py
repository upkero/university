import unittest

from src.common.boolean import evaluate_sop
from src.part1.full_adder import solve_part1


class Part1TestCase(unittest.TestCase):
    def test_part1_table_and_sknf(self) -> None:
        result = solve_part1()
        self.assertEqual(len(result.rows), 8)
        self.assertEqual((result.rows[0].s, result.rows[0].c), (0, 0))
        self.assertEqual((result.rows[-1].s, result.rows[-1].c), (1, 1))

        self.assertEqual(
            result.sknf_s,
            "(X1 + X2 + X3) * (X1 + !X2 + !X3) * (!X1 + X2 + !X3) * (!X1 + !X2 + X3)",
        )
        self.assertEqual(
            result.sknf_c,
            "(X1 + X2 + X3) * (X1 + X2 + !X3) * (X1 + !X2 + X3) * (!X1 + X2 + X3)",
        )

    def test_part1_minimized_equivalence(self) -> None:
        result = solve_part1()
        for row in result.rows:
            assignment = {"X1": row.x1, "X2": row.x2, "X3": row.x3}
            self.assertEqual(evaluate_sop(result.minimized_s.terms, assignment), row.s)
            self.assertEqual(evaluate_sop(result.minimized_c.terms, assignment), row.c)


if __name__ == "__main__":
    unittest.main()

