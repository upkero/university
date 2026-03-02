from __future__ import annotations

from dataclasses import dataclass

from src.truth_table import TruthTable
from src.zhegalkin import zhegalkin_coefficients


@dataclass(frozen=True)
class PostClasses:
    t0: bool
    t1: bool
    s: bool
    m: bool
    l: bool


def _is_monotone(table: TruthTable) -> bool:
    for row_a in table.rows:
        for row_b in table.rows:
            dominates = all(
                value_a <= value_b
                for value_a, value_b in zip(row_a.assignment, row_b.assignment)
            )
            if dominates and row_a.result > row_b.result:
                return False
    return True


def _is_self_dual(table: TruthTable) -> bool:
    variables_count = len(table.variables)
    max_index = (1 << variables_count) - 1
    for row in table.rows:
        opposite_result = table.rows[max_index ^ row.index].result
        if row.result == opposite_result:
            return False
    return True


def _is_linear(table: TruthTable) -> bool:
    coefficients = zhegalkin_coefficients(table)
    for mask, coefficient in enumerate(coefficients):
        if coefficient == 1 and bin(mask).count("1") > 1:
            return False
    return True


def determine_post_classes(table: TruthTable) -> PostClasses:
    if not table.rows:
        raise ValueError("Truth table must contain at least one row.")

    t0 = table.rows[0].result == 0
    t1 = table.rows[-1].result == 1
    s = _is_self_dual(table)
    m = _is_monotone(table)
    l = _is_linear(table)
    return PostClasses(t0=t0, t1=t1, s=s, m=m, l=l)

