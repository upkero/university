from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Tuple

from src.truth_table import TruthTable


@dataclass(frozen=True)
class ZhegalkinPolynomial:
    coefficients: Tuple[int, ...]
    monomials: Tuple[str, ...]
    expression: str


def zhegalkin_coefficients(table: TruthTable) -> Tuple[int, ...]:
    variables_count = len(table.variables)
    coefficients = list(table.vector)
    for bit in range(variables_count):
        bit_mask = 1 << bit
        for mask in range(1 << variables_count):
            if mask & bit_mask:
                coefficients[mask] ^= coefficients[mask ^ bit_mask]
    return tuple(coefficients)


def _mask_for_variables(variables_count: int, indexes: Tuple[int, ...]) -> int:
    mask = 0
    for index in indexes:
        mask |= 1 << (variables_count - 1 - index)
    return mask


def _monomial_from_mask(mask: int, variables: Tuple[str, ...]) -> str:
    if mask == 0:
        return "1"
    parts: list[str] = []
    dimension = len(variables)
    for index, variable in enumerate(variables):
        bit = 1 << (dimension - 1 - index)
        if mask & bit:
            parts.append(variable)
    return "*".join(parts)


def build_zhegalkin_polynomial(table: TruthTable) -> ZhegalkinPolynomial:
    variables_count = len(table.variables)
    coefficients = zhegalkin_coefficients(table)

    masks_in_readable_order: list[int] = [0]
    for degree in range(1, variables_count + 1):
        for variable_indexes in combinations(range(variables_count), degree):
            masks_in_readable_order.append(
                _mask_for_variables(variables_count, variable_indexes)
            )

    monomials = tuple(
        _monomial_from_mask(mask, table.variables)
        for mask in masks_in_readable_order
        if coefficients[mask] == 1
    )
    expression = " ^ ".join(monomials) if monomials else "0"
    return ZhegalkinPolynomial(
        coefficients=coefficients,
        monomials=monomials,
        expression=expression,
    )

