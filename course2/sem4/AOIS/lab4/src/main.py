"""CLI interface for hash table operations."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from src.hash_table import HashTable


InputFn = Callable[[str], str]
OutputFn = Callable[[str], Any]


def _ask_int(prompt: str, input_fn: InputFn, output_fn: OutputFn) -> int:
    while True:
        raw = input_fn(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            output_fn("Ошибка: введите целое число.")


def _print_menu(output_fn: OutputFn) -> None:
    output_fn("")
    output_fn("Меню:")
    output_fn("1 - Добавить запись")
    output_fn("2 - Найти запись")
    output_fn("3 - Обновить запись")
    output_fn("4 - Удалить запись")
    output_fn("5 - Показать количество элементов")
    output_fn("6 - Показать содержимое таблицы")
    output_fn("0 - Выход")


def _ask_yes_no(prompt: str, input_fn: InputFn, output_fn: OutputFn) -> bool:
    while True:
        raw = input_fn(prompt).strip().lower()
        if raw in {"y", "yes", "д", "да", "1"}:
            return True
        if raw in {"n", "no", "н", "нет", "0"}:
            return False
        output_fn("Ошибка: введите y/n (да/нет).")


def run_cli(
    table: HashTable | None = None,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    if table is None:
        output_fn("Настройка хеш-таблицы")

        size = _ask_int("Введите размер H: ", input_fn, output_fn)
        while size <= 0:
            output_fn("Ошибка: размер должен быть больше нуля.")
            size = _ask_int("Введите размер H: ", input_fn, output_fn)

        base = _ask_int("Введите базовый адрес B: ", input_fn, output_fn)
        auto_resize = _ask_yes_no(
            "Включить авторасширение? (y/n): ", input_fn, output_fn
        )
        table = HashTable(size=size, base=base, auto_resize=auto_resize)

    while True:
        _print_menu(output_fn)
        choice = input_fn("Выберите пункт: ").strip()

        if choice == "1":
            key = _ask_int("Введите ключ: ", input_fn, output_fn)
            value = input_fn("Введите значение: ")
            try:
                table.create(key, value)
                output_fn("Запись добавлена.")
            except (KeyError, OverflowError) as error:
                output_fn(f"Ошибка: {error}")

        elif choice == "2":
            key = _ask_int("Введите ключ: ", input_fn, output_fn)
            value = table.read(key)
            if value is None:
                output_fn("Ключ не найден.")
            else:
                output_fn(f"Значение: {value}")

        elif choice == "3":
            key = _ask_int("Введите ключ: ", input_fn, output_fn)
            value = input_fn("Введите новое значение: ")
            try:
                table.update(key, value)
                output_fn("Запись обновлена.")
            except KeyError as error:
                output_fn(f"Ошибка: {error}")

        elif choice == "4":
            key = _ask_int("Введите ключ: ", input_fn, output_fn)
            try:
                removed_value = table.delete(key)
                output_fn(f"Удалено значение: {removed_value}")
            except KeyError as error:
                output_fn(f"Ошибка: {error}")

        elif choice == "5":
            output_fn(f"Количество элементов: {len(table)}")

        elif choice == "6":
            output_fn("Содержимое таблицы:")
            state_labels = {
                "empty": "пусто",
                "deleted": "удалено",
                "occupied": "занято",
            }
            for slot in table.dump():
                state = state_labels[slot["state"]]
                address = slot["address"]
                if slot["state"] == "occupied":
                    output_fn(
                        f"[{address}] {state}: {slot['key']} -> {slot['value']}"
                    )
                else:
                    output_fn(f"[{address}] {state}")

        elif choice == "0":
            output_fn("Выход из программы.")
            break

        else:
            output_fn("Неизвестный пункт меню.")


def main() -> None:
    run_cli()


if __name__ == "__main__":  # pragma: no cover
    main()
