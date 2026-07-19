import itertools
from typing import Annotated
from unittest import TestCase
from reification import Reified


class ReifiedSet[T](Reified, set[T]):
    pass


class ReifiedClass[T](Reified):
    def some(self, val: T) -> T:
        return val


class ReifiedList[T](Reified, list[T]):
    pass


class ReifiedStrList[T](ReifiedClass[T], ReifiedList[str]):
    pass


class ReifiedTest(TestCase):
    def test_mro(self):
        self.assertIn(Reified, ReifiedSet[int].__mro__)

    def test_banned_instantiating(self):
        with self.assertRaises(TypeError):
            Reified()
        with self.assertRaises(TypeError):
            Reified[int]()

    def test_class_getitem_tuple_notations(self):
        c1 = ReifiedClass[int]
        instance = c1()
        c2 = ReifiedClass[int,]
        self.assertIs(c1, c2)
        self.assertIs(c1.targ, int)
        self.assertIs(c2.targ, int)
        self.assertIs(instance.targ, int)
        self.assertEqual(instance.type_args, (int,))

    def test_equivalent_type_args_do_not_replace_cached_metadata(self):
        class LocalReifiedClass[T](Reified):
            pass

        arg1 = int | str
        arg2 = str | int
        self.assertEqual(arg1, arg2)
        self.assertIsNot(arg1, arg2)

        c1 = LocalReifiedClass[arg1]
        instance = c1()
        c2 = LocalReifiedClass[arg2]

        self.assertIs(c1, c2)
        self.assertIs(c1.targ, arg1)
        self.assertIs(c2.targ, arg1)
        self.assertIs(instance.targ, arg1)
        self.assertIs(c1.type_args[0], arg1)
        self.assertIs(instance.type_args[0], arg1)

    def test_hashable_annotated_type_argument(self):
        class LocalReifiedClass[T](Reified):
            pass

        annotated = Annotated[int, ("unit", "ms")]
        reified = LocalReifiedClass[annotated]

        self.assertIs(reified.targ, annotated)
        self.assertIs(reified.type_args[0], annotated)

    def test_unhashable_annotated_type_argument(self):
        class LocalReifiedClass[T](Reified):
            pass

        annotated = Annotated[int, []]

        with self.assertRaisesRegex(TypeError, r"^Reified type arguments must be hashable\.$"):
            LocalReifiedClass[annotated]

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
