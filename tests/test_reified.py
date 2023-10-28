import itertools
from unittest import TestCase
from reification import Reified


class ReifiedSet[T](Reified, set[T]):
    pass


class ReifiedClass[T](Reified):
    def some(val: T) -> T:
        return val


class ReifiedList[T](Reified, list[T]):
    pass


class ReifiedStrList[T](ReifiedClass[T], ReifiedList[str]):
    pass


class ReifiedTest(TestCase):
    def test_mro(self):
        self.assertIn(Reified, ReifiedSet[int].__mro__)

    def test_banned_instantiating(self):
        with self.assertRaises(Exception):
            Reified()
        with self.assertRaises(Exception):
            Reified[int]()

    def test_subclass(self):
        types = [
            int,
            str,
            float,
            bool,
            type,
            list[int],
            dict[int, str],
            tuple[bool],
            tuple[int],
            ReifiedClass[int],
            ReifiedClass[ReifiedClass[int]],
            ReifiedClass[ReifiedClass[dict[str, float]]],
        ]
        for t1, t2 in itertools.product(types, repeat=2):
            with self.subTest(left=t1, right=t2):
                l1 = ReifiedStrList[t1]
                l2 = ReifiedStrList[t2]
                self.assertTrue(issubclass(l1, list))
                self.assertTrue(issubclass(l1, Reified))
                self.assertTrue(issubclass(l1, ReifiedList))
                self.assertTrue(issubclass(l1, ReifiedList[str]))
                self.assertTrue(issubclass(l1, ReifiedClass))
                self.assertFalse(issubclass(l1, ReifiedClass[t1]))
                if l1 == l2:
                    self.assertTrue(issubclass(l1, l2))
                else:
                    self.assertFalse(issubclass(l1, l2))
