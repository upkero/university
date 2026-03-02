from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

from src.canonical_forms import build_canonical_forms
from src.truth_table import TruthTable


@dataclass(frozen=True)
class Implicant:
    pattern: str
    minterms: Tuple[int, ...]

    @property
    def literals_count(self) -> int:
        return sum(1 for bit in self.pattern if bit != "-")


@dataclass(frozen=True)
class GluingRecord:
    left_pattern: str
    right_pattern: str
    result_pattern: str


@dataclass(frozen=True)
class GluingStage:
    input_patterns: Tuple[str, ...]
    records: Tuple[GluingRecord, ...]
    output_patterns: Tuple[str, ...]


@dataclass(frozen=True)
class RedundancyCheck:
    implicant: str
    removed: bool
    reason: str


@dataclass(frozen=True)
class PrimeImplicantChart:
    minterms: Tuple[int, ...]
    implicants: Tuple[str, ...]
    matrix: Tuple[Tuple[int, ...], ...]


@dataclass(frozen=True)
class MinimizationResult:
    method_name: str
    initial_sdnf: str
    stages: Tuple[GluingStage, ...]
    prime_implicants: Tuple[str, ...]
    selected_implicants: Tuple[str, ...]
    expression: str
    redundancy_checks: Tuple[RedundancyCheck, ...] = tuple()
    chart: PrimeImplicantChart | None = None


def _pattern_from_minterm(minterm: int, dimension: int) -> str:
    return format(minterm, f"0{dimension}b")


def _combine_patterns(left: str, right: str) -> str | None:
    diff_count = 0
    combined: list[str] = []
    for left_bit, right_bit in zip(left, right):
        if left_bit == right_bit:
            combined.append(left_bit)
            continue
        if left_bit == "-" or right_bit == "-":
            return None
        diff_count += 1
        combined.append("-")
        if diff_count > 1:
            return None
    if diff_count != 1:
        return None
    return "".join(combined)


def implicant_covers_minterm(pattern: str, minterm: int, dimension: int) -> bool:
    minterm_pattern = _pattern_from_minterm(minterm, dimension)
    return all(bit == "-" or bit == minterm_bit for bit, minterm_bit in zip(pattern, minterm_pattern))


def _merge_implicants(implicants: Iterable[Implicant]) -> List[Implicant]:
    merged: Dict[str, set[int]] = {}
    for implicant in implicants:
        merged.setdefault(implicant.pattern, set()).update(implicant.minterms)
    result = [
        Implicant(pattern=pattern, minterms=tuple(sorted(minterms)))
        for pattern, minterms in merged.items()
    ]
    result.sort(key=lambda item: (item.literals_count, item.pattern))
    return result


def _generate_prime_implicants(
    dimension: int, minterms: Sequence[int]
) -> Tuple[Tuple[GluingStage, ...], Tuple[Implicant, ...]]:
    current = _merge_implicants(
        Implicant(_pattern_from_minterm(minterm, dimension), (minterm,))
        for minterm in sorted(set(minterms))
    )

    stages: list[GluingStage] = []
    prime_implicants: Dict[str, set[int]] = {}

    while current:
        groups: Dict[int, List[Implicant]] = {}
        for implicant in current:
            ones_count = implicant.pattern.count("1")
            groups.setdefault(ones_count, []).append(implicant)

        combined_patterns: set[str] = set()
        next_implicants: list[Implicant] = []
        records: Dict[Tuple[str, str, str], GluingRecord] = {}

        all_group_indexes = sorted(groups.keys())
        for group_index in all_group_indexes:
            left_group = groups.get(group_index, [])
            right_group = groups.get(group_index + 1, [])
            for left_implicant in left_group:
                for right_implicant in right_group:
                    combined_pattern = _combine_patterns(
                        left_implicant.pattern, right_implicant.pattern
                    )
                    if combined_pattern is None:
                        continue
                    combined_patterns.add(left_implicant.pattern)
                    combined_patterns.add(right_implicant.pattern)
                    merged_minterms = tuple(
                        sorted(set(left_implicant.minterms) | set(right_implicant.minterms))
                    )
                    next_implicants.append(
                        Implicant(pattern=combined_pattern, minterms=merged_minterms)
                    )
                    record_key = (
                        min(left_implicant.pattern, right_implicant.pattern),
                        max(left_implicant.pattern, right_implicant.pattern),
                        combined_pattern,
                    )
                    records[record_key] = GluingRecord(
                        left_pattern=record_key[0],
                        right_pattern=record_key[1],
                        result_pattern=combined_pattern,
                    )

        for implicant in current:
            if implicant.pattern not in combined_patterns:
                prime_implicants.setdefault(implicant.pattern, set()).update(
                    implicant.minterms
                )

        if not next_implicants:
            break

        next_merged = _merge_implicants(next_implicants)
        stage = GluingStage(
            input_patterns=tuple(item.pattern for item in current),
            records=tuple(records[key] for key in sorted(records.keys())),
            output_patterns=tuple(item.pattern for item in next_merged),
        )
        stages.append(stage)
        current = next_merged

    prime_result = _merge_implicants(
        Implicant(pattern=pattern, minterms=tuple(sorted(minterms)))
        for pattern, minterms in prime_implicants.items()
    )
    return tuple(stages), tuple(prime_result)


def _pattern_to_term(pattern: str, variables: Tuple[str, ...]) -> str:
    literals: list[str] = []
    for bit, variable in zip(pattern, variables):
        if bit == "1":
            literals.append(variable)
        elif bit == "0":
            literals.append(f"!{variable}")
    if not literals:
        return "1"
    if len(literals) == 1:
        return literals[0]
    return f"({'&'.join(literals)})"


def _patterns_to_expression(patterns: Sequence[str], variables: Tuple[str, ...]) -> str:
    if not patterns:
        return "0"
    terms = [_pattern_to_term(pattern, variables) for pattern in patterns]
    return "|".join(terms)


def _covers_all_minterms(
    implicant_patterns: Sequence[str], minterms: Sequence[int], dimension: int
) -> bool:
    for minterm in minterms:
        if not any(
            implicant_covers_minterm(pattern, minterm, dimension)
            for pattern in implicant_patterns
        ):
            return False
    return True


def _build_prime_implicant_chart(
    dimension: int, prime_implicants: Sequence[str], minterms: Sequence[int]
) -> PrimeImplicantChart:
    matrix = tuple(
        tuple(
            int(implicant_covers_minterm(implicant, minterm, dimension))
            for minterm in minterms
        )
        for implicant in prime_implicants
    )
    return PrimeImplicantChart(
        minterms=tuple(minterms),
        implicants=tuple(prime_implicants),
        matrix=matrix,
    )


def minimize_by_calculation(table: TruthTable) -> MinimizationResult:
    canonical = build_canonical_forms(table)
    minterms = tuple(canonical.sdnf_numeric)
    dimension = len(table.variables)
    if not minterms:
        return MinimizationResult(
            method_name="calculation",
            initial_sdnf=canonical.sdnf,
            stages=tuple(),
            prime_implicants=tuple(),
            selected_implicants=tuple(),
            expression="0",
        )

    stages, prime_implicants = _generate_prime_implicants(dimension, minterms)
    selected = [item.pattern for item in prime_implicants]
    checks: list[RedundancyCheck] = []
    for pattern in list(selected):
        others = [item for item in selected if item != pattern]
        removable = _covers_all_minterms(others, minterms, dimension)
        checks.append(
            RedundancyCheck(
                implicant=pattern,
                removed=removable,
                reason="covered by other implicants"
                if removable
                else "required for at least one minterm",
            )
        )
        if removable:
            selected.remove(pattern)

    selected.sort(key=lambda item: (sum(bit != "-" for bit in item), item))

    return MinimizationResult(
        method_name="calculation",
        initial_sdnf=canonical.sdnf,
        stages=stages,
        prime_implicants=tuple(item.pattern for item in prime_implicants),
        selected_implicants=tuple(selected),
        expression=_patterns_to_expression(selected, table.variables),
        redundancy_checks=tuple(checks),
    )


def minimize_by_calculation_table(table: TruthTable) -> MinimizationResult:
    canonical = build_canonical_forms(table)
    minterms = tuple(canonical.sdnf_numeric)
    dimension = len(table.variables)
    if not minterms:
        empty_chart = PrimeImplicantChart(tuple(), tuple(), tuple())
        return MinimizationResult(
            method_name="calculation_table",
            initial_sdnf=canonical.sdnf,
            stages=tuple(),
            prime_implicants=tuple(),
            selected_implicants=tuple(),
            expression="0",
            chart=empty_chart,
        )

    stages, prime_implicants = _generate_prime_implicants(dimension, minterms)
    prime_patterns = [item.pattern for item in prime_implicants]
    prime_patterns.sort(key=lambda item: (sum(bit != "-" for bit in item), item))

    chart = _build_prime_implicant_chart(dimension, prime_patterns, minterms)
    selected: set[str] = set()

    for column_index, minterm in enumerate(chart.minterms):
        covering = [
            chart.implicants[row_index]
            for row_index, row in enumerate(chart.matrix)
            if row[column_index] == 1
        ]
        if len(covering) == 1:
            selected.add(covering[0])

    uncovered = set(minterms)
    for pattern in selected:
        for minterm in minterms:
            if implicant_covers_minterm(pattern, minterm, dimension):
                uncovered.discard(minterm)

    while uncovered:
        candidates = [pattern for pattern in chart.implicants if pattern not in selected]
        scored_candidates = []
        for pattern in candidates:
            covered = {
                minterm
                for minterm in uncovered
                if implicant_covers_minterm(pattern, minterm, dimension)
            }
            scored_candidates.append((len(covered), -sum(bit != "-" for bit in pattern), pattern, covered))
        scored_candidates.sort(reverse=True)
        best_cover_count, _, best_pattern, covered = scored_candidates[0]
        if best_cover_count == 0:
            break
        selected.add(best_pattern)
        uncovered -= covered

    selected_patterns = sorted(
        selected, key=lambda item: (sum(bit != "-" for bit in item), item)
    )
    return MinimizationResult(
        method_name="calculation_table",
        initial_sdnf=canonical.sdnf,
        stages=stages,
        prime_implicants=tuple(prime_patterns),
        selected_implicants=tuple(selected_patterns),
        expression=_patterns_to_expression(selected_patterns, table.variables),
        chart=chart,
    )

