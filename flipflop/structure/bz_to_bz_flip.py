import math

from flipflop.bz import get_buy_volume, get_sell_volume
from flipflop.structure.flip import Flip


class BZToBZFlip(Flip):
    """Craft Flip class, encompassing data about a craft flip."""

    profit_margin: float
    metric: float

    def __init__(self, item_id: str, cost: int, profit: int):
        super().__init__(item_id, cost, profit)

        self.profit_margin = profit / cost

    @property
    def metric(self):
        # Metric calculation
        #
        # Computing how good a flip is. Includes:
        #   - Absolute profit (we don't care if the margin is really good, if the profit is tiny)
        #   - Margin (if something is really expensive for a small profit, it may not be worth it)
        #   - Volume (how long will it actually take to fill buy/sell orders)
        #
        # The score is of the form
        #     score = log(1 + P)^α * log(1 + V_geometric)^β * (M / [M + M_target])^γ
        #
        # Where P is price, V_geometric = sqrt(V_buy * V_sell), M is margin, M_target is the desired profit margin

        if self.profit < 0:
            return 0.0

        MARGIN_TARGET = 0.2

        profit_score = math.log1p(self.profit)

        # Geometric mean for skewed buy/sell volumes
        volume_gm = math.sqrt(get_buy_volume(self.item) * get_sell_volume(self.item))
        volume_score = math.log1p(volume_gm)

        # TODO Estimated profit/hr

        return (
                profit_score ** 0.8
                * volume_score ** 1.0
                * (self.profit_margin / (self.profit_margin + MARGIN_TARGET)) ** 0.5
        )

