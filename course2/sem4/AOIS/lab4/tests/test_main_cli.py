import unittest

from src.hash_table import HashTable
from src.main import run_cli


class _FakeIO:
    def __init__(self, inputs: list[str]) -> None:
        self._inputs = iter(inputs)
        self.outputs: list[str] = []

    def input(self, prompt: str) -> str:
        self.outputs.append(prompt)
        return next(self._inputs)

    def output(self, message: str) -> None:
        self.outputs.append(str(message))


class CliTestCase(unittest.TestCase):
    def test_cli_full_crud_flow(self) -> None:
        table = HashTable(size=5)
        io = _FakeIO(
            [
                "1",
                "1",
                "one",
                "2",
                "1",
                "3",
                "1",
                "ONE",
                "2",
                "1",
                "4",
                "1",
                "2",
                "1",
                "5",
                "0",
            ]
        )

        run_cli(table=table, input_fn=io.input, output_fn=io.output)

        log = "\n".join(io.outputs)
        self.assertIn("Запись добавлена.", log)
        self.assertIn("Значение: one", log)
        self.assertIn("Запись обновлена.", log)
        self.assertIn("Значение: ONE", log)
        self.assertIn("Удалено значение: ONE", log)
        self.assertIn("Ключ не найден.", log)
        self.assertIn("Количество элементов: 0", log)
        self.assertIn("Выход из программы.", log)

    def test_cli_handles_non_integer_key(self) -> None:
        table = HashTable(size=5)
        io = _FakeIO(["1", "abc", "7", "value", "0"])

        run_cli(table=table, input_fn=io.input, output_fn=io.output)

        log = "\n".join(io.outputs)
        self.assertIn("Ошибка: введите целое число.", log)
        self.assertEqual(table.read(7), "value")

    def test_cli_handles_duplicate_and_overflow(self) -> None:
        table = HashTable(size=1)
        io = _FakeIO(["1", "1", "one", "1", "1", "dup", "1", "2", "two", "0"])

        run_cli(table=table, input_fn=io.input, output_fn=io.output)

        log = "\n".join(io.outputs)
        self.assertIn("already exists", log)
        self.assertIn("hash table is full", log)

    def test_cli_shows_table_dump(self) -> None:
        table = HashTable(size=3)
        table.create(1, "one")
        io = _FakeIO(["6", "0"])

        run_cli(table=table, input_fn=io.input, output_fn=io.output)

        log = "\n".join(io.outputs)
        self.assertIn("Содержимое таблицы:", log)
        self.assertIn("[1] занято: 1 -> one", log)

    def test_cli_handles_missing_update_delete_and_unknown_choice(self) -> None:
        table = HashTable(size=5)
        io = _FakeIO(["3", "1", "x", "4", "1", "9", "0"])

        run_cli(table=table, input_fn=io.input, output_fn=io.output)

        log = "\n".join(io.outputs)
        self.assertIn("does not exist", log)
        self.assertIn("Неизвестный пункт меню.", log)

    def test_cli_initializes_table_when_not_provided(self) -> None:
        io = _FakeIO(["0", "3", "10", "y", "0"])

        run_cli(table=None, input_fn=io.input, output_fn=io.output)

        log = "\n".join(io.outputs)
        self.assertIn("Настройка хеш-таблицы", log)
        self.assertIn("Ошибка: размер должен быть больше нуля.", log)
        self.assertIn("Выход из программы.", log)

    def test_cli_asks_for_auto_resize_flag(self) -> None:
        io = _FakeIO(["3", "0", "maybe", "n", "0"])

        run_cli(table=None, input_fn=io.input, output_fn=io.output)

        log = "\n".join(io.outputs)
        self.assertIn("Включить авторасширение? (y/n):", log)
        self.assertIn("Ошибка: введите y/n (да/нет).", log)


if __name__ == "__main__":
    unittest.main()
