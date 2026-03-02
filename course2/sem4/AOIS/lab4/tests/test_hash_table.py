import unittest

from src.hash_table import HashTable


class HashTableTestCase(unittest.TestCase):
    def test_hash_formula_with_base(self) -> None:
        table = HashTable(size=20, base=7)
        self.assertEqual(table.hash_address(42), 42 % 20 + 7)

    def test_create_and_read(self) -> None:
        table = HashTable(size=5)
        table.create(1, "one")
        self.assertEqual(table.read(1), "one")

    def test_read_missing_returns_none(self) -> None:
        table = HashTable(size=5)
        self.assertIsNone(table.read(100))

    def test_create_duplicate_key_raises(self) -> None:
        table = HashTable(size=5)
        table.create(1, "one")
        with self.assertRaises(KeyError):
            table.create(1, "new")

    def test_update_existing_key(self) -> None:
        table = HashTable(size=5)
        table.create(1, "one")
        table.update(1, "ONE")
        self.assertEqual(table.read(1), "ONE")

    def test_update_missing_key_raises(self) -> None:
        table = HashTable(size=5)
        with self.assertRaises(KeyError):
            table.update(1, "ONE")

    def test_delete_existing_key_returns_value(self) -> None:
        table = HashTable(size=5)
        table.create(1, "one")
        deleted = table.delete(1)
        self.assertEqual(deleted, "one")
        self.assertIsNone(table.read(1))

    def test_delete_missing_key_raises(self) -> None:
        table = HashTable(size=5)
        with self.assertRaises(KeyError):
            table.delete(1)

    def test_auto_resize_grows_table_and_preserves_values(self) -> None:
        table = HashTable(size=2, auto_resize=True)
        table.create(1, "one")
        table.create(2, "two")
        table.create(3, "three")

        self.assertGreaterEqual(table.size, 4)
        self.assertEqual(table.read(1), "one")
        self.assertEqual(table.read(2), "two")
        self.assertEqual(table.read(3), "three")

    def test_resize_requires_growth(self) -> None:
        table = HashTable(size=2, auto_resize=True)
        with self.assertRaises(ValueError):
            table._resize(2)

    def test_dump_reflects_internal_state(self) -> None:
        table = HashTable(size=3)
        table.create(1, "one")  # index 1
        table.create(4, "four")  # collision -> index 2
        table.delete(1)

        snapshot = table.dump()
        self.assertEqual(len(snapshot), 3)
        self.assertEqual(snapshot[0]["state"], "empty")
        self.assertEqual(snapshot[1]["state"], "deleted")
        self.assertEqual(snapshot[2]["state"], "occupied")
        self.assertEqual(snapshot[2]["key"], 4)
        self.assertEqual(snapshot[2]["value"], "four")

    def test_len_changes_after_create_and_delete(self) -> None:
        table = HashTable(size=5)
        self.assertEqual(len(table), 0)
        table.create(1, "one")
        table.create(2, "two")
        self.assertEqual(len(table), 2)
        table.delete(1)
        self.assertEqual(len(table), 1)

    def test_linear_probing_for_collisions(self) -> None:
        table = HashTable(size=5)
        table.create(1, "one")
        table.create(6, "six")   # 6 % 5 == 1
        table.create(11, "eleven")  # 11 % 5 == 1
        self.assertEqual(table.read(1), "one")
        self.assertEqual(table.read(6), "six")
        self.assertEqual(table.read(11), "eleven")

    def test_linear_probing_wraps_with_non_zero_base(self) -> None:
        table = HashTable(size=3, base=10)
        table.create(2, "a")  # start at address 12
        table.create(5, "b")  # collision, wraps to 10
        table.create(8, "c")  # collision, then 11
        self.assertEqual(table.read(2), "a")
        self.assertEqual(table.read(5), "b")
        self.assertEqual(table.read(8), "c")

    def test_delete_keeps_probe_chain(self) -> None:
        table = HashTable(size=5)
        table.create(1, "one")
        table.create(6, "six")
        table.delete(1)
        self.assertEqual(table.read(6), "six")

    def test_deleted_slot_is_reused(self) -> None:
        table = HashTable(size=5)
        table.create(1, "one")
        table.create(6, "six")
        table.delete(1)
        table.create(11, "eleven")
        self.assertEqual(table.read(11), "eleven")
        self.assertEqual(table.read(6), "six")

    def test_insert_into_table_with_only_deleted_slots(self) -> None:
        table = HashTable(size=2)
        table.create(1, "one")
        table.create(2, "two")
        table.delete(1)
        table.delete(2)
        table.create(3, "three")
        self.assertEqual(table.read(3), "three")

    def test_overflow_when_table_is_full(self) -> None:
        table = HashTable(size=2)
        table.create(1, "one")
        table.create(2, "two")
        with self.assertRaises(OverflowError):
            table.create(3, "three")

    def test_invalid_size_raises(self) -> None:
        with self.assertRaises(ValueError):
            HashTable(size=0)

    def test_non_integer_key_raises_for_all_operations(self) -> None:
        table = HashTable(size=5)
        with self.assertRaises(TypeError):
            table.hash_address("1")
        with self.assertRaises(TypeError):
            table.create("1", "one")
        with self.assertRaises(TypeError):
            table.read("1")
        with self.assertRaises(TypeError):
            table.update("1", "one")
        with self.assertRaises(TypeError):
            table.delete("1")


if __name__ == "__main__":
    unittest.main()
