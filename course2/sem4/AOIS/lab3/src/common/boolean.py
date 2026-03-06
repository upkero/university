from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Literal:
    name: str
    negated: bool

    def render(self) -> str:
        return f"!{self.name}" if self.negated else self.name


@dataclass(frozen=True)
class Term:
    literals: tuple[Literal, ...]

    def render(self) -> str:
        if not self.literals:
            return "1"
        return "*".join(literal.render() for literal in self.literals)


@dataclass(frozen=True)
class MinimizedSOP:
    variables: tuple[str, ...]
    patterns: tuple[str, ...]
    terms: tuple[Term, ...]
    expression: str


def assignment_to_index(assignment: Iterable[int]) -> int:
    index = 0
    for bit in assignment:
        index = (index << 1) | int(bool(bit))
    return index


def index_to_assignment(index: int, dimension: int) -> tuple[int, ...]:
    if dimension < 0:
        raise ValueError("Dimension must be non-negative.")
    if dimension == 0:
        return tuple()
    if index < 0 or index >= (1 << dimension):
        raise ValueError("Index is out of range for the given dimension.")
    return tuple((index >> shift) & 1 for shift in range(dimension - 1, -1, -1))


def iter_assignments(variables: Sequence[str]) -> tuple[tuple[int, ...], ...]:
    return tuple(product((0, 1), repeat=len(variables)))


def build_sknf(variables: Sequence[str], values: Sequence[int]) -> str:
    dimension = len(variables)
    expected = 1 << dimension
    if len(values) != expected:
        raise ValueError(f"Expected {expected} values, got {len(values)}.")

    clauses: list[str] = []
    for index, value in enumerate(values):
        if int(bool(value)) != 0:
            continue
        bits = index_to_assignment(index, dimension)
        literals: list[str] = []
        for variable, bit in zip(variables, bits):
            literals.append(variable if bit == 0 else f"!{variable}")
        clauses.append(f"({' + '.join(literals)})")

    if not clauses:
        return "1"
    return " * ".join(clauses)


def _pattern_covers_index(pattern: str, index: int, dimension: int) -> bool:
    bits = index_to_assignment(index, dimension)
    for symbol, bit in zip(pattern, bits):
        if symbol == "-":
            continue
        if int(symbol) != bit:
            return False
    return True


def _pattern_literals_count(pattern: str) -> int:
    return sum(1 for symbol in pattern if symbol != "-")


def _pattern_sort_key(pattern: str) -> tuple[int, str]:
    return _pattern_literals_count(pattern), pattern


def _pattern_to_term(pattern: str, variables: Sequence[str]) -> Term:
    literals: list[Literal] = []
    for symbol, variable in zip(pattern, variables):
        if symbol == "1":
            literals.append(Literal(name=variable, negated=False))
        elif symbol == "0":
            literals.append(Literal(name=variable, negated=True))
    return Term(literals=tuple(literals))


def _terms_to_expression(terms: Sequence[Term]) -> str:
    if not terms:
        return "0"
    if len(terms) == 1 and not terms[0].literals:
        return "1"
    return " + ".join(term.render() for term in terms)


def _build_coverage_mask(ones: Sequence[int], covered_indexes: set[int]) -> int:
    mask = 0
    for bit_index, minterm in enumerate(ones):
        if minterm in covered_indexes:
            mask |= 1 << bit_index
    return mask


def minimize_sop(
    variables: Sequence[str],
    ones: Iterable[int],
    dont_cares: Iterable[int] = (),
) -> MinimizedSOP:
    variable_tuple = tuple(variables)
    dimension = len(variable_tuple)
    max_index = 1 << dimension

    ones_set = set(int(item) for item in ones)
    dont_care_set = set(int(item) for item in dont_cares)

    if ones_set & dont_care_set:
        raise ValueError("A minterm cannot be both 1 and don't care.")

    invalid = [item for item in ones_set | dont_care_set if item < 0 or item >= max_index]
    if invalid:
        raise ValueError(f"Indexes out of range: {sorted(invalid)}")

    if not ones_set:
        return MinimizedSOP(variable_tuple, tuple(), tuple(), "0")

    sorted_ones = tuple(sorted(ones_set))
    allowed_indexes = ones_set | dont_care_set

    candidate_patterns: list[tuple[str, int, int]] = []
    for symbols in product(("0", "1", "-"), repeat=dimension):
        pattern = "".join(symbols)
        covered = {
            index
            for index in range(max_index)
            if _pattern_covers_index(pattern, index, dimension)
        }
        if not covered:
            continue
        if not (covered & ones_set):
            continue
        if not covered.issubset(allowed_indexes):
            continue
        mask = _build_coverage_mask(sorted_ones, covered)
        candidate_patterns.append((pattern, mask, _pattern_literals_count(pattern)))

    full_mask = (1 << len(sorted_ones)) - 1
    best: dict[int, tuple[int, int, tuple[str, ...]]] = {0: (0, 0, tuple())}

    for mask in range(full_mask + 1):
        state = best.get(mask)
        if state is None:
            continue
        term_count, literal_count, selected = state
        for pattern, pattern_mask, pattern_literals in candidate_patterns:
            new_mask = mask | pattern_mask
            if new_mask == mask:
                continue
            candidate_patterns_tuple = tuple(sorted(selected + (pattern,), key=_pattern_sort_key))
            candidate = (
                term_count + 1,
                literal_count + pattern_literals,
                candidate_patterns_tuple,
            )
            current_best = best.get(new_mask)
            if current_best is None or candidate < current_best:
                best[new_mask] = candidate

    final_state = best.get(full_mask)
    if final_state is None:
        raise RuntimeError("Unable to minimize expression.")

    minimized_patterns = final_state[2]
    terms = tuple(_pattern_to_term(pattern, variable_tuple) for pattern in minimized_patterns)
    expression = _terms_to_expression(terms)
    return MinimizedSOP(
        variables=variable_tuple,
        patterns=minimized_patterns,
        terms=terms,
        expression=expression,
    )


def evaluate_sop(terms: Sequence[Term], assignment: dict[str, int]) -> int:
    if not terms:
        return 0
    for term in terms:
        is_true = True
        for literal in term.literals:
            value = int(bool(assignment[literal.name]))
            if literal.negated:
                value = 1 - value
            if value == 0:
                is_true = False
                break
        if is_true:
            return 1
    return 0

