import unittest

from .syncdicts import AutoSyncDict, AutoDbDict


class MyTest(unittest.TestCase):
    def test_puts(self):
        a = AutoSyncDict(".some_save", clean_start=True)
        values = [("a", 1), ("b", 2), ("c", 3), ("d", 4)]

        for i, j in values:
            a[i] = j

        self.assertEqual(len(a), len(values))

        for i, j in values:
            self.assertEqual(a[i], j)

        a["d"] = 5

        self.assertEqual(len(a), len(values))
        self.assertEqual(a["d"], 5)

        del a["d"]

        self.assertEqual("d" in a, False)

        a.clear()

        self.assertEqual(len(a), 0)

    def test_lru(self):
        SIZE = 3
        a = AutoSyncDict(size=SIZE, clean_start=True)
        values = [("a", 1), ("b", 2), ("c", 3), ("d", 4)]

        for i, j in values:
            a[i] = j

        self.assertEqual(len(a), SIZE)

        for i, j in values[1:]:
            self.assertEqual(a[i], j)

        a["d"] = 5

        self.assertEqual(len(a), SIZE)
        self.assertEqual(a["d"], 5)

        del a["d"]

        self.assertEqual("d" in a, False)

        a.clear()

        self.assertEqual(len(a), 0)

    def test_db(self):

        a = AutoDbDict(clean_start=True)
        values = [("a", 1), ("b", 2), ("c", 3), ("d", 4)]

        for i, j in values:
            a[i] = j

        for i, j in values[1:]:
            self.assertEqual(a[i], j)

        self.assertEqual(len(a), 4)

        self.assertEqual("d" in a, True)

        del a["d"]

        self.assertEqual("d" in a, False)

        self.assertEqual(len(a), 3)

        keys = a.keys()

        self.assertEqual(keys, ["a", "b", "c"])

        values = a.values()

        self.assertEqual(values, [1, 2, 3])

        values = a.pop("a", "b")

        self.assertEqual(values, [1, 2])

        for i in a:
            self.assertEqual(i, 3)

        a["d"] = 5
        self.assertTrue(a == {"c": 3, "d": 5})
