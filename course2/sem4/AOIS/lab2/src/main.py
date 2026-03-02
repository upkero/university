from __future__ import annotations

import sys

from src.analyzer import analyze_expression
from src.report import render_analysis


def main() -> int:
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
    else:
        expression = input("Введите логическую формулу: ").strip()

    if not expression:
        print("Пустая формула не поддерживается.")
        return 1

    try:
        result = analyze_expression(expression)
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        return 1

    print(render_analysis(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

