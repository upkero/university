from __future__ import annotations

import io
import unittest
from unittest.mock import patch

from src.analyzer import analyze_expression
from src.karnaugh import build_karnaugh_layers, minimize_by_karnaugh
from src.main import main
from src.report import render_analysis
from src.truth_table import truth_table_from_vector


class KarnaughAndReportTests(unittest.TestCase):
    def test_karnaugh_gray_order_for_three_variables(self) -> None:
        table = truth_table_from_vector(("a", "b", "c"), (0, 0, 0, 1, 1, 1, 1, 1))
        layers = build_karnaugh_layers(table)
        self.assertEqual(len(layers), 1)
        self.assertEqual(layers[0].col_labels, ("00", "01", "11", "10"))

    def test_karnaugh_matches_table_minimization(self) -> None:
        table = truth_table_from_vector(("a", "b", "c"), (0, 0, 0, 1, 1, 1, 1, 1))
        result = minimize_by_karnaugh(table)
        self.assertEqual(result.expression, "a|(b&c)")
        self.assertTrue(result.groups)
        self.assertIn("[map]", result.rendered_map)

    def test_render_analysis_contains_required_sections(self) -> None:
        analysis = analyze_expression("a|b")
        text = render_analysis(analysis)
        self.assertIn("Таблица истинности:", text)
        self.assertIn("Полином Жегалкина:", text)
        self.assertIn("Минимизация (карта Карно):", text)

    def test_main_returns_error_for_empty_input(self) -> None:
        with patch("builtins.input", return_value=""), patch("sys.argv", ["prog"]), patch(
            "sys.stdout", new_callable=io.StringIO
        ):
            code = main()
        self.assertEqual(code, 1)

    def test_main_successful_execution(self) -> None:
        with patch("sys.argv", ["prog", "a|b"]), patch(
            "sys.stdout", new_callable=io.StringIO
        ) as output:
            code = main()
        self.assertEqual(code, 0)
        self.assertIn("СДНФ", output.getvalue())


if __name__ == "__main__":
    unittest.main()

