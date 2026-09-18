import math

from flipflop.bz import get_buy_volume, get_sell_volume
from flipflop.structure.flip import Flip


class CraftFlip(Flip):
    """Craft Flip class, encompassing data about a craft flip."""

    materials: tuple[tuple[str, int]]
    profit_margin: float

    def __init__(self, item_id: str, cost: int, profit: int, materials: tuple[tuple[str, int]]):
        super().__init__(item_id, cost, profit)

        self.profit_margin = profit / cost
        self.materials = materials

    @property
    def metric(self):
        # Metric calculation
        #
        # Computing how good a craft flip is. Includes:
        #   - Absolute profit
        #   - Margin
        #   - Number of distinct items needed to craft (>= 3 is BAD)
        #   - Volume (how long will it actually take to fill buy orders of ingredients + to fill sell order of crafted product)
        #
        # The score is of the form
        #     score = log(1 + P)^α * log(1 + V_geometric)^β * (M / [M + M_target])^γ
        #
        # Where P is price, V_geometric = sqrt(V_buy * V_sell), M is margin, M_target is the desired profit margin

        if self.profit < 0:
            return 0.0

        MARGIN_TARGET = 0.2

        # Absolute profit
        profit_score = math.log1p(self.profit)

        # Weighted harmonic mean for volumes of each ingredient
        # TODO This doesn't account for the INSTA_BUY / INSTA_SELL setting
        adjusted_volumes = [
            get_sell_volume(material) / items_per_craft
            for material, items_per_craft in self.materials
        ]

        mats_per_craft = sum(mat[1] for mat in self.materials)

        effective_craft_volume = mats_per_craft / sum(
            1/v for v in adjusted_volumes
        )

        # Volume score combining craft volume AND sell volume of final product
        volume_score = math.log1p(effective_craft_volume * get_buy_volume(self.item))

        # Number of ingredients penalty
        #   f(N) = e^(1 - N)
        #
        #   f(1) = 1.0
        #   f(2) = 0.368
        #   f(3) = 0.135
        #   f(4) = 0.050
        #
        # Greatly punishes craft flips which need many items.
        # TODO This could perhaps be accounted for with an OVERNIGHT option to disregard this, so that it doesn't matter too much.
        complexity = math.exp(1 - len(self.materials))

        return (
                profit_score ** 0.8
                * volume_score ** 1.0
                * complexity
                * (self.profit_margin / (self.profit_margin + MARGIN_TARGET)) ** 0.5
        )
