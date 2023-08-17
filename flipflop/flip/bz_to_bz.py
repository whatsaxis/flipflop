"""
BZ to BZ Module

Used for the classic flipping method of placing buy and sell orders for a profit margin.
"""

from flipflop.bz import BazaarSession
from flipflop.structure import BZToBZFlip

from flipflop.utils.helpers import flip


@flip(BZToBZFlip)
def get_order_flip(item_id: str):
    """
    Get the profit obtained from buying and subsequently selling an item.

    Does **not** ignore ``settings.INSTANT_BUY`` and ``settings.INSTANT_SELL``, though it is *strongly* recommended
    that both these settings be on ``True`` for this type of flip.
    """

    with BazaarSession() as session:

        session.buy(item_id)
        sale_price = session.sell(item_id)

        return item_id, session.coins, sale_price
