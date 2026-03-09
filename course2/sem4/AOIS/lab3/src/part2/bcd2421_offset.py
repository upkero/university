from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from src.common import Gate, evaluate_gate_network, index_to_assignment, render_table


INPUT_VARIABLES = ("A3", "A2", "A1", "A0", "B3", "B2", "B1", "B0")
OUTPUT_VARIABLES = ("T3", "T2", "T1", "T0", "U3", "U2", "U1", "U0", "OVF")


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

REVERSE_CODE_2421 = {code: digit for digit, code in CODE_2421.items()}
OFFSET_N = 6


@dataclass(frozen=True)
class Part2TruthRow:
    a3: int
    a2: int
    a1: int
    a0: int
    b3: int
    b2: int
    b1: int
    b0: int
    digit_a: int | None
    digit_b: int | None
    total: int | None
    offset: int | None
    tens_digit: int | None
    units_digit: int | None
    t3: int | None
    t2: int | None
    t1: int | None
    t0: int | None
    u3: int | None
    u2: int | None
    u1: int | None
    u0: int | None
    ovf: int | None


@dataclass(frozen=True)
class Part2Netlist:
    equations: tuple[str, ...]
    gates: tuple[Gate, ...]
    outputs: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class Part2Result:
    rows: tuple[Part2TruthRow, ...]
    netlist: Part2Netlist


class _NetlistBuilder:
    def __init__(self) -> None:
        self._counts: Counter[str] = Counter()
        self._gates: list[Gate] = []

    def add(self, gate_type: str, inputs: tuple[str, ...], output: str) -> str:
        self._counts[gate_type] += 1
        self._gates.append(
            Gate(
                name=f"{gate_type}{self._counts[gate_type]}",
                gate_type=gate_type,
                inputs=inputs,
                output=output,
            )
        )
        return output

    def gates(self) -> tuple[Gate, ...]:
        return tuple(self._gates)


def _render_cell(value: int | None) -> str:
    if value is None:
        return "-"
    return str(value)


def _resolve_output_source(source: str, signals: dict[str, int]) -> int:
    if source == "0":
        return 0
    if source == "1":
        return 1
    return int(bool(signals[source]))


def build_truth_rows() -> tuple[Part2TruthRow, ...]:
    rows: list[Part2TruthRow] = []
    for index in range(1 << len(INPUT_VARIABLES)):
        a3, a2, a1, a0, b3, b2, b1, b0 = index_to_assignment(index, len(INPUT_VARIABLES))
        left_code = (a3, a2, a1, a0)
        right_code = (b3, b2, b1, b0)

        digit_a = REVERSE_CODE_2421.get(left_code)
        digit_b = REVERSE_CODE_2421.get(right_code)
        if digit_a is None or digit_b is None:
            rows.append(
                Part2TruthRow(
                    a3=a3,
                    a2=a2,
                    a1=a1,
                    a0=a0,
                    b3=b3,
                    b2=b2,
                    b1=b1,
                    b0=b0,
                    digit_a=None,
                    digit_b=None,
                    total=None,
                    offset=None,
                    tens_digit=None,
                    units_digit=None,
                    t3=None,
                    t2=None,
                    t1=None,
                    t0=None,
                    u3=None,
                    u2=None,
                    u1=None,
                    u0=None,
                    ovf=None,
                )
            )
            continue

        total = digit_a + digit_b
        tens_digit, units_digit = divmod(total, 10)
        overflow = 1 if total >= 10 else 0
        offset = OFFSET_N if overflow else 0
        t3, t2, t1, t0 = CODE_2421[tens_digit]
        u3, u2, u1, u0 = CODE_2421[units_digit]

        rows.append(
            Part2TruthRow(
                a3=a3,
                a2=a2,
                a1=a1,
                a0=a0,
                b3=b3,
                b2=b2,
                b1=b1,
                b0=b0,
                digit_a=digit_a,
                digit_b=digit_b,
                total=total,
                offset=offset,
                tens_digit=tens_digit,
                units_digit=units_digit,
                t3=t3,
                t2=t2,
                t1=t1,
                t0=t0,
                u3=u3,
                u2=u2,
                u1=u1,
                u0=u0,
                ovf=overflow,
            )
        )
    return tuple(rows)


def build_structural_netlist() -> Part2Netlist:
    builder = _NetlistBuilder()

    ad31 = builder.add("AND", ("A3", "A1"), "AD31")
    da3 = builder.add("AND", ("A3", "A2", "A1"), "DA3")
    da2 = builder.add("XOR", ("A2", ad31), "DA2")
    da1 = builder.add("XOR", ("A1", "A3"), "DA1")
    da0 = "A0"

    bd31 = builder.add("AND", ("B3", "B1"), "BD31")
    db3 = builder.add("AND", ("B3", "B2", "B1"), "DB3")
    db2 = builder.add("XOR", ("B2", bd31), "DB2")
    db1 = builder.add("XOR", ("B1", "B3"), "DB1")
    db0 = "B0"

    s0 = builder.add("XOR", (da0, db0), "S0")
    c1 = builder.add("AND", (da0, db0), "C1")

    p1 = builder.add("XOR", (da1, db1), "P1")
    s1 = builder.add("XOR", (p1, c1), "S1")
    g1 = builder.add("AND", (da1, db1), "G1")
    c1p1 = builder.add("AND", (c1, p1), "C1P1")
    c2 = builder.add("OR", (g1, c1p1), "C2")

    p2 = builder.add("XOR", (da2, db2), "P2")
    s2 = builder.add("XOR", (p2, c2), "S2")
    g2 = builder.add("AND", (da2, db2), "G2")
    c2p2 = builder.add("AND", (c2, p2), "C2P2")
    c3 = builder.add("OR", (g2, c2p2), "C3")

    p3 = builder.add("XOR", (da3, db3), "P3")
    s3 = builder.add("XOR", (p3, c3), "S3")
    g3 = builder.add("AND", (da3, db3), "G3")
    c3p3 = builder.add("AND", (c3, p3), "C3P3")
    c4 = builder.add("OR", (g3, c3p3), "C4")

    s3s2 = builder.add("AND", (s3, s2), "S3S2")
    s3s1 = builder.add("AND", (s3, s1), "S3S1")
    k1 = builder.add("OR", (c4, s3s2), "K1")
    k = builder.add("OR", (k1, s3s1), "K")

    z0 = s0
    z1 = builder.add("XOR", (s1, k), "Z1")
    c5 = builder.add("AND", (s1, k), "C5")
    pz2 = builder.add("XOR", (s2, k), "PZ2")
    z2 = builder.add("XOR", (pz2, c5), "Z2")
    s2_or_s1 = builder.add("OR", (s2, s1), "S2_OR_S1")
    c6 = builder.add("AND", (k, s2_or_s1), "C6")
    z3 = builder.add("XOR", (s3, c6), "Z3")

    z1_or_z0 = builder.add("OR", (z1, z0), "Z1_OR_Z0")
    u3a = builder.add("AND", (z2, z1_or_z0), "U3A")
    u3 = builder.add("OR", (z3, u3a), "U3")
    u1 = builder.add("XOR", (z1, u3), "U1")
    nz1 = builder.add("NOT", (z1,), "NZ1")
    u3_nz1 = builder.add("AND", (u3, nz1), "U3_NZ1")
    u2 = builder.add("XOR", (z2, u3_nz1), "U2")
    u0 = z0

    equations = (
        "DA3 = A3*A2*A1; DA2 = A2 xor (A3*A1); DA1 = A1 xor A3; DA0 = A0",
        "DB3 = B3*B2*B1; DB2 = B2 xor (B3*B1); DB1 = B1 xor B3; DB0 = B0",
        "Ripple adder: S0..S3, C1..C4 for decoded 8421 digits",
        "K = C4 + S3*S2 + S3*S1",
        "Z0 = S0; Z1 = S1 xor K; Z2 = (S2 xor K) xor (S1*K); Z3 = S3 xor (K*(S2 + S1))",
        "U3 = Z3 + Z2*(Z1 + Z0); U2 = Z2 xor (U3*!Z1); U1 = Z1 xor U3; U0 = Z0",
        "T3 = 0; T2 = 0; T1 = 0; T0 = K; OVF = K",
    )
    outputs = (
        ("T3", "0"),
        ("T2", "0"),
        ("T1", "0"),
        ("T0", k),
        ("U3", u3),
        ("U2", u2),
        ("U1", u1),
        ("U0", u0),
        ("OVF", k),
    )
    return Part2Netlist(equations=equations, gates=builder.gates(), outputs=outputs)


def evaluate_structural_outputs(netlist: Part2Netlist, assignment: dict[str, int]) -> dict[str, int]:
    signals = evaluate_gate_network(netlist.gates, assignment)
    return {
        output_name: _resolve_output_source(source, signals)
        for output_name, source in netlist.outputs
    }


def solve_part2() -> Part2Result:
    return Part2Result(rows=build_truth_rows(), netlist=build_structural_netlist())


def _render_netlist(netlist: Part2Netlist) -> str:
    lines = [
        f"{gate.name}: {gate.gate_type}({', '.join(gate.inputs)}) -> {gate.output}"
        for gate in netlist.gates
    ]
    for output_name, source in netlist.outputs:
        lines.append(f"{output_name} = {source}")
    return "\n".join(lines)


def render_part2(result: Part2Result) -> str:
    valid_rows = [
        row for row in result.rows if row.digit_a is not None and row.digit_b is not None
    ]
    table = render_table(
        headers=(
            "A3",
            "A2",
            "A1",
            "A0",
            "B3",
            "B2",
            "B1",
            "B0",
            "a",
            "b",
            "a+b",
            "+n",
            "T",
            "U",
            "T3",
            "T2",
            "T1",
            "T0",
            "U3",
            "U2",
            "U1",
            "U0",
            "OVF",
        ),
        rows=(
            (
                row.a3,
                row.a2,
                row.a1,
                row.a0,
                row.b3,
                row.b2,
                row.b1,
                row.b0,
                _render_cell(row.digit_a),
                _render_cell(row.digit_b),
                _render_cell(row.total),
                _render_cell(row.offset),
                _render_cell(row.tens_digit),
                _render_cell(row.units_digit),
                _render_cell(row.t3),
                _render_cell(row.t2),
                _render_cell(row.t1),
                _render_cell(row.t0),
                _render_cell(row.u3),
                _render_cell(row.u2),
                _render_cell(row.u1),
                _render_cell(row.u0),
                _render_cell(row.ovf),
            )
            for row in valid_rows
        ),
    )

    gate_counts = Counter(gate.gate_type for gate in result.netlist.gates)
    gate_summary = ", ".join(
        f"{gate_type}={gate_counts.get(gate_type, 0)}"
        for gate_type in ("XOR", "AND", "OR", "NOT")
        if gate_counts.get(gate_type, 0) > 0
    )

    lines = [
        "Task 2. 2421-code adder for two one-digit decimal numbers with offset n = 6",
        "Truth table for valid 2421 combinations (the remaining 156 combinations are don't care):",
        table,
        "Minimized functions (structural shared XOR/AND/OR implementation):",
        "Structural equations (shared XOR/AND/OR network):",
    ]
    lines.extend(result.netlist.equations)
    lines.extend(
        [
            f"Gate count: {gate_summary}",
            "Shared circuit:",
            _render_netlist(result.netlist),
            "Notes:",
            "- correction K implements decimal carry and +6 adjustment;",
            "- T3..T0 encode the tens digit in 2421;",
            "- U3..U0 encode the units digit in 2421;",
            "- OVF equals the carry into the tens digit.",
        ]
    )
    return "\n".join(lines)
