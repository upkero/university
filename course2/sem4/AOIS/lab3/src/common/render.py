from __future__ import annotations

from typing import Iterable, Sequence


def render_table(headers: Sequence[str], rows: Iterable[Sequence[object]]) -> str:
    rendered_rows = [[str(cell) for cell in row] for row in rows]
    widths = [len(str(header)) for header in headers]

    for row in rendered_rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def render_row(values: Sequence[str]) -> str:
        cells = [value.ljust(widths[index]) for index, value in enumerate(values)]
        return "| " + " | ".join(cells) + " |"

    header_line = render_row([str(header) for header in headers])
    separator = "|-" + "-|-".join("-" * width for width in widths) + "-|"
    body = [render_row(row) for row in rendered_rows]
    return "\n".join([header_line, separator, *body])


def render_section(title: str, body: str) -> str:
    return f"{title}\n{body}"

