import unittest
from calc.item import Item
from calc.recipe import Recipe


class TestRecipe(unittest.TestCase):
    def test_initialization_with_byproducts(self):
        main_product = Item(name="Main Product")
        ingredients = [Item(name="Ingredient 1"), Item(name="Ingredient 2")]
        byproducts = [Item(name="Byproduct 1")]

        recipe = Recipe(main_product, ingredients, byproducts)

        self.assertEqual(recipe.main_product, main_product)
        self.assertEqual(recipe.ingredients, ingredients)
        self.assertEqual(recipe.byproducts, byproducts)

    def test_initialization_without_byproducts(self):
        main_product = Item(name="Main Product")
        ingredients = [Item(name="Ingredient 1"), Item(name="Ingredient 2")]

        recipe = Recipe(main_product, ingredients)

        self.assertEqual(recipe.main_product, main_product)
        self.assertEqual(recipe.ingredients, ingredients)
        self.assertEqual(recipe.byproducts, [])


if __name__ == "__main__":
    unittest.main()
