#!.venv/bin/python

from calc.item import Item
from calc.recipe import Recipe
from calc.recipe_group import RecipeGroup
from calc.ingredient_tree import IngredientTree
from calc.process_simulator import ProcessSimulator

if __name__ == "__main__":
    recipes = RecipeGroup([
        Recipe(Item("Wood Plank", 4), [Item("Log")]),
        Recipe(Item("Stick", 4), [Item("Wood Plank", 2)]),
        Recipe(Item("Wooden Pickaxe"), [Item("Stick", 2), Item("Wood Plank", 3)]),
        Recipe(Item("Cake"), [Item("Wheat", 3), Item("Milk Bucket", 3), Item("Egg"), Item("Sugar", 2)], [Item("Bucket", 3)]),
        Recipe(Item("Bucket"), [Item("Iron Ingot", 3)]),
        Recipe(Item("Sugar"), [Item("Sugar Cane")]),
    ])
    
    def calc(recipes: RecipeGroup, item: Item):
        tree = IngredientTree(item, recipes)
        print(tree)
        result = ProcessSimulator.get_total_costs(recipes, item)
        print("総コスト:", ", ".join([str(item) for item in result.total_costs]))
        print("余り物:", ", ".join([str(item) for item in result.excess_items]) or "-")
        print("中間素材履歴:", ", ".join([str(item) for item in result.intermediate_history]))

    calc(recipes, Item("Cake", 1))
    calc(recipes, Item("Cake", 5))
    
    print()
    
    calc(recipes, Item("Wooden Pickaxe", 1))
    calc(recipes, Item("Wooden Pickaxe", 2))
    calc(recipes, Item("Wooden Pickaxe", 11))

