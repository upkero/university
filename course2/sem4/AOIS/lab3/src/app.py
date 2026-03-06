from __future__ import annotations

from src.part1 import render_part1, solve_part1
from src.part2 import render_part2, solve_part2
from src.part3 import render_part3, solve_part3


def generate_report() -> str:
    part1_result = solve_part1()
    part2_result = solve_part2()
    part3_result = solve_part3()

    sections = [
        render_part1(part1_result),
        render_part2(part2_result),
        render_part3(part3_result),
    ]
    return "\n\n".join(sections)


def main() -> int:
    print(generate_report())
    return 0

