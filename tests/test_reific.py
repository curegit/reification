import itertools
from unittest import TestCase

from reific_stack import Stack

class SubClassTest(TestCase):

    def test_list(self):
        types = [int, str, float]
        for t1, t2 in itertools.product(types, repeat=2):
            with self.subTest(left=t1, right=t2):
                l1 = Stack[t1]
                l2 = Stack[t2]
                print(l1, l2)
                if t1 is t2:
                    self.assertTrue(issubclass(l1, l2))
                else:
                    self.assertFalse(issubclass(l1, l2))



class InstanceTest:
    pass
