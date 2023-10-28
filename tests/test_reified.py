from unittest import TestCase
from reification import Reified


class ReifiedSet[T](Reified, set[T]):
    pass


class ReifiedTest(TestCase):
    def test_mro(self):
        self.assertIn(Reified, ReifiedSet[int].__mro__)

    def test_banned_instantiating(self):
        with self.assertRaises(Exception):
            Reified()
        with self.assertRaises(Exception):
            Reified[int]()
