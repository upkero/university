from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, Iterable, Tuple

from src.expression_parser import ParsedExpression


@dataclass(frozen=True)
class TruthRow:
    assignment: Tuple[int, ...]
    result: int
    index: int


@dataclass(frozen=True)
class TruthTable:
    variables: Tuple[str, ...]
    rows: Tuple[TruthRow, ...]

    @property
    def vector(self) -> Tuple[int, ...]:
        return tuple(row.result for row in self.rows)

    @property
    def dimension(self) -> int:
        return len(self.variables)


def assignment_to_index(assignment: Iterable[int]) -> int:
    index = 0
    for value in assignment:
        index = (index << 1) | int(bool(value))
    return index


def index_to_assignment(index: int, dimension: int) -> Tuple[int, ...]:
    if dimension == 0:
        return tuple()
    values: list[int] = []
    for bit in range(dimension - 1, -1, -1):
        values.append((index >> bit) & 1)
    return tuple(values)


def build_truth_table(parsed_expression: ParsedExpression) -> TruthTable:
    variables = parsed_expression.variables
    dimension = len(variables)
    rows: list[TruthRow] = []
    for values in product((0, 1), repeat=dimension):
        assignment_dict: Dict[str, int] = dict(zip(variables, values))
        result = parsed_expression.root.evaluate(assignment_dict)
        index = assignment_to_index(values)
        rows.append(TruthRow(values, result, index))
    if dimension == 0:
        result = parsed_expression.root.evaluate({})
        rows = [TruthRow(tuple(), result, 0)]
    return TruthTable(variables=variables, rows=tuple(rows))


def truth_table_from_vector(variables: Tuple[str, ...], vector: Iterable[int]) -> TruthTable:
    values = tuple(int(bool(item)) for item in vector)
    expected_size = 1 << len(variables)
    if len(values) != expected_size:
        raise ValueError(
            f"Vector size must be {expected_size} for variables {variables}, got {len(values)}."
        )
    rows = tuple(
        TruthRow(index_to_assignment(index, len(variables)), result, index)
        for index, result in enumerate(values)
    )
    return TruthTable(variables=variables, rows=rows)

