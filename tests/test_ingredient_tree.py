import unittest
from calc.item import Item
from calc.recipe_group import RecipeGroup
from calc.recipe import Recipe
from calc.ingredient_tree import IngredientTree

class TestIngredientTree(unittest.TestCase):

    def test_get_process_times(self):
        self.assertEqual(IngredientTree.get_process_times(3, 4), 1)
        self.assertEqual(IngredientTree.get_process_times(4, 4), 1)
        self.assertEqual(IngredientTree.get_process_times(5, 4), 2)
        self.assertEqual(IngredientTree.get_process_times(0, 4), 0)
        self.assertEqual(IngredientTree.get_process_times(8, 4), 2)

    def test_get_required_quantity(self):
        self.assertEqual(IngredientTree.get_required_quantity(3, 4), 4)
        self.assertEqual(IngredientTree.get_required_quantity(4, 4), 4)
        self.assertEqual(IngredientTree.get_required_quantity(5, 4), 8)
        self.assertEqual(IngredientTree.get_required_quantity(0, 4), 0)
        self.assertEqual(IngredientTree.get_required_quantity(8, 4), 8)

    def test_calculate_children(self):
        recipes = RecipeGroup([
            Recipe(Item("Wood Plank", 4), [Item("Log")]),
            Recipe(Item("Stick", 4), [Item("Wood Plank", 2)]),
            Recipe(Item("Wooden Pickaxe"), [Item("Stick", 2), Item("Wood Plank", 3)]),
        ])
        tree = IngredientTree(Item("Wooden Pickaxe"), recipes)
        self.assertEqual(len(tree.children), 2)
        self.assertEqual(tree.children[0].item.name, "Stick")
        self.assertEqual(tree.children[0].item.quantity, 2)
        self.assertEqual(tree.children[1].item.name, "Wood Plank")
        self.assertEqual(tree.children[1].item.quantity, 3)

    def test_str(self):
        recipes = RecipeGroup([
            Recipe(Item("Wood Plank", 4), [Item("Log")]),
            Recipe(Item("Stick", 4), [Item("Wood Plank", 2)]),
            Recipe(Item("Wooden Pickaxe"), [Item("Stick", 2), Item("Wood Plank", 3)]),
        ])
        tree = IngredientTree(Item("Wooden Pickaxe"), recipes)
        expected_str = (
            "Wooden Pickaxe x1\n"
            "|-Stick x2 (+2)\n"
            "| \\-Wood Plank x2 (+2)\n"
            "|   \\-Log x1\n"
            "\\-Wood Plank x3 (+1)\n"
            "  \\-Log x1"
        )
        self.assertEqual(str(tree), expected_str)

if __name__ == '__main__':
    unittest.main()
