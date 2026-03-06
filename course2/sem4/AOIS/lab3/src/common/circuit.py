from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Gate:
    name: str
    gate_type: str
    inputs: tuple[str, ...]
    output: str


@dataclass(frozen=True)
class Circuit:
    output_name: str
    output_source: str
    gates: tuple[Gate, ...]


def build_circuit_from_patterns(
    output_name: str,
    variables: Sequence[str],
    patterns: Iterable[str],
) -> Circuit:
    pattern_list = list(patterns)
    if not pattern_list:
        return Circuit(output_name=output_name, output_source="0", gates=tuple())

    if len(pattern_list) == 1 and set(pattern_list[0]) == {"-"}:
        return Circuit(output_name=output_name, output_source="1", gates=tuple())

    gates: list[Gate] = []
    not_count = 0
    and_count = 0
    or_count = 0

    negated_signal_by_var: dict[str, str] = {}
    for var_index, variable in enumerate(variables):
        need_negation = any(pattern[var_index] == "0" for pattern in pattern_list)
        if need_negation:
            not_count += 1
            signal = f"n{variable}"
            gates.append(
                Gate(
                    name=f"NOT{not_count}",
                    gate_type="NOT",
                    inputs=(variable,),
                    output=signal,
                )
            )
            negated_signal_by_var[variable] = signal

    term_signals: list[str] = []
    for pattern in pattern_list:
        literal_signals: list[str] = []
        for symbol, variable in zip(pattern, variables):
            if symbol == "-":
                continue
            if symbol == "1":
                literal_signals.append(variable)
            else:
                literal_signals.append(negated_signal_by_var[variable])

        if not literal_signals:
            term_signals = ["1"]
            break
        if len(literal_signals) == 1:
            term_signals.append(literal_signals[0])
            continue

        and_count += 1
        term_output = f"t{and_count}"
        gates.append(
            Gate(
                name=f"AND{and_count}",
                gate_type="AND",
                inputs=tuple(literal_signals),
                output=term_output,
            )
        )
        term_signals.append(term_output)

    if term_signals == ["1"]:
        return Circuit(output_name=output_name, output_source="1", gates=tuple(gates))

    if len(term_signals) == 1:
        return Circuit(output_name=output_name, output_source=term_signals[0], gates=tuple(gates))

    or_count += 1
    gates.append(
        Gate(
            name=f"OR{or_count}",
            gate_type="OR",
            inputs=tuple(term_signals),
            output=output_name,
        )
    )
    return Circuit(output_name=output_name, output_source=output_name, gates=tuple(gates))


def render_circuit(circuit: Circuit) -> str:
    lines: list[str] = []
    if not circuit.gates:
        lines.append(f"{circuit.output_name} = {circuit.output_source}")
        return "\n".join(lines)

    for gate in circuit.gates:
        joined_inputs = ", ".join(gate.inputs)
        lines.append(f"{gate.name}: {gate.gate_type}({joined_inputs}) -> {gate.output}")

    if circuit.output_source != circuit.output_name:
        lines.append(f"{circuit.output_name} = {circuit.output_source}")

    return "\n".join(lines)

