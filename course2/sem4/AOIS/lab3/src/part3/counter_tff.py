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


STATE_VARIABLES = ("Q2", "Q1", "Q0")
EXCITATION_VARIABLES = ("T0", "T1", "T2")


@dataclass(frozen=True)
class Part3TransitionRow:
    q2: int
    q1: int
    q0: int
    q2_next: int
    q1_next: int
    q0_next: int
    t0: int
    t1: int
    t2: int


@dataclass(frozen=True)
class Part3Result:
    rows: tuple[Part3TransitionRow, ...]
    minimized_t: tuple[tuple[str, MinimizedSOP], ...]
    circuits: tuple[tuple[str, Circuit], ...]


def _next_state(index: int) -> int:
    return (index + 1) % 8


def build_transition_rows() -> tuple[Part3TransitionRow, ...]:
    rows: list[Part3TransitionRow] = []
    for state_index in range(8):
        q2, q1, q0 = index_to_assignment(state_index, 3)
        next_index = _next_state(state_index)
        q2_next, q1_next, q0_next = index_to_assignment(next_index, 3)

        t0 = q0 ^ q0_next
        t1 = q1 ^ q1_next
        t2 = q2 ^ q2_next

        rows.append(
            Part3TransitionRow(
                q2=q2,
                q1=q1,
                q0=q0,
                q2_next=q2_next,
                q1_next=q1_next,
                q0_next=q0_next,
                t0=t0,
                t1=t1,
                t2=t2,
            )
        )
    return tuple(rows)


def solve_part3() -> Part3Result:
    rows = build_transition_rows()

    minimized_t: list[tuple[str, MinimizedSOP]] = []
    circuits: list[tuple[str, Circuit]] = []

    for excitation in EXCITATION_VARIABLES:
        ones = [
            index
            for index, row in enumerate(rows)
            if getattr(row, excitation.lower()) == 1
        ]
        minimized = minimize_sop(STATE_VARIABLES, ones)
        circuit = build_circuit_from_patterns(excitation, STATE_VARIABLES, minimized.patterns)

        minimized_t.append((excitation, minimized))
        circuits.append((excitation, circuit))

    return Part3Result(rows=rows, minimized_t=tuple(minimized_t), circuits=tuple(circuits))


def render_part3(result: Part3Result) -> str:
    table = render_table(
        headers=("Q2", "Q1", "Q0", "Q2+", "Q1+", "Q0+", "T0", "T1", "T2"),
        rows=(
            (
                row.q2,
                row.q1,
                row.q0,
                row.q2_next,
                row.q1_next,
                row.q0_next,
                row.t0,
                row.t1,
                row.t2,
            )
            for row in result.rows
        ),
    )

    lines = [
        "Task 3. Binary accumulative counter (mod 8) on T flip-flops",
        "State transition table:",
        table,
        "Excitation functions (minimized):",
    ]

    for excitation, minimized in result.minimized_t:
        lines.append(f"{excitation} = {minimized.expression}")

    lines.append("Circuit (NOT, AND, OR):")
    for excitation, circuit in result.circuits:
        lines.append(f"For {excitation}:")
        lines.append(render_circuit(circuit))

    return "\n".join(lines)

