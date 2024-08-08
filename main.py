#!.venv/bin/python

import math
from typing import NamedTuple, Self

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
    
    def __str__(self) -> str:
        """アイテムを文字列として表現する

        Returns:
            str: アイテムを表現する文字列

        Examples:
            >>> str(Item("Wood Plank", 4))
            'Wood Plank x4'
        """
        return f"{self.name} x{self.quantity}"

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
        self.recipes = recipes
        self.children: list[IngredientTree] = []
        self.byproducts: list[Item] = []
        self.calculate_children()
    
    @staticmethod
    def get_craft_times(min_quantity: int, batch_size: int) -> int:
        """最小の個数と一度に作られる個数から必要なクラフト回数を計算する

        Args:
            min_quantity (int): 要求する最小のアイテム数
            batch_size (int): 一度に作成されるアイテム数

        Returns:
            int: 必要なクラフト回数
        
        Examples:
            >>> IngredientTree.get_craft_times(3, 4)
            1
            >>> IngredientTree.get_craft_times(4, 4)
            1
            >>> IngredientTree.get_craft_times(5, 4)
            2
        """
        return math.ceil(min_quantity / batch_size)
    
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
        return IngredientTree.get_craft_times(min_quantity, batch_size) * batch_size
    
    def calculate_children(self) -> Self:
        """自身のアイテムの作成に必要な材料を再帰的に計算し、子要素に設定する

        `self.item`を`self.recipes`から参照し、必要な材料を子要素に設定する。
        子要素の設定時、このメソッドは自動的に呼び出されるため、再帰的な計算となる。
        また、実際に作成されるアイテム数は`IngredientTree.get_required_quantity()`を用いて自動的に調整され、計算に用いられる。
        副産物は計算において完全に無視されるが、`self.byproducts`に集計される。

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
        recipe = self.recipes.get_recipe(self.item.name)
        
        if not recipe:
            self.children = []
            self.byproducts = []
            return self
        
        self.actual_quantity = self.get_required_quantity(self.item.quantity, recipe.main_product.quantity)
        self.children = [
            IngredientTree(
                Item(ingredient.name, ingredient.quantity * self.actual_quantity // recipe.main_product.quantity),
                self.recipes,
            ) for ingredient in recipe.ingredients
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
            byproducts_str = " + " + " + ".join([f"{byproduct.name} x{byproduct.quantity}" for byproduct in self.byproducts])
            result += f" [{byproducts_str}]"

        new_prefix = prefix + ("  " if is_last else "| ") if level > 0 else ""
        for i, child in enumerate(self.children):
            result += f"\n{child.__str__(level + 1, is_last=(i == len(self.children) - 1), prefix=new_prefix)}"

        return result

class RecipeSimulator:
    """レシピを用いた加工をシミュレーションするクラス
    """
    class CostsResult(NamedTuple):
        total_costs: list[Item]
        excess_items: list[Item]
        intermediate_history: list[Item]
    
    @staticmethod
    def get_total_costs(recipes: RecipeGroup, items: Item | list[Item]) -> CostsResult:
        """アイテムの加工をシミュレーションし、総コストを計算する

        Args:
            recipes (RecipeGroup): シミュレーションに用いるレシピグループ
            items (Item|list[Item]): シミュレーション対象のアイテムまたはアイテムのリスト

        Returns:
            CostsResult: 総コスト、余剰品、中間素材履歴を含む`CostsResult`インスタンス
        """
        
        total_costs: dict[str, Item] = {}
        excess_items: dict[str, Item] = {}
        intermediate_history: dict[str, Item] = {}
        processing_queue: dict[str, Item] = {}
        
        if isinstance(items, Item):
            items = [items]
        
        # 要求されたアイテムをすべて加工キューに追加
        for item in items:
            processing_queue.setdefault(item.name, Item(item.name, 0)).quantity += item.quantity
        
        # 加工キューが空になるまで続ける
        while processing_queue:
            _, item = processing_queue.popitem()
            recipe = recipes.get_recipe(item.name)
            
            # レシピが存在しない場合、総コストプールに追加し次のアイテムへ
            if not recipe:
                total_costs.setdefault(item.name, Item(item.name, 0)).quantity += item.quantity
                continue
            
            # レシピが存在する場合、まずは余剰品プールから消費可能なだけ消費
            # このとき、一度に消費されるのは、レシピの主産物の個数個ずつとなる
            if item.name in excess_items:
                extra_item = excess_items[item.name]
                while recipe.main_product.quantity <= extra_item.quantity and recipe.main_product.quantity <= item.quantity:
                    extra_item.quantity -= recipe.main_product.quantity
                    item.quantity -= recipe.main_product.quantity
            
            # 次に、必要な材料を計算し、加工キューに追加
            actual_quantity = IngredientTree.get_required_quantity(item.quantity, recipe.main_product.quantity)
            process_times = actual_quantity // recipe.main_product.quantity
            for ingredient in recipe.ingredients:
                processing_queue.setdefault(ingredient.name, Item(ingredient.name, 0)).quantity += ingredient.quantity * process_times
            
            # 同様に副産物を余剰品プールに追加
            for byproduct in recipe.byproducts:
                excess_items.setdefault(byproduct.name, Item(byproduct.name, 0)).quantity += byproduct.quantity * process_times
            
            # もともと要求されていたアイテム分を中間素材履歴に追加
            intermediate_history.setdefault(item.name, Item(item.name, 0)).quantity += item.quantity
            
            # 余分に作成されたアイテム分を余剰品プールに追加
            if actual_quantity > item.quantity:
                excess_items.setdefault(item.name, Item(item.name, 0)).quantity += actual_quantity - item.quantity
        
        # 総コストプールと余剰品プール、中間素材履歴をそれぞれリストに変換して返す
        total_costs_list = sorted(list(total_costs.values()), key=lambda x: x.quantity, reverse=True)
        excess_items_list = sorted(list(excess_items.values()), key=lambda x: x.quantity, reverse=True)
        intermediate_history_list = list(intermediate_history.values())
        return RecipeSimulator.CostsResult(
            total_costs_list,
            excess_items_list,
            intermediate_history_list,
        )


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
        result = RecipeSimulator.get_total_costs(recipes, item)
        print("総コスト:", ", ".join([str(item) for item in result.total_costs]))
        print("余り物:", ", ".join([str(item) for item in result.excess_items]) or "-")
        print("中間素材履歴:", ", ".join([str(item) for item in result.intermediate_history]))

    calc(recipes, Item("Cake", 1))
    calc(recipes, Item("Cake", 5))
    
    print()
    
    calc(recipes, Item("Wooden Pickaxe", 1))
    calc(recipes, Item("Wooden Pickaxe", 2))
    calc(recipes, Item("Wooden Pickaxe", 11))
    
