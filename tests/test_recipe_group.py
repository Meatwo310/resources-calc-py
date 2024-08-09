import unittest
from calc.recipe_group import RecipeGroup
from calc.recipe import Recipe
from calc.item import Item


class TestRecipeGroup(unittest.TestCase):
    def setUp(self):
        self.recipe1 = Recipe(Item("Wood Plank", 4), [Item("Log")])
        self.recipe2 = Recipe(Item("Stick", 4), [Item("Wood Plank", 2)])
        self.recipe3 = Recipe(
            Item("Wooden Pickaxe"), [Item("Stick", 2), Item("Wood Plank", 3)]
        )
        self.recipe_group = RecipeGroup([self.recipe1, self.recipe2])

    def test_initialization(self):
        self.assertEqual(len(self.recipe_group.recipes), 2)
        self.assertIn("Wood Plank", self.recipe_group.recipes)
        self.assertIn("Stick", self.recipe_group.recipes)

    def test_add_recipe(self):
        self.recipe_group.add_recipe(
            Item("Wooden Pickaxe"), [Item("Stick", 2), Item("Wood Plank", 3)]
        )
        self.assertEqual(len(self.recipe_group.recipes), 3)
        self.assertIn("Wooden Pickaxe", self.recipe_group.recipes)

    def test_add_recipes(self):
        self.recipe_group.add_recipes([self.recipe3])
        self.assertEqual(len(self.recipe_group.recipes), 3)
        self.assertIn("Wooden Pickaxe", self.recipe_group.recipes)

    def test_get_recipe(self):
        recipe = self.recipe_group.get_recipe("Wood Plank")
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.main_product.name, "Wood Plank") # type: ignore
        self.assertEqual(recipe.main_product.quantity, 4)  # type: ignore

        recipe = self.recipe_group.get_recipe("Nonexistent Item")
        self.assertIsNone(recipe)


if __name__ == "__main__":
    unittest.main()
