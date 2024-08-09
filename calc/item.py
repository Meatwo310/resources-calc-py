class Item:
    """アイテム名と個数を表すクラス"""

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
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return self.name == other.name and self.quantity == other.quantity
