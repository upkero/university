from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from src.truth_table import TruthRow, TruthTable


@dataclass(frozen=True)
class CanonicalForms:
    sdnf: str
    sknf: str
    sdnf_numeric: Tuple[int, ...]
    sknf_numeric: Tuple[int, ...]
    index_vector: str
    index_number: int


def _build_sdnf_term(variables: Tuple[str, ...], row: TruthRow) -> str:
    if not variables:
        return "1"
    literals = [
        variable if value == 1 else f"!{variable}"
        for variable, value in zip(variables, row.assignment)
    ]
    if len(literals) == 1:
        return literals[0]
    return f"({'&'.join(literals)})"


def _build_sknf_term(variables: Tuple[str, ...], row: TruthRow) -> str:
    if not variables:
        return "0"
    literals = [
        variable if value == 0 else f"!{variable}"
        for variable, value in zip(variables, row.assignment)
    ]
    if len(literals) == 1:
        return literals[0]
    return f"({'|'.join(literals)})"


def build_canonical_forms(table: TruthTable) -> CanonicalForms:
    sdnf_rows = tuple(row for row in table.rows if row.result == 1)
    sknf_rows = tuple(row for row in table.rows if row.result == 0)

    sdnf_terms = tuple(_build_sdnf_term(table.variables, row) for row in sdnf_rows)
    sknf_terms = tuple(_build_sknf_term(table.variables, row) for row in sknf_rows)

    sdnf = "|".join(sdnf_terms) if sdnf_terms else "0"
    sknf = "&".join(sknf_terms) if sknf_terms else "1"

    index_vector = "".join(str(row.result) for row in table.rows)
    index_number = int(index_vector, 2) if index_vector else 0

    return CanonicalForms(
        sdnf=sdnf,
        sknf=sknf,
        sdnf_numeric=tuple(row.index for row in sdnf_rows),
        sknf_numeric=tuple(row.index for row in sknf_rows),
        index_vector=index_vector,
        index_number=index_number,
    )

