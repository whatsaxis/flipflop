from flipflop.structure.flip import Flip


class BZToBZFlip(Flip):
    """Craft Flip class, encompassing data about a craft flip."""

    sell_price: int
    profit_margin: float

    def __init__(self, item_id: str, profit: int, sell_price: int):
        super().__init__(item_id, profit)

        self.sell_price = sell_price
        self.profit_margin = profit / sell_price
