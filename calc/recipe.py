from calc.item import Item


class Recipe:
    """アイテムとそれに必要な材料、過程で生じる副産物を表すクラス"""

    def __init__(
        self, main_product: Item, ingredients: list[Item], byproducts: list[Item] = []
    ):
        """レシピを初期化する

        Args:
            main_product (Item): 主産物となるアイテム
            ingredients (list[Item]): 必要な材料となるアイテムのリスト
            byproducts (list[Item], optional): 過程で生じる副産物となるアイテムのリスト。省略すると`[]`。
        """
        self.main_product = main_product
        self.ingredients = ingredients
        self.byproducts = byproducts
