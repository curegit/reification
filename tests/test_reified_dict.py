import itertools
from unittest import TestCase
from reification import Reified


class ReifiedDict[T, S](Reified, dict[T, S]):
    pass


class ReifiedDictSub[T](ReifiedDict[str, T]):
    pass


class ReifiedDictTest(TestCase):
    def test_type_args(self):
        ReifiedFloatList = ReifiedDict[int, float]
        self.assertEqual(ReifiedFloatList.targ, (int, float))
        self.assertEqual(ReifiedFloatList.type_args, (int, float))
        d = ReifiedFloatList([(1, 2.3), (2, 4.5)])
        self.assertEqual(d.targ, (int, float))
        self.assertEqual(d.type_args, (int, float))
        ReifiedListDict = ReifiedDictSub[list[int]]
        self.assertEqual(ReifiedListDict.targ, list[int])
        self.assertEqual(ReifiedListDict.type_args, (list[int],))
        ds = ReifiedListDict()
        self.assertEqual(ds.targ, list[int])
        self.assertEqual(ds.type_args, (list[int],))

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
            ReifiedDict[int],
            type,
        ]
        for t1, t2, t3, t4 in itertools.product(types, repeat=4):
            with self.subTest(left=(t1, t2), right=(t3, t4)):
                d1 = ReifiedDict[t1, t2]
                d2 = ReifiedDict[t3, t4]
                if (t1, t2) == (t3, t4):
                    self.assertEqual(d1, d2)
                else:
                    self.assertNotEqual(d1, d2)

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
            ReifiedDict[int],
            ReifiedDict[ReifiedDict[int]],
            ReifiedDict[ReifiedDict[dict[str, float]]],
        ]
        for t1, t2, t3, t4 in itertools.product(types, repeat=4):
            with self.subTest(left=(t1, t2), right=(t3, t4)):
                d = ReifiedDict[t1, t2]()
                self.assertIsInstance(d, dict)
                self.assertIsInstance(d, Reified)
                self.assertIsInstance(d, ReifiedDict)
                self.assertIsInstance(d, ReifiedDict[t1, t2])
                if (t1, t2) == (t3, t4):
                    self.assertIsInstance(d, ReifiedDict[t3, t4])
                else:
                    self.assertNotIsInstance(d, ReifiedDict[t3, t4])

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
            ReifiedDict[int],
            ReifiedDict[ReifiedDict[int]],
            ReifiedDict[ReifiedDict[dict[str, float]]],
        ]
        for t1, t2, t3, t4 in itertools.product(types, repeat=4):
            with self.subTest(left=(t1, t2), right=(t3, t4)):
                d1 = ReifiedDict[t1, t2]
                d2 = ReifiedDict[t3, t4]
                self.assertTrue(issubclass(d1, dict))
                self.assertTrue(issubclass(d1, Reified))
                self.assertTrue(issubclass(d1, ReifiedDict))
                if d1 == d2:
                    self.assertTrue(issubclass(d1, d2))
                else:
                    self.assertFalse(issubclass(d1, d2))
