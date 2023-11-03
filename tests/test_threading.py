import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from unittest import TestCase
from reification import Reified


class ReifiedClass[T](Reified):
    def some(val: T) -> T:
        return val


class ThreadingTest(TestCase):
    def test_safety(self, n: int = 200, workers: int = 1024):
        def get_reified_type(param):
            return ReifiedClass[param]

        with ThreadPoolExecutor(max_workers=workers) as executor:
            for k in range(n):
                with self.subTest(k=k):
                    literal_type = str(k)
                    fs = [executor.submit(get_reified_type, literal_type) for _ in range(workers)]
                    concurrent.futures.wait(fs)
                    t = get_reified_type(literal_type)
                    results = [f.result() == t for f in fs]
                    self.assertTrue(all(results))
