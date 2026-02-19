from typing import Any
from unittest import TestCase
from reification import Reified


class TypedRegistry[K, V](Reified):
    def __init__(self) -> None:
        super().__init__()
        self._store: dict[K, V] = {}

    def register(self, key: K, value: V) -> None:
        key_type, value_type = self.type_args
        if not isinstance(key, key_type):
            raise TypeError(f"Key must be {key_type.__name__}, got {type(key).__name__}")
        if not isinstance(value, value_type):
            raise TypeError(f"Value must be {value_type.__name__}, got {type(value).__name__}")
        self._store[key] = value

    def lookup(self, key: K) -> V:
        return self._store[key]

    def entries(self) -> list[tuple[K, V]]:
        return list(self._store.items())


class TypedRegistryTest(TestCase):
    def test_type_args(self):
        registry = TypedRegistry[str, int]()
        self.assertEqual(registry.targ, (str, int))
        self.assertEqual(registry.type_args, (str, int))

    def test_register_ok(self):
        registry = TypedRegistry[str, int]()
        registry.register("apples", 3)
        registry.register("bananas", 5)
        self.assertEqual(registry.lookup("apples"), 3)
        self.assertEqual(registry.lookup("bananas"), 5)

    def test_register_invalid_key(self):
        registry = TypedRegistry[str, int]()
        with self.assertRaises(TypeError):
            registry.register(42, 10)

    def test_register_invalid_value(self):
        registry = TypedRegistry[str, int]()
        with self.assertRaises(TypeError):
            registry.register("apples", "three")

    def test_register_both_invalid(self):
        registry = TypedRegistry[str, int]()
        with self.assertRaises(TypeError):
            registry.register(42, "spam")

    def test_lookup_missing_key(self):
        registry = TypedRegistry[str, int]()
        with self.assertRaises(KeyError):
            registry.lookup("missing")

    def test_entries(self):
        registry = TypedRegistry[str, int]()
        registry.register("x", 1)
        registry.register("y", 2)
        entries = registry.entries()
        self.assertIn(("x", 1), entries)
        self.assertIn(("y", 2), entries)
        self.assertEqual(len(entries), 2)

    def test_different_type_combinations(self):
        registry = TypedRegistry[int, str]()
        registry.register(1, "one")
        registry.register(2, "two")
        self.assertEqual(registry.lookup(1), "one")
        with self.assertRaises(TypeError):
            registry.register("three", 3)

    def test_default_type_args_cannot_init(self):
        registry = TypedRegistry()
        self.assertEqual(registry.targ, Any)
        self.assertEqual(registry.type_args, (Any,))
