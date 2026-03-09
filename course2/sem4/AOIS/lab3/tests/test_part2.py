import unittest

from src.part2.bcd2421_offset import CODE_2421, build_truth_rows, evaluate_structural_outputs, solve_part2


class Part2TestCase(unittest.TestCase):
    def test_code_2421_mapping(self) -> None:
        self.assertEqual(len(CODE_2421), 10)
        self.assertEqual(len(set(CODE_2421.values())), 10)

    def test_truth_table_contains_valid_and_invalid_rows(self) -> None:
        rows = build_truth_rows()
        self.assertEqual(len(rows), 256)

        valid_rows = [row for row in rows if row.digit_a is not None and row.digit_b is not None]
        invalid_rows = [row for row in rows if row.digit_a is None or row.digit_b is None]
        self.assertEqual(len(valid_rows), 100)
        self.assertEqual(len(invalid_rows), 156)

        zero_sum = rows[0]
        self.assertEqual((zero_sum.digit_a, zero_sum.digit_b, zero_sum.total), (0, 0, 0))
        self.assertEqual((zero_sum.tens_digit, zero_sum.units_digit, zero_sum.ovf), (0, 0, 0))
        self.assertEqual(
            (zero_sum.t3, zero_sum.t2, zero_sum.t1, zero_sum.t0),
            CODE_2421[0],
        )
        self.assertEqual(
            (zero_sum.u3, zero_sum.u2, zero_sum.u1, zero_sum.u0),
            CODE_2421[0],
        )

        max_sum = rows[-1]
        self.assertEqual((max_sum.digit_a, max_sum.digit_b, max_sum.total), (9, 9, 18))
        self.assertEqual((max_sum.offset, max_sum.tens_digit, max_sum.units_digit, max_sum.ovf), (6, 1, 8, 1))
        self.assertEqual(
            (max_sum.t3, max_sum.t2, max_sum.t1, max_sum.t0),
            CODE_2421[1],
        )
        self.assertEqual(
            (max_sum.u3, max_sum.u2, max_sum.u1, max_sum.u0),
            CODE_2421[8],
        )

        invalid_row = next(row for row in rows if (row.a3, row.a2, row.a1, row.a0) == (0, 1, 0, 1))
        self.assertIsNone(invalid_row.digit_a)
        self.assertIsNone(invalid_row.u0)

    def test_structural_netlist_equivalent_on_valid_codes(self) -> None:
        result = solve_part2()
        for row in result.rows:
            if row.digit_a is None or row.digit_b is None:
                continue

            assignment = {
                "A3": row.a3,
                "A2": row.a2,
                "A1": row.a1,
                "A0": row.a0,
                "B3": row.b3,
                "B2": row.b2,
                "B1": row.b1,
                "B0": row.b0,
            }
            expected = {
                "T3": row.t3,
                "T2": row.t2,
                "T1": row.t1,
                "T0": row.t0,
                "U3": row.u3,
                "U2": row.u2,
                "U1": row.u1,
                "U0": row.u0,
                "OVF": row.ovf,
            }
            actual = evaluate_structural_outputs(result.netlist, assignment)
            self.assertEqual(actual, expected)

    def test_structural_netlist_is_compact_and_uses_xor(self) -> None:
        result = solve_part2()
        gate_types = {gate.gate_type for gate in result.netlist.gates}
        self.assertIn("XOR", gate_types)
        self.assertIn("AND", gate_types)
        self.assertIn("OR", gate_types)
        self.assertLess(len(result.netlist.gates), 50)


if __name__ == "__main__":
    unittest.main()
