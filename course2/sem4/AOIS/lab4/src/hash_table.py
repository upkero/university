"""Simple hash table with linear probing collision resolution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class _Entry:
    key: int
    value: Any


_DELETED = object()


class HashTable:
    """Hash table for integer keys with CRUD operations."""

    def __init__(
        self, size: int = 20, base: int = 0, auto_resize: bool = False
    ) -> None:
        if size <= 0:
            raise ValueError("size must be greater than zero")

        self._size = size
        self._base = base
        self._auto_resize = auto_resize
        self._table: list[_Entry | object | None] = [None] * size
        self._count = 0

    @property
    def size(self) -> int:
        return self._size

    @property
    def base(self) -> int:
        return self._base

    @property
    def auto_resize(self) -> bool:
        return self._auto_resize

    def __len__(self) -> int:
        return self._count

    def hash_address(self, key: int) -> int:
        """Calculate address by h(V) = V mod H + B."""
        self._validate_key(key)
        return key % self._size + self._base

    def create(self, key: int, value: Any) -> None:
        """Create a new record. Raises KeyError for duplicate key."""
        index = self._probe(key, for_insert=True)
        if index is None:
            if self._auto_resize:
                self._resize(self._size * 2)
                index = self._probe(key, for_insert=True)
            if index is None:
                raise OverflowError("hash table is full")

        slot = self._table[index]
        if slot is not None and slot is not _DELETED and slot.key == key:
            raise KeyError(f"key {key} already exists")

        self._table[index] = _Entry(key=key, value=value)
        self._count += 1

    def read(self, key: int) -> Any | None:
        """Read value by key. Returns None if key does not exist."""
        index = self._probe(key, for_insert=False)
        if index is None:
            return None
        return self._table[index].value

    def update(self, key: int, value: Any) -> None:
        """Update existing record. Raises KeyError if key does not exist."""
        index = self._probe(key, for_insert=False)
        if index is None:
            raise KeyError(f"key {key} does not exist")
        self._table[index] = _Entry(key=key, value=value)

    def delete(self, key: int) -> Any:
        """Delete record and return removed value. Raises KeyError if missing."""
        index = self._probe(key, for_insert=False)
        if index is None:
            raise KeyError(f"key {key} does not exist")

        value = self._table[index].value
        self._table[index] = _DELETED
        self._count -= 1
        return value

    def dump(self) -> list[dict[str, Any]]:
        """Return a snapshot of the internal table state."""
        snapshot: list[dict[str, Any]] = []
        for offset, slot in enumerate(self._table):
            address = self._base + offset
            if slot is None:
                snapshot.append(
                    {
                        "address": address,
                        "state": "empty",
                        "key": None,
                        "value": None,
                    }
                )
            elif slot is _DELETED:
                snapshot.append(
                    {
                        "address": address,
                        "state": "deleted",
                        "key": None,
                        "value": None,
                    }
                )
            else:
                snapshot.append(
                    {
                        "address": address,
                        "state": "occupied",
                        "key": slot.key,
                        "value": slot.value,
                    }
                )
        return snapshot

    def _resize(self, new_size: int) -> None:
        if new_size <= self._size:
            raise ValueError("new size must be greater than current size")

        old_table = self._table
        self._table = [None] * new_size
        self._size = new_size
        self._count = 0

        for slot in old_table:
            if isinstance(slot, _Entry):
                self._insert_rehash(slot.key, slot.value)

    def _insert_rehash(self, key: int, value: Any) -> None:
        index = self._probe(key, for_insert=True)
        if index is None:
            raise RuntimeError("rehash failed")
        self._table[index] = _Entry(key=key, value=value)
        self._count += 1

    def _validate_key(self, key: int) -> None:
        if not isinstance(key, int):
            raise TypeError("key must be an integer")

    def _address_to_index(self, address: int) -> int:
        return address - self._base

    def _next_address(self, address: int) -> int:
        last_address = self._base + self._size - 1
        if address == last_address:
            return self._base
        return address + 1

    def _probe(self, key: int, for_insert: bool) -> int | None:
        start_address = self.hash_address(key)
        address = start_address
        first_deleted_index: int | None = None

        for _ in range(self._size):
            index = self._address_to_index(address)
            slot = self._table[index]

            if slot is None:
                if for_insert:
                    return (
                        first_deleted_index
                        if first_deleted_index is not None
                        else index
                    )
                return None

            if slot is _DELETED:
                if for_insert and first_deleted_index is None:
                    first_deleted_index = index
            elif slot.key == key:
                return index

            address = self._next_address(address)

        if for_insert and first_deleted_index is not None:
            return first_deleted_index
        return None
