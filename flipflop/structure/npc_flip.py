from flipflop.structure.flip import Flip

from settings import NPC_DAILY_LIMIT


class NPCFlip(Flip):
    """
    NPC Flip class, encompassing data about an NPC flip.

    Includes the maximum volume and profit that one can purchase and sell to NPCs without exceeding the daily limit.
    """

    npc_sell_price: int

    max_daily_volume: int
    max_daily_profit: int

    def __init__(self, item_id: str, profit: int, npc_sell_price: int):
        super().__init__(item_id, profit)

        self.npc_sell_price = npc_sell_price

        self.max_daily_volume = NPC_DAILY_LIMIT // npc_sell_price
        self.max_daily_profit = self.max_daily_volume * profit
