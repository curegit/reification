from typing import TypeVar, Any
from unittest import TestCase


T = TypeVar("T")
S = TypeVar("S")


class Eqtest(TestCase):

    def test_union(self):
        self.assertEqual(int | str, str | int)
        self.assertNotEqual(int | str, int)
        self.assertEqual(list[int] | list[str], list[str] | list[int])
        self.assertNotEqual(list | list[int], list[int])

    def test_generics(self):
        self.assertEqual(list[int], list[int])
        self.assertNotEqual(list[int], list[str])
        self.assertEqual(dict[int, list[str]], dict[int, list[str]])
        self.assertNotEqual(dict[int, list[str]], dict[int, list[float]])

    def test_any(self):
        self.assertEqual(Any, Any)
        self.assertNotEqual(list[int], list[Any])

    def test_typevar(self):
        self.assertEqual(T, T)
        self.assertNotEqual(T, S)
