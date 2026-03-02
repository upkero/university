from __future__ import annotations

import unittest

from src.expression_parser import parse_expression
from src.post_classes import determine_post_classes
from src.truth_table import build_truth_table
from src.zhegalkin import build_zhegalkin_polynomial


class PostAndZhegalkinTests(unittest.TestCase):
    def test_and_function_properties(self) -> None:
        table = build_truth_table(parse_expression("a&b"))
        polynomial = build_zhegalkin_polynomial(table)
        post = determine_post_classes(table)

        self.assertEqual(polynomial.expression, "a*b")
        self.assertTrue(post.t0)
        self.assertTrue(post.t1)
        self.assertFalse(post.s)
        self.assertTrue(post.m)
        self.assertFalse(post.l)

    def test_xor_function_is_linear_and_not_monotone(self) -> None:
        table = build_truth_table(parse_expression("(a&!b)|(!a&b)"))
        polynomial = build_zhegalkin_polynomial(table)
        post = determine_post_classes(table)

        self.assertEqual(polynomial.expression, "a ^ b")
        self.assertTrue(post.l)
        self.assertFalse(post.m)

    def test_variable_function_is_self_dual(self) -> None:
        table = build_truth_table(parse_expression("a"))
        post = determine_post_classes(table)
        self.assertTrue(post.s)


if __name__ == "__main__":
    unittest.main()

