import unittest
from calc.item import Item


class TestItem(unittest.TestCase):
    def test_initialization(self):
        # Test with default quantity
        item = Item("Wood Plank")
        self.assertEqual(item.name, "Wood Plank")
        self.assertEqual(item.quantity, 1)

        # Test with specified quantity
        item = Item("Wood Plank", 4)
        self.assertEqual(item.name, "Wood Plank")
        self.assertEqual(item.quantity, 4)

    def test_str_representation(self):
        # Test string representation with default quantity
        item = Item("Wood Plank")
        self.assertEqual(str(item), "Wood Plank x1")

        # Test string representation with specified quantity
        item = Item("Wood Plank", 4)
        self.assertEqual(str(item), "Wood Plank x4")


if __name__ == "__main__":
    unittest.main()
