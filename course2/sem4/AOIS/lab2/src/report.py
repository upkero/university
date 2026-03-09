from __future__ import annotations

from typing import Iterable

from src.analyzer import FullAnalysis
from src.minimization import MinimizationResult, PrimeImplicantChart
from src.truth_table import TruthTable


def _format_truth_table(table: TruthTable) -> str:
    if table.variables:
        header = " ".join(table.variables) + " | f"
    else:
        header = "f"
    lines = [header, "-" * len(header)]
    for row in table.rows:
        assignment = " ".join(str(value) for value in row.assignment)
        if assignment:
            lines.append(f"{assignment} | {row.result}")
        else:
            lines.append(str(row.result))
    return "\n".join(lines)


def _format_redundancy_checks(result: MinimizationResult) -> str:
    if not result.redundancy_checks:
        return "нет проверок"
    lines = []
    for check in result.redundancy_checks:
        status = "удалена" if check.removed else "оставлена"
        lines.append(f"{check.implicant}: {status} ({check.reason})")
    return "\n".join(lines)


def _format_gluing_stages(result: MinimizationResult) -> str:
    if not result.stages:
        return "склеивание не выполнялось"
    lines = []
    for stage_index, stage in enumerate(result.stages, start=1):
        lines.append(f"Этап {stage_index}:")
        if stage.records:
            for record in stage.records:
                lines.append(
                    f"  {record.left_pattern} + {record.right_pattern} -> {record.result_pattern}"
                )
        else:
            lines.append("  нет склеиваемых пар")
        lines.append(f"  Результат: {', '.join(stage.output_patterns)}")
    return "\n".join(lines)


def _format_chart(chart: PrimeImplicantChart | None) -> str:
    if chart is None:
        return "таблица не построена"
    if not chart.terms:
        return "нет единичных наборов" if chart.normal_form == "sdnf" else "нет нулевых наборов"
    header = "pat\\idx " + " ".join(f"{term:>3}" for term in chart.terms)
    lines = [header, "-" * len(header)]
    for implicant, row in zip(chart.implicants, chart.matrix):
        row_values = " ".join(f"{cell:>3}" for cell in row)
        lines.append(f"{implicant:>5} {row_values}")
    return "\n".join(lines)


def _format_post_classes(result: FullAnalysis) -> str:
    classes = result.post_classes
    return "\n".join(
        [
            f"T0: {'да' if classes.t0 else 'нет'}",
            f"T1: {'да' if classes.t1 else 'нет'}",
            f"S: {'да' if classes.s else 'нет'}",
            f"M: {'да' if classes.m else 'нет'}",
            f"L: {'да' if classes.l else 'нет'}",
        ]
    )


def _format_derivatives(result: FullAnalysis) -> str:
    if not result.derivatives:
        return "нет переменных для дифференциации"
    lines = []
    for derivative in result.derivatives:
        suffix = "".join(derivative.by_variables)
        lines.append(
            f"D_{suffix}: {derivative.sdnf} | индекс={derivative.index_number} ({derivative.index_vector})"
        )
    return "\n".join(lines)


def _format_implicants(patterns: Iterable[str]) -> str:
    values = list(patterns)
    return ", ".join(values) if values else "нет"


def _append_calculation_section(
    lines: list[str], title: str, result: MinimizationResult
) -> None:
    lines.extend(
        [
            title,
            f"Исходная {result.form_label}: {result.initial_expression}",
            _format_gluing_stages(result),
            f"Простые {result.prime_label}: {_format_implicants(result.prime_implicants)}",
            "Проверка лишних термов:",
            _format_redundancy_checks(result),
            f"Результат: {result.expression}",
            "",
        ]
    )


def _append_calculation_table_section(
    lines: list[str], title: str, result: MinimizationResult
) -> None:
    lines.extend(
        [
            title,
            f"Исходная {result.form_label}: {result.initial_expression}",
            _format_gluing_stages(result),
            "Таблица покрытия:",
            _format_chart(result.chart),
            f"Выбранные {result.selected_label}: {_format_implicants(result.selected_implicants)}",
            f"Результат: {result.expression}",
            "",
        ]
    )


def _append_karnaugh_section(lines: list[str], title: str, expression_result) -> None:
    lines.extend(
        [
            title,
            expression_result.rendered_map,
            f"Группы: {expression_result.groups}",
            f"Результат: {expression_result.expression}",
            "",
        ]
    )


def render_analysis(result: FullAnalysis) -> str:
    lines = [
        f"Формула: {result.parsed.source}",
        "",
        "Таблица истинности:",
        _format_truth_table(result.table),
        "",
        "СДНФ и СКНФ:",
        f"СДНФ: {result.canonical.sdnf}",
        f"СКНФ: {result.canonical.sknf}",
        f"Числовая форма СДНФ: {result.canonical.sdnf_numeric}",
        f"Числовая форма СКНФ: {result.canonical.sknf_numeric}",
        "",
        "Индексная форма:",
        f"Вектор: {result.canonical.index_vector}",
        f"Индекс: {result.canonical.index_number}",
        "",
        "Классы Поста:",
        _format_post_classes(result),
        "",
        "Полином Жегалкина:",
        result.zhegalkin.expression,
        "",
        "Фиктивные переменные:",
        ", ".join(result.fictitious_variables) if result.fictitious_variables else "нет",
        "",
        "Булевы производные:",
        _format_derivatives(result),
        "",
    ]
    _append_calculation_section(lines, "Минимизация СДНФ (расчетный метод):", result.calculation_minimization)
    _append_calculation_section(
        lines,
        "Минимизация СКНФ (расчетный метод):",
        result.calculation_sknf_minimization,
    )
    _append_calculation_table_section(
        lines,
        "Минимизация СДНФ (расчетно-табличный метод):",
        result.calculation_table_minimization,
    )
    _append_calculation_table_section(
        lines,
        "Минимизация СКНФ (расчетно-табличный метод):",
        result.calculation_table_sknf_minimization,
    )
    _append_karnaugh_section(lines, "Минимизация СДНФ (карта Карно):", result.karnaugh_minimization)
    _append_karnaugh_section(
        lines, "Минимизация СКНФ (карта Карно):", result.karnaugh_sknf_minimization
    )
    return "\n".join(lines).strip()

