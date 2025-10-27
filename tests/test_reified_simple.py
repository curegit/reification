from unittest import TestCase
from reification import Reified


class ReifiedObject[T](Reified):
    pass


class ReifiedObjectTest(TestCase):
    def test_instantiate(self):
        obj = ReifiedObject[int]()
        self.assertIs(obj.targ, int)
        with self.assertRaises(TypeError):
            ReifiedObject[str]("")
