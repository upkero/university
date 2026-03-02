from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, Tuple

from src.canonical_forms import build_canonical_forms
from src.truth_table import TruthTable, truth_table_from_vector


@dataclass(frozen=True)
class Derivative:
    by_variables: Tuple[str, ...]
    order: int
    vector: Tuple[int, ...]
    sdnf: str
    numeric_form: Tuple[int, ...]
    index_vector: str
    index_number: int


def find_fictitious_variables(table: TruthTable) -> Tuple[str, ...]:
    dimension = len(table.variables)
    if dimension == 0:
        return tuple()

    fictitious: list[str] = []
    for variable_index, variable in enumerate(table.variables):
        bit = 1 << (dimension - 1 - variable_index)
        is_fictitious = True
        for index in range(1 << dimension):
            if index & bit:
                continue
            if table.vector[index] != table.vector[index | bit]:
                is_fictitious = False
                break
        if is_fictitious:
            fictitious.append(variable)
    return tuple(fictitious)


def _toggle_masks(bits: Iterable[int]) -> Tuple[int, ...]:
    masks = [0]
    for bit in bits:
        masks.extend(mask | bit for mask in list(masks))
    return tuple(masks)


def boolean_derivative(table: TruthTable, by_variables: Tuple[str, ...]) -> Derivative:
    if not by_variables:
        raise ValueError("At least one variable is required for differentiation.")

    dimension = len(table.variables)
    variable_to_mask: Dict[str, int] = {
        variable: 1 << (dimension - 1 - index)
        for index, variable in enumerate(table.variables)
    }
    unknown = [variable for variable in by_variables if variable not in variable_to_mask]
    if unknown:
        raise ValueError(f"Unknown variable(s) for derivative: {unknown}")

    derivative_masks = _toggle_masks(variable_to_mask[variable] for variable in by_variables)
    derivative_vector = []
    for index in range(1 << dimension):
        value = 0
        for mask in derivative_masks:
            value ^= table.vector[index ^ mask]
        derivative_vector.append(value)

    derivative_table = truth_table_from_vector(table.variables, derivative_vector)
    canonical = build_canonical_forms(derivative_table)
    return Derivative(
        by_variables=by_variables,
        order=len(by_variables),
        vector=tuple(derivative_vector),
        sdnf=canonical.sdnf,
        numeric_form=canonical.sdnf_numeric,
        index_vector=canonical.index_vector,
        index_number=canonical.index_number,
    )


def build_all_derivatives(table: TruthTable, max_order: int = 4) -> Tuple[Derivative, ...]:
    max_supported_order = min(max_order, len(table.variables))
    derivatives: list[Derivative] = []
    for order in range(1, max_supported_order + 1):
        for variables_group in combinations(table.variables, order):
            derivatives.append(boolean_derivative(table, variables_group))
    return tuple(derivatives)

