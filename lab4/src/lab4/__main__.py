from __future__ import annotations

import sys

from .cli import main as cli_main
from .gui import main as gui_main


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--gui" in args:
        args = [value for value in args if value != "--gui"]
        return gui_main(args)
    return cli_main(args)


if __name__ == "__main__":
    raise SystemExit(main())
