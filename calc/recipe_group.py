from typing import Self
from calc.recipe import Recipe
from calc.item import Item


class RecipeGroup:
    """複数のレシピを保持するクラス"""

    def __init__(self, recipes: list[Recipe] = []):
        """初期化とともにレシピを一括で登録する
        Args:
            recipes (list[Recipe], optional): レシピを含むリスト。省略すると`[]`。

        Examples:
            >>> recipes = RecipeGroup([
            ...     Recipe(Item("Wood Plank", 4), [Item("Log")]),
            ...     Recipe(Item("Stick", 4), [Item("Wood Plank", 2)]),
            ...     Recipe(Item("Wooden Pickaxe"), [Item("Stick", 2), Item("Wood Plank", 3)]),
            ... ])
        """
        self.recipes = {recipe.main_product.name: recipe for recipe in recipes}

    def add_recipe(
        self, main_product: Item, ingredients: list[Item], byproducts: list[Item] = []
    ) -> Self:
        """レシピを追加で登録する。

        Args:
            main_product (Item): 主産物となるアイテム
            ingredients (list[Item]): 必要な材料となるアイテムのリスト
            byproducts (list[Item], optional): 過程で生じる副産物となるアイテムのリスト。省略すると`[]`。

        Returns:
            Self: 自身のインスタンス
        """
        recipe = Recipe(main_product, ingredients, byproducts)
        self.recipes[main_product.name] = recipe
        return self

    def add_recipes(self, recipes: list[Recipe]) -> Self:
        """複数のレシピを一括で追加する。

        Args:
            recipes (list[Recipe]): レシピを含むリスト

        Returns:
            Self: 自身のインスタンス
        """
        for recipe in recipes:
            self.add_recipe(recipe.main_product, recipe.ingredients, recipe.byproducts)
        return self

    def get_recipe(self, item_name: str) -> Recipe | None:
        """アイテム名からレシピを取得する。

        Args:
            item_name (str): 取得するレシピのアイテム名

        Returns:
            Recipe | None: アイテム名に対応するレシピ。存在しない場合は`None`。
        """
        return self.recipes.get(item_name)
