import io
import unittest
from contextlib import redirect_stdout

from src.app import generate_report, main


class AppReportTestCase(unittest.TestCase):
    def test_report_contains_all_sections(self) -> None:
        report = generate_report()
        self.assertIn("Task 1", report)
        self.assertIn("Task 2", report)
        self.assertIn("Task 3", report)
        self.assertIn("PCNF", report)
        self.assertIn("Minimized functions", report)
        self.assertIn("Excitation functions", report)

    def test_main_prints_report(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = main()
        output = buffer.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("Task 1", output)


if __name__ == "__main__":
    unittest.main()
