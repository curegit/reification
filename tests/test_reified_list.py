import itertools
from unittest import TestCase
from reification import Reified


class ReifiedList[T](Reified, list[T]):
    pass


class ReifiedListSub[T](ReifiedList[T]):
    pass


class ReifiedListTest(TestCase):
    def test_type_args(self):
        ReifiedIntList = ReifiedList[int]
        self.assertEqual(ReifiedIntList.targ, int)
        self.assertEqual(ReifiedIntList.type_args, (int,))
        l = ReifiedIntList([1, 2, 3])
        self.assertEqual(l.targ, int)
        self.assertEqual(l.type_args, (int,))
        ReifiedIntListSub = ReifiedListSub[int]
        self.assertEqual(ReifiedIntListSub.targ, int)
        self.assertEqual(ReifiedIntListSub.type_args, (int,))
        ls = ReifiedIntListSub()
        self.assertEqual(ls.targ, int)
        self.assertEqual(ls.type_args, (int,))

    def test_typing(self):
        l = ReifiedList[int]()
        l.append(11)
        n = l[0]
        self.assertEqual(n + 2, 13)

    def test_equivalence(self):
        types = [
            int,
            str,
            float,
            bool,
            list[int],
            dict[int, str],
            tuple[bool],
            tuple[int],
            ReifiedList[int],
            type,
        ]
        for t1, t2 in itertools.product(types, repeat=2):
            with self.subTest(left=t1, right=t2):
                l1 = ReifiedList[t1]
                l2 = ReifiedList[t2]
                if t1 == t2:
                    self.assertEqual(l1, l2)
                else:
                    self.assertNotEqual(l1, l2)

    def test_instance(self):
        types = [
            int,
            str,
            float,
            bool,
            type,
            tuple[bool],
            tuple[int],
            list[int],
            dict[int, str],
            ReifiedList[int],
            ReifiedList[ReifiedList[int]],
            ReifiedList[ReifiedList[dict[str, float]]],
        ]
        for t1, t2 in itertools.product(types, repeat=2):
            with self.subTest(left=t1, right=t2):
                l = ReifiedList[t1]()
                self.assertIsInstance(l, list)
                self.assertIsInstance(l, Reified)
                self.assertIsInstance(l, ReifiedList)
                self.assertIsInstance(l, ReifiedList[t1])
                if t1 == t2:
                    self.assertIsInstance(l, ReifiedList[t2])
                else:
                    self.assertNotIsInstance(l, ReifiedList[t2])

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
            ReifiedList[int],
            ReifiedList[ReifiedList[int]],
            ReifiedList[ReifiedList[dict[str, float]]],
        ]
        for t1, t2 in itertools.product(types, repeat=2):
            with self.subTest(left=t1, right=t2):
                l1 = ReifiedList[t1]
                l2 = ReifiedList[t2]
                self.assertTrue(issubclass(l1, list))
                self.assertTrue(issubclass(l1, Reified))
                self.assertTrue(issubclass(l1, ReifiedList))
                if l1 == l2:
                    self.assertTrue(issubclass(l1, l2))
                else:
                    self.assertFalse(issubclass(l1, l2))
