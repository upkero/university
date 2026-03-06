from __future__ import annotations

from dataclasses import dataclass

from src.common import (
    Circuit,
    MinimizedSOP,
    build_circuit_from_patterns,
    build_sknf,
    iter_assignments,
    minimize_sop,
    render_circuit,
    render_table,
)


VARIABLES = ("X1", "X2", "X3")


@dataclass(frozen=True)
class Part1TruthRow:
    x1: int
    x2: int
    x3: int
    s: int
    c: int


@dataclass(frozen=True)
class Part1Result:
    rows: tuple[Part1TruthRow, ...]
    sknf_s: str
    sknf_c: str
    minimized_s: MinimizedSOP
    minimized_c: MinimizedSOP
    circuit_s: Circuit
    circuit_c: Circuit


def _full_adder_outputs(x1: int, x2: int, x3: int) -> tuple[int, int]:
    total = x1 + x2 + x3
    s = total % 2
    c = 1 if total >= 2 else 0
    return s, c


def build_truth_rows() -> tuple[Part1TruthRow, ...]:
    rows: list[Part1TruthRow] = []
    for x1, x2, x3 in iter_assignments(VARIABLES):
        s, c = _full_adder_outputs(x1, x2, x3)
        rows.append(Part1TruthRow(x1=x1, x2=x2, x3=x3, s=s, c=c))
    return tuple(rows)


def solve_part1() -> Part1Result:
    rows = build_truth_rows()
    s_values = [row.s for row in rows]
    c_values = [row.c for row in rows]

    sknf_s = build_sknf(VARIABLES, s_values)
    sknf_c = build_sknf(VARIABLES, c_values)

    ones_s = [index for index, row in enumerate(rows) if row.s == 1]
    ones_c = [index for index, row in enumerate(rows) if row.c == 1]

    minimized_s = minimize_sop(VARIABLES, ones_s)
    minimized_c = minimize_sop(VARIABLES, ones_c)

    circuit_s = build_circuit_from_patterns("S", VARIABLES, minimized_s.patterns)
    circuit_c = build_circuit_from_patterns("C", VARIABLES, minimized_c.patterns)

    return Part1Result(
        rows=rows,
        sknf_s=sknf_s,
        sknf_c=sknf_c,
        minimized_s=minimized_s,
        minimized_c=minimized_c,
        circuit_s=circuit_s,
        circuit_c=circuit_c,
    )


def render_part1(result: Part1Result) -> str:
    table = render_table(
        headers=("X1", "X2", "X3", "S", "C"),
        rows=((row.x1, row.x2, row.x3, row.s, row.c) for row in result.rows),
    )

    lines = [
        "Task 1. One-bit full adder (PCNF)",
        "Truth table:",
        table,
        "Canonical forms (PCNF):",
        f"S = {result.sknf_s}",
        f"C = {result.sknf_c}",
        "Minimized expressions:",
        f"S = {result.minimized_s.expression}",
        f"C = {result.minimized_c.expression}",
        "Circuit (NOT, AND, OR):",
        "For S:",
        render_circuit(result.circuit_s),
        "For C:",
        render_circuit(result.circuit_c),
    ]
    return "\n".join(lines)

