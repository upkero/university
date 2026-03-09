from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple

from src.minimization import (
    MinimizationResult,
    implicant_covers_minterm,
    minimize_by_calculation_table,
)
from src.truth_table import TruthTable


@dataclass(frozen=True)
class KarnaughLayer:
    title: str
    row_labels: Tuple[str, ...]
    col_labels: Tuple[str, ...]
    values: Tuple[Tuple[int, ...], ...]
    indexes: Tuple[Tuple[int, ...], ...]


@dataclass(frozen=True)
class KarnaughResult:
    normal_form: str
    expression: str
    selected_implicants: Tuple[str, ...]
    layers: Tuple[KarnaughLayer, ...]
    groups: Tuple[Tuple[int, ...], ...]
    rendered_map: str

    @property
    def form_label(self) -> str:
        return "СДНФ" if self.normal_form == "sdnf" else "СКНФ"


def _gray_codes(bits: int) -> Tuple[int, ...]:
    if bits == 0:
        return (0,)
    return tuple(index ^ (index >> 1) for index in range(1 << bits))


def _gray_label(value: int, bits: int) -> str:
    if bits == 0:
        return "-"
    return format(value, f"0{bits}b")


def _index_from_assignment(values: Sequence[int]) -> int:
    index = 0
    for value in values:
        index = (index << 1) | value
    return index


def build_karnaugh_layers(table: TruthTable) -> Tuple[KarnaughLayer, ...]:
    dimension = len(table.variables)
    if dimension == 0:
        single_value = table.vector[0]
        return (
            KarnaughLayer(
                title="const",
                row_labels=("-",),
                col_labels=("-",),
                values=((single_value,),),
                indexes=((0,),),
            ),
        )

    if dimension < 5:
        layer_variables: Tuple[str, ...] = tuple()
        row_variables = table.variables[: max(0, dimension - 2)]
        col_variables = table.variables[max(0, dimension - 2) :]
    else:
        layer_variables = (table.variables[0],)
        row_variables = table.variables[1:3]
        col_variables = table.variables[3:5]

    layer_gray = _gray_codes(len(layer_variables))
    row_gray = _gray_codes(len(row_variables))
    col_gray = _gray_codes(len(col_variables))

    layers: List[KarnaughLayer] = []
    for layer_value in layer_gray:
        layer_bits = format(layer_value, f"0{len(layer_variables)}b") if layer_variables else ""
        layer_title = (
            ",".join(
                f"{variable}={bit}"
                for variable, bit in zip(layer_variables, layer_bits)
            )
            if layer_variables
            else "map"
        )
        layer_rows: list[Tuple[int, ...]] = []
        layer_indexes: list[Tuple[int, ...]] = []
        for row_value in row_gray:
            row_bits = format(row_value, f"0{len(row_variables)}b") if row_variables else ""
            row_values: list[int] = []
            row_indexes: list[int] = []
            for col_value in col_gray:
                col_bits = format(col_value, f"0{len(col_variables)}b") if col_variables else ""
                assignment_bits = [0] * dimension

                for offset, bit in enumerate(layer_bits):
                    assignment_bits[offset] = int(bit)
                for offset, bit in enumerate(row_bits):
                    assignment_bits[len(layer_variables) + offset] = int(bit)
                for offset, bit in enumerate(col_bits):
                    assignment_bits[
                        len(layer_variables) + len(row_variables) + offset
                    ] = int(bit)

                index = _index_from_assignment(assignment_bits)
                row_values.append(table.vector[index])
                row_indexes.append(index)
            layer_rows.append(tuple(row_values))
            layer_indexes.append(tuple(row_indexes))

        layers.append(
            KarnaughLayer(
                title=layer_title,
                row_labels=tuple(_gray_label(value, len(row_variables)) for value in row_gray),
                col_labels=tuple(_gray_label(value, len(col_variables)) for value in col_gray),
                values=tuple(layer_rows),
                indexes=tuple(layer_indexes),
            )
        )
    return tuple(layers)


def render_karnaugh_map(layers: Tuple[KarnaughLayer, ...]) -> str:
    lines: list[str] = []
    for layer in layers:
        lines.append(f"[{layer.title}]")
        header = "    " + " ".join(f"{label:>4}" for label in layer.col_labels)
        lines.append(header)
        for row_label, row_values in zip(layer.row_labels, layer.values):
            lines.append(f"{row_label:>3} " + " ".join(f"{value:>4}" for value in row_values))
        lines.append("")
    return "\n".join(lines).rstrip()


def _groups_from_implicants(
    table: TruthTable, minimization_result: MinimizationResult
) -> Tuple[Tuple[int, ...], ...]:
    dimension = len(table.variables)
    target_value = 1 if minimization_result.normal_form == "sdnf" else 0
    groups = []
    for implicant in minimization_result.selected_implicants:
        covered = tuple(
            index
            for index in range(1 << dimension)
            if implicant_covers_minterm(implicant, index, dimension)
            and table.vector[index] == target_value
        )
        groups.append(covered)
    return tuple(groups)


def minimize_by_karnaugh(
    table: TruthTable, normal_form: str = "sdnf"
) -> KarnaughResult:
    minimization_result = minimize_by_calculation_table(table, normal_form)
    layers = build_karnaugh_layers(table)
    rendered = render_karnaugh_map(layers)
    groups = _groups_from_implicants(table, minimization_result)
    return KarnaughResult(
        normal_form=minimization_result.normal_form,
        expression=minimization_result.expression,
        selected_implicants=minimization_result.selected_implicants,
        layers=layers,
        groups=groups,
        rendered_map=rendered,
    )


def minimize_sknf_by_karnaugh(table: TruthTable) -> KarnaughResult:
    return minimize_by_karnaugh(table, normal_form="sknf")

