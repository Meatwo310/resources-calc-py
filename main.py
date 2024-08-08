#!.venv/bin/python

import math
from typing import Self

class Item:
    """アイテム名と個数を表すクラス
    """
    def __init__(self, name: str, quantity: int = 1):
        """アイテムを初期化する

        Args:
            name (str): アイテム名
            quantity (int, optional): アイテムの個数。省略すると`1`。
        """
        self.name = name
        self.quantity = quantity

class Recipe:
    """アイテムとそれに必要な材料、過程で生じる副産物を表すクラス
    """
    def __init__(self, main_product: Item, ingredients: list[Item], byproducts: list[Item] = []):
        """レシピを初期化する

        Args:
            main_product (Item): 主産物となるアイテム
            ingredients (list[Item]): 必要な材料となるアイテムのリスト
            byproducts (list[Item], optional): 過程で生じる副産物となるアイテムのリスト。省略すると`[]`。
        """
        self.main_product = main_product
        self.ingredients = ingredients
        self.byproducts = byproducts

class RecipeGroup:
    """複数のレシピを保持するクラス
    """
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
        self.recipes: dict[str, Recipe] = {}
        self.add_recipes(recipes)
    
    def add_recipe(self, main_product: Item, ingredients: list[Item], byproducts: list[Item] = []) -> Self:
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
        """複数のレシピを一括で登録する。

        Args:
            recipes (list[Recipe]): レシピを含むリスト

        Returns:
            Self: 自身のインスタンス
        """
        self.recipes = {recipe.main_product.name: recipe for recipe in recipes}
        return self
    
    def get_recipe(self, item_name: str) -> Recipe | None:
        """アイテム名からレシピを取得する。

        Args:
            item_name (str): 取得するレシピのアイテム名

        Returns:
            Recipe | None: アイテム名に対応するレシピ。存在しない場合は`None`。
        """
        return self.recipes.get(item_name)

class IngredientTree:
    """アイテムとそれに必要な材料を再帰的に表すクラス
    """
    def __init__(self, item: Item, recipes: RecipeGroup):
        """ツリーにおけるノードにアイテムを設定し、`recipes`から自動的に子要素を計算する

        Args:
            item (Item): ノードに設定するアイテム
            recipes (RecipeGroup): 子要素の計算に用いるレシピグループ
        """
        self.item = item
        self.actual_quantity = item.quantity
        self.children: list[IngredientTree] = []
        self.byproducts: list[Item] = []
        self.calculate_children(recipes)
    
    @staticmethod
    def get_required_quantity(min_quantity: int, batch_size: int) -> int:
        """最小の個数と一度に作られる個数から実際に作成されるアイテム数を計算する

        Args:
            min_quantity (int): 要求する最小のアイテム数
            batch_size (int): 一度に作成されるアイテム数

        Returns:
            int: 実際に作成する必要があるアイテム数
        
        Examples:
            >>> IngredientTree.get_required_quantity(3, 4)
            4
            >>> IngredientTree.get_required_quantity(4, 4)
            4
            >>> IngredientTree.get_required_quantity(5, 4)
            8
        """
        return math.ceil(min_quantity / batch_size) * batch_size
    
    def calculate_children(self, recipes: RecipeGroup) -> Self:
        """自身のアイテムの作成に必要な材料を再帰的に計算し、子要素に設定する

        `self.item`を`recipes`から参照し、必要な材料を子要素に設定する。
        子要素の設定時、`calculate_children()`が自動的に呼び出されることで、再帰的な計算となる。
        また、実際に作成されるアイテム数は`IngredientTree.get_required_quantity()`を用いて自動的に調整され、計算に用いられる。
        副産物は計算において完全に無視されるが、`self.byproducts`に集計される。

        Args:
            recipes (RecipeGroup): 計算に用いられるレシピグループ

        Returns:
            Self: 自身のインスタンス

        Examples:
            >>> recipes = RecipeGroup([
            ...     Recipe(Item("Wood Plank", 4), [Item("Log")]),
            ...     Recipe(Item("Stick", 4), [Item("Wood Plank", 2)]),
            ...     Recipe(Item("Wooden Pickaxe"), [Item("Stick", 2), Item("Wood Plank", 3)]),
            ... ])
            >>> print(IngredientTree(Item("Wooden Pickaxe"), recipes))
            Wooden Pickaxe x1
            |-Stick x2 (+2)
            | \\-Wood Plank x2 (+2)
            |   \\-Log x1
            \\-Wood Plank x3 (+1)
                \\-Log x1
        """
        recipe = recipes.get_recipe(self.item.name)
        
        if not recipe:
            self.children = []
            self.byproducts = []
            return self
        
        self.actual_quantity = self.get_required_quantity(self.item.quantity, recipe.main_product.quantity)
        self.children = [
            IngredientTree(
                Item(ingredient.name, ingredient.quantity * self.actual_quantity // recipe.main_product.quantity),
                recipes,
            )
            for ingredient in recipe.ingredients
        ]
        self.byproducts = [byproduct for byproduct in recipe.byproducts]
        
        return self
    
    def __str__(self, level=0, is_last=True, prefix="") -> str:
        """ツリーを文字列として表現する

        Args:
            level (int, optional): ツリーの深さ。省略すると`0`。
            is_last (bool, optional): このノードが親ノードの最後の子ノードかどうか。省略すると`True`。
            prefix (str, optional): ノードにつく接頭辞。省略すると`""`。

        Returns:
            str: ツリーを表現する文字列

        Examples:
            >>> str(IngredientTree(Item("Wooden Pickaxe"), recipes))
            Wooden Pickaxe x1
            |-Stick x2 (+2)
            | \\-Wood Plank x2 (+2)
            |   \\-Log x1
            \\-Wood Plank x3 (+1)
              \\-Log x1
        """
        indent = prefix + ("\\-" if is_last else "|-") if level > 0 else ""
        result = f"{indent}{self.item.name} x{self.item.quantity}"
        
        if self.actual_quantity != self.item.quantity:
            result += f" (+{self.actual_quantity - self.item.quantity})"

        if self.byproducts:
            byproducts_str = " + " + " + ".join(
                [
                    f"{byproduct.name} x{byproduct.quantity}"
                    for byproduct in self.byproducts
                ]
            )
            result += f" [{byproducts_str}]"

        new_prefix = prefix + ("  " if is_last else "| ") if level > 0 else ""
        for i, child in enumerate(self.children):
            result += f"\n{child.__str__(level + 1, is_last=(i == len(self.children) - 1), prefix=new_prefix)}"

        return result

if __name__ == "__main__":
    recipes = RecipeGroup([
        Recipe(Item("Wood Plank", 4), [Item("Log")]),
        Recipe(Item("Stick", 4), [Item("Wood Plank", 2)]),
        Recipe(Item("Wooden Pickaxe"), [Item("Stick", 2), Item("Wood Plank", 3)]),
        Recipe(Item("Cake"), [Item("Wheat", 3), Item("Milk Bucket", 3), Item("Egg"), Item("Sugar", 2)], [Item("Bucket", 3)]),
        Recipe(Item("Bucket"), [Item("Iron Ingot", 3)]),
        Recipe(Item("Sugar"), [Item("Sugar Cane")]),
    ])

    print(IngredientTree(Item("Wooden Pickaxe", 1), recipes))
