from __future__ import annotations

import unittest

from src.expression_parser import parse_expression


class ExpressionParserTests(unittest.TestCase):
    def test_parses_unicode_symbols(self) -> None:
        parsed = parse_expression("!(!a→!b)∨c")
        self.assertEqual(parsed.source, "!(!a->!b)|c")
        self.assertEqual(parsed.variables, ("a", "b", "c"))

        self.assertEqual(parsed.root.evaluate({"a": 0, "b": 0, "c": 0}), 0)
        self.assertEqual(parsed.root.evaluate({"a": 0, "b": 1, "c": 0}), 1)
        self.assertEqual(parsed.root.evaluate({"a": 1, "b": 1, "c": 1}), 1)

    def test_implication_is_right_associative(self) -> None:
        parsed = parse_expression("a->b->c")
        result = parsed.root.evaluate({"a": 1, "b": 1, "c": 0})
        self.assertEqual(result, 0)

    def test_operator_precedence(self) -> None:
        parsed = parse_expression("a|b&c")
        self.assertEqual(parsed.root.evaluate({"a": 0, "b": 1, "c": 0}), 0)
        self.assertEqual(parsed.root.evaluate({"a": 0, "b": 1, "c": 1}), 1)

    def test_invalid_character_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            parse_expression("a + b")

    def test_unbalanced_parenthesis_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            parse_expression("(a&b")

    def test_missing_assignment_variable_raises(self) -> None:
        parsed = parse_expression("a&b")
        with self.assertRaises(ValueError):
            parsed.root.evaluate({"a": 1})


if __name__ == "__main__":
    unittest.main()

