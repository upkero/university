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
    if not chart.minterms:
        return "нет единичных наборов"
    header = "imp\\m " + " ".join(f"{minterm:>3}" for minterm in chart.minterms)
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
        "Минимизация (расчетный метод):",
        f"Исходная СДНФ: {result.calculation_minimization.initial_sdnf}",
        _format_gluing_stages(result.calculation_minimization),
        f"Простые импликанты: {_format_implicants(result.calculation_minimization.prime_implicants)}",
        "Проверка лишних импликант:",
        _format_redundancy_checks(result.calculation_minimization),
        f"Результат: {result.calculation_minimization.expression}",
        "",
        "Минимизация (расчетно-табличный метод):",
        f"Исходная СДНФ: {result.calculation_table_minimization.initial_sdnf}",
        _format_gluing_stages(result.calculation_table_minimization),
        "Таблица простых импликант:",
        _format_chart(result.calculation_table_minimization.chart),
        f"Выбранные импликанты: {_format_implicants(result.calculation_table_minimization.selected_implicants)}",
        f"Результат: {result.calculation_table_minimization.expression}",
        "",
        "Минимизация (карта Карно):",
        result.karnaugh_minimization.rendered_map,
        f"Группы: {result.karnaugh_minimization.groups}",
        f"Результат: {result.karnaugh_minimization.expression}",
    ]
    return "\n".join(lines).strip()

