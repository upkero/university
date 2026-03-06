from __future__ import annotations

from dataclasses import dataclass

from src.common import (
    Circuit,
    MinimizedSOP,
    build_circuit_from_patterns,
    index_to_assignment,
    minimize_sop,
    render_circuit,
    render_table,
)


INPUT_VARIABLES = ("A", "B", "C", "D")
OUTPUT_VARIABLES = ("Y3", "Y2", "Y1", "Y0")


CODE_2421: dict[int, tuple[int, int, int, int]] = {
    0: (0, 0, 0, 0),
    1: (0, 0, 0, 1),
    2: (0, 0, 1, 0),
    3: (0, 0, 1, 1),
    4: (0, 1, 0, 0),
    5: (1, 0, 1, 1),
    6: (1, 1, 0, 0),
    7: (1, 1, 0, 1),
    8: (1, 1, 1, 0),
    9: (1, 1, 1, 1),
}


@dataclass(frozen=True)
class Part2TruthRow:
    a: int
    b: int
    c: int
    d: int
    in_digit: int | None
    out_digit: int | None
    y3: int | None
    y2: int | None
    y1: int | None
    y0: int | None


@dataclass(frozen=True)
class Part2Result:
    rows: tuple[Part2TruthRow, ...]
    minimized_outputs: tuple[tuple[str, MinimizedSOP], ...]
    circuits: tuple[tuple[str, Circuit], ...]


def build_truth_rows() -> tuple[Part2TruthRow, ...]:
    reverse_map = {code: digit for digit, code in CODE_2421.items()}

    rows: list[Part2TruthRow] = []
    for index in range(16):
        a, b, c, d = index_to_assignment(index, 4)
        input_code = (a, b, c, d)

        input_digit = reverse_map.get(input_code)
        if input_digit is None:
            rows.append(
                Part2TruthRow(
                    a=a,
                    b=b,
                    c=c,
                    d=d,
                    in_digit=None,
                    out_digit=None,
                    y3=None,
                    y2=None,
                    y1=None,
                    y0=None,
                )
            )
            continue

        output_digit = (input_digit + 6) % 10
        y3, y2, y1, y0 = CODE_2421[output_digit]
        rows.append(
            Part2TruthRow(
                a=a,
                b=b,
                c=c,
                d=d,
                in_digit=input_digit,
                out_digit=output_digit,
                y3=y3,
                y2=y2,
                y1=y1,
                y0=y0,
            )
        )
    return tuple(rows)


def solve_part2() -> Part2Result:
    rows = build_truth_rows()
    dont_cares = [
        index for index, row in enumerate(rows) if row.in_digit is None
    ]

    minimized_outputs: list[tuple[str, MinimizedSOP]] = []
    circuits: list[tuple[str, Circuit]] = []
    for output_name in OUTPUT_VARIABLES:
        ones = [
            index
            for index, row in enumerate(rows)
            if getattr(row, output_name.lower()) == 1
        ]
        minimized = minimize_sop(INPUT_VARIABLES, ones, dont_cares)
        circuit = build_circuit_from_patterns(output_name, INPUT_VARIABLES, minimized.patterns)

        minimized_outputs.append((output_name, minimized))
        circuits.append((output_name, circuit))

    return Part2Result(
        rows=rows,
        minimized_outputs=tuple(minimized_outputs),
        circuits=tuple(circuits),
    )


def _render_cell(value: int | None) -> str:
    if value is None:
        return "-"
    return str(value)


def render_part2(result: Part2Result) -> str:
    table = render_table(
        headers=("A", "B", "C", "D", "d", "(d+6)mod10", "Y3", "Y2", "Y1", "Y0"),
        rows=(
            (
                row.a,
                row.b,
                row.c,
                row.d,
                _render_cell(row.in_digit),
                _render_cell(row.out_digit),
                _render_cell(row.y3),
                _render_cell(row.y2),
                _render_cell(row.y1),
                _render_cell(row.y0),
            )
            for row in result.rows
        ),
    )

    lines = [
        "Task 2. 2421 code, shift n = 6",
        "Truth table (unused combinations are don't care):",
        table,
        "Minimized functions:",
    ]

    for output_name, minimized in result.minimized_outputs:
        lines.append(f"{output_name} = {minimized.expression}")

    lines.append("Circuit (NOT, AND, OR):")
    for output_name, circuit in result.circuits:
        lines.append(f"For {output_name}:")
        lines.append(render_circuit(circuit))

    return "\n".join(lines)

