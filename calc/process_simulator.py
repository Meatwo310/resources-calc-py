from typing import NamedTuple
from calc.ingredient_tree import IngredientTree
from calc.item import Item
from calc.recipe_group import RecipeGroup


class ProcessSimulator:
    """レシピを用いた加工をシミュレーションするクラス"""

    class CostsResult(NamedTuple):
        total_costs: list[Item]
        excess_items: list[Item]
        intermediate_history: list[Item]

    @staticmethod
    def get_total_costs(recipes: RecipeGroup, items: Item | list[Item]) -> CostsResult:
        """アイテムの加工をシミュレーションし、総コストを計算する

        レシピを参照しながら4種類の内部的なプールを用いて、
        アイテム加工のシミュレーションを行い、総コスト、余剰品、中間素材履歴を返す。
        計算はレシピの主産物が最小になるよう行われる。
        副産物も計算に使用されるが、主産物と違い最小になるよう調整されるわけではない。

        Args:
            recipes (RecipeGroup): シミュレーションに用いるレシピグループ
            items (Item|list[Item]): シミュレーション対象のアイテムまたはアイテムのリスト

        Returns:
            CostsResult: 総コスト`total_costs`、余剰品`excess_items`、中間素材履歴`intermediate_history`を含む`CostsResult`インスタンス
        """

        total_costs: dict[str, Item] = {}
        excess_items: dict[str, Item] = {}
        intermediate_history: dict[str, Item] = {}
        processing_queue: dict[str, Item] = {}

        if isinstance(items, Item):
            items = [items]

        # 要求されたアイテムをすべて加工キューに追加
        for item in items:
            processing_queue.setdefault(
                item.name, Item(item.name, 0)
            ).quantity += item.quantity

        # 加工キューが空になるまで続ける
        while processing_queue:
            _, item = processing_queue.popitem()
            recipe = recipes.get_recipe(item.name)

            # レシピが存在しない場合、総コストプールに追加し次のアイテムへ
            if not recipe:
                total_costs.setdefault(
                    item.name, Item(item.name, 0)
                ).quantity += item.quantity
                continue

            # レシピが存在する場合、まずは余剰品プールから消費可能なだけ消費
            # このとき、一度に消費されるのは、レシピの主産物の個数個ずつとなる
            if item.name in excess_items:
                extra_item = excess_items[item.name]
                while (
                    recipe.main_product.quantity <= extra_item.quantity
                    and recipe.main_product.quantity <= item.quantity
                ):
                    extra_item.quantity -= recipe.main_product.quantity
                    item.quantity -= recipe.main_product.quantity

            # 次に、必要な材料を計算し、加工キューに追加
            actual_quantity = IngredientTree.get_required_quantity(
                item.quantity, recipe.main_product.quantity
            )
            process_times = IngredientTree.get_process_times(
                item.quantity, recipe.main_product.quantity
            )
            for ingredient in recipe.ingredients:
                processing_queue.setdefault(
                    ingredient.name, Item(ingredient.name, 0)
                ).quantity += ingredient.quantity * process_times

            # 同様に副産物を余剰品プールに追加
            for byproduct in recipe.byproducts:
                excess_items.setdefault(
                    byproduct.name, Item(byproduct.name, 0)
                ).quantity += byproduct.quantity * process_times

            # もともと要求されていたアイテム分を中間素材履歴に追加
            intermediate_history.setdefault(
                item.name, Item(item.name, 0)
            ).quantity += item.quantity

            # 余分に作成されたアイテム分を余剰品プールに追加
            if actual_quantity > item.quantity:
                excess_items.setdefault(item.name, Item(item.name, 0)).quantity += (
                    actual_quantity - item.quantity
                )

        # 総コストプールと余剰品プール、中間素材履歴をそれぞれリストに変換して返す
        total_costs_list = sorted(
            list(total_costs.values()), key=lambda x: x.quantity, reverse=True
        )
        excess_items_list = sorted(
            list(excess_items.values()), key=lambda x: x.quantity, reverse=True
        )
        intermediate_history_list = list(intermediate_history.values())
        return ProcessSimulator.CostsResult(
            total_costs_list,
            excess_items_list,
            intermediate_history_list,
        )
