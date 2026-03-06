import unittest

from src.common.boolean import evaluate_sop
from src.part3.counter_tff import build_transition_rows, solve_part3


class Part3TestCase(unittest.TestCase):
    def test_transition_table(self) -> None:
        rows = build_transition_rows()
        self.assertEqual(len(rows), 8)

        for index, row in enumerate(rows):
            next_index = (index + 1) % 8
            next_bits = (row.q2_next, row.q1_next, row.q0_next)
            self.assertEqual(next_bits, tuple((next_index >> shift) & 1 for shift in (2, 1, 0)))

    def test_excitation_functions(self) -> None:
        result = solve_part3()
        expressions = {name: minimized.expression for name, minimized in result.minimized_t}

        self.assertEqual(expressions["T0"], "1")
        self.assertEqual(expressions["T1"], "Q0")
        self.assertEqual(expressions["T2"], "Q1*Q0")

        for row in result.rows:
            assignment = {"Q2": row.q2, "Q1": row.q1, "Q0": row.q0}
            expected = {"T0": row.t0, "T1": row.t1, "T2": row.t2}
            for name, minimized in result.minimized_t:
                self.assertEqual(evaluate_sop(minimized.terms, assignment), expected[name])


if __name__ == "__main__":
    unittest.main()

