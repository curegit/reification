from unittest import TestCase
from reification import Reified


class ReifiedStack[T](Reified):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[T] = []

    def push(self, item: T) -> None:
        # We can do runtime check
        if isinstance(item, self.targ):
            self.items.append(item)
        else:
            raise TypeError()

    def pop(self) -> T:
        if self.items:
            return self.items.pop()
        else:
            raise IndexError("pop from empty stack")


class ReifiedStackTest(TestCase):
    def test_type_args(self):
        stack = ReifiedStack[int]()
        self.assertIs(stack.targ, int)

    def test_ok(self):
        stack = ReifiedStack[int]()
        stack.push(10)
        stack.push(42)
        self.assertEqual(stack.pop(), 42)
        self.assertEqual(stack.pop(), 10)

    def test_fail(self):
        stack = ReifiedStack[str]()
        stack.push("spam")
        with self.assertRaises(TypeError):
            stack.push(100)

    def test_nested_type(self):
        stack = ReifiedStack[ReifiedStack[int]]()
        stack.push(ReifiedStack[int]())
        with self.assertRaises(TypeError):
            stack.push(ReifiedStack[str]())
