import unittest
from calc.process_simulator import ProcessSimulator
from calc.item import Item
from calc.recipe_group import RecipeGroup
from calc.recipe import Recipe


class MockRecipeGroup(RecipeGroup):
    def __init__(self):
        self.recipes = {}

    def add_recipe(self, item_name, recipe):
        self.recipes[item_name] = recipe

    def get_recipe(self, item_name):
        return self.recipes.get(item_name, None)


class TestProcessSimulator(unittest.TestCase):
    def setUp(self):
        self.recipes = MockRecipeGroup()

    def test_no_recipes(self):
        item = Item("Wood Plank", 5)
        result = ProcessSimulator.get_total_costs(self.recipes, item)

        self.assertEqual(result.total_costs, [Item("Wood Plank", 5)])
        self.assertEqual(result.excess_items, [])
        self.assertEqual(result.intermediate_history, [])

    def test_single_recipe(self):
        item = Item("Wood Plank", 5)
        recipe = Recipe(
            main_product=Item("Wood Plank", 1),
            ingredients=[Item("Wood", 2)],
            byproducts=[],
        )
        self.recipes.add_recipe("Wood Plank", recipe)

        result = ProcessSimulator.get_total_costs(self.recipes, item)

        self.assertEqual(result.total_costs, [Item("Wood", 10)])
        self.assertEqual(result.excess_items, [])
        self.assertEqual(result.intermediate_history, [Item("Wood Plank", 5)])

    def test_multiple_recipes(self):
        item = Item("Wood Plank", 5)
        recipe1 = Recipe(
            main_product=Item("Wood Plank", 1),
            ingredients=[Item("Wood", 2)],
            byproducts=[],
        )
        recipe2 = Recipe(
            main_product=Item("Wood", 1), ingredients=[Item("Tree", 1)], byproducts=[]
        )
        self.recipes.add_recipe("Wood Plank", recipe1)
        self.recipes.add_recipe("Wood", recipe2)

        result = ProcessSimulator.get_total_costs(self.recipes, item)

        self.assertEqual(result.total_costs, [Item("Tree", 10)])
        self.assertEqual(result.excess_items, [])
        self.assertEqual(
            result.intermediate_history, [Item("Wood Plank", 5), Item("Wood", 10)]
        )

    def test_byproducts(self):
        item = Item("Wood Plank", 5)
        recipe = Recipe(
            main_product=Item("Wood Plank", 1),
            ingredients=[Item("Wood", 2)],
            byproducts=[Item("Sawdust", 1)],
        )
        self.recipes.add_recipe("Wood Plank", recipe)

        result = ProcessSimulator.get_total_costs(self.recipes, item)

        self.assertEqual(result.total_costs, [Item("Wood", 10)])
        self.assertEqual(result.excess_items, [Item("Sawdust", 5)])
        self.assertEqual(result.intermediate_history, [Item("Wood Plank", 5)])
    
    def test_multiple_products(self):
        item = Item("Wood Plank", 5)
        recipe = Recipe(
            main_product=Item("Wood Plank", 4),
            ingredients=[Item("Wood", 1)],
            byproducts=[],
        )
        self.recipes.add_recipe("Wood Plank", recipe)
        result = ProcessSimulator.get_total_costs(self.recipes, item)

        self.assertEqual(result.total_costs, [Item("Wood", 2)])
        self.assertEqual(result.excess_items, [Item("Wood Plank", 3)])
        self.assertEqual(result.intermediate_history, [Item("Wood Plank", 5)])


if __name__ == "__main__":
    unittest.main()
