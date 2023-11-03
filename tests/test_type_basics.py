import types
from typing import Generic, Any
from unittest import TestCase


class BasicsTest(TestCase):
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

    def test_typevar[T, S](self):
        self.assertEqual(T, T)
        self.assertNotEqual(T, S)

    def test_bases(self):
        class X(list[str]):
            pass

        self.assertEqual(types.get_original_bases(X)[0], list[str])
        self.assertNotEqual(types.get_original_bases(X)[0], list[int])
        self.assertNotEqual(types.get_original_bases(X)[0], list)

    def test_mro(self):
        class A:
            pass

        class B[T](A):
            def some(val: T) -> T:
                return val

        class C[T](B[T]):
            pass

        self.assertFalse(issubclass(A, Generic))
        self.assertTrue(issubclass(B, Generic))
        self.assertLess(B.__mro__.index(B), B.__mro__.index(Generic))
        self.assertLess(C.__mro__.index(B), C.__mro__.index(Generic))
