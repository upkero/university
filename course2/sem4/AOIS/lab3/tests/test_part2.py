import unittest

from src.common.boolean import evaluate_sop
from src.part2.bcd2421_offset import CODE_2421, build_truth_rows, solve_part2


class Part2TestCase(unittest.TestCase):
    def test_code_2421_mapping(self) -> None:
        self.assertEqual(len(CODE_2421), 10)
        self.assertEqual(len(set(CODE_2421.values())), 10)

    def test_truth_table_contains_valid_and_invalid_rows(self) -> None:
        rows = build_truth_rows()
        self.assertEqual(len(rows), 16)

        valid_rows = [row for row in rows if row.in_digit is not None]
        invalid_rows = [row for row in rows if row.in_digit is None]
        self.assertEqual(len(valid_rows), 10)
        self.assertEqual(len(invalid_rows), 6)

        self.assertEqual((rows[0].in_digit, rows[0].out_digit), (0, 6))
        self.assertEqual((rows[0].y3, rows[0].y2, rows[0].y1, rows[0].y0), (1, 1, 0, 0))

        invalid_0101 = rows[5]
        self.assertIsNone(invalid_0101.in_digit)
        self.assertIsNone(invalid_0101.y0)

    def test_minimized_functions_equivalent_on_valid_codes(self) -> None:
        result = solve_part2()
        for row in result.rows:
            if row.in_digit is None:
                continue
            assignment = {"A": row.a, "B": row.b, "C": row.c, "D": row.d}
            expected = {
                "Y3": row.y3,
                "Y2": row.y2,
                "Y1": row.y1,
                "Y0": row.y0,
            }
            for output_name, minimized in result.minimized_outputs:
                self.assertEqual(evaluate_sop(minimized.terms, assignment), expected[output_name])


if __name__ == "__main__":
    unittest.main()

