"""
NPC Module

Computes the profits from flipping to NPCs, accounting for the daily limit.
"""


from flipflop.api import fetch_item_data
from flipflop.flip.craft import get_bz_materials
from flipflop.structure import NPCFlip
from flipflop.utils.helpers import flip, to_tuple


def is_npc_sellable(item_id: str):
    """Returns whether an item can be sold to NPCs or not."""

    return 'npc_sell_price' in fetch_item_data()[item_id].keys()


def get_npc_price(item_id: str):
    """Returns the NPC sell price of an item."""

    if not is_npc_sellable(item_id):
        raise Exception(f'Cannot determine NPC sell price of `{ item_id }`! Item cannot be sold to NPC!')

    return fetch_item_data()[item_id]['npc_sell_price']


@flip(NPCFlip)
def get_npc_flip(item_id: str):
    """
    Returns the profit from NPC flipping an item.

    For Bazaar items, they are directly sold to NPCs.
    For other items, it is checked whether they can be crafted from the Bazaar, and uses that price.
    """

    from flipflop.bz import BazaarSession, is_bz_item, is_obtainable

    # Basic checks

    if not is_obtainable(item_id):
        raise Exception(f'Cannot calculate NPC flip! Item `{ item_id }` is not obtainable from the Bazaar!')

    if not is_npc_sellable(item_id):
        raise Exception(f'Cannot calculate NPC flip! Item `{ item_id }` cannot be sold to NPCs!')

    is_bz = is_bz_item(item_id)

    with BazaarSession() as session:

        # Account for NPC sell revenue

        sell_price = session.sell(item_id, npc=True)

        # !
        # Bazaar Items
        # !

        if is_bz:
            session.buy(item_id)

            return item_id, session.coins, sell_price

        # !
        # Other Items
        # #

        for mat, qty in to_tuple(get_bz_materials(item_id)):
            session.buy(mat, qty)

        return item_id, session.coins, sell_price
