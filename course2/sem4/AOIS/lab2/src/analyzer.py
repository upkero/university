from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from src.canonical_forms import CanonicalForms, build_canonical_forms
from src.derivatives import Derivative, build_all_derivatives, find_fictitious_variables
from src.expression_parser import ParsedExpression, parse_expression
from src.karnaugh import KarnaughResult, minimize_by_karnaugh
from src.minimization import (
    MinimizationResult,
    minimize_by_calculation,
    minimize_by_calculation_table,
)
from src.post_classes import PostClasses, determine_post_classes
from src.truth_table import TruthTable, build_truth_table
from src.zhegalkin import ZhegalkinPolynomial, build_zhegalkin_polynomial


@dataclass(frozen=True)
class FullAnalysis:
    parsed: ParsedExpression
    table: TruthTable
    canonical: CanonicalForms
    post_classes: PostClasses
    zhegalkin: ZhegalkinPolynomial
    fictitious_variables: Tuple[str, ...]
    derivatives: Tuple[Derivative, ...]
    calculation_minimization: MinimizationResult
    calculation_table_minimization: MinimizationResult
    karnaugh_minimization: KarnaughResult


def analyze_expression(source: str) -> FullAnalysis:
    parsed = parse_expression(source)
    table = build_truth_table(parsed)
    canonical = build_canonical_forms(table)
    zhegalkin = build_zhegalkin_polynomial(table)
    post_classes = determine_post_classes(table)
    fictitious_variables = find_fictitious_variables(table)
    derivatives = build_all_derivatives(table, max_order=4)
    calculation_minimization = minimize_by_calculation(table)
    calculation_table_minimization = minimize_by_calculation_table(table)
    karnaugh_minimization = minimize_by_karnaugh(table)
    return FullAnalysis(
        parsed=parsed,
        table=table,
        canonical=canonical,
        post_classes=post_classes,
        zhegalkin=zhegalkin,
        fictitious_variables=fictitious_variables,
        derivatives=derivatives,
        calculation_minimization=calculation_minimization,
        calculation_table_minimization=calculation_table_minimization,
        karnaugh_minimization=karnaugh_minimization,
    )

