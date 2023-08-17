from flipflop.api import fetch_bz

import settings


class BazaarSession:
    """
    A context manager allowing the ability to manipulate the Bazaar market with a temporary session.
    This involves subtracting purchased items from the supply of the product, and providing an easy interface to do so.
    """

    coins: int

    in_session: bool

    def __init__(self):
        self.in_session = False

    """Context Manager"""

    def __enter__(self):
        self.coins = 0
        self.in_session = True

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        # By design, does NOT reset state upon context manager exit, so that
        # the object's data can be used outside the `with` block

        self.in_session = False

        # NOTE: No value is returned, in order to not suppress any exceptions
        # that may take place within the session.
        #
        # More information on context manager overload behaviour:
        #   [https://stackoverflow.com/a/28158006]

    """Methods"""

    def buy(self, item_id: str, quantity=1):
        """
        Function to buy an item at a certain quantity from the Bazaar.

        Returns the total cost as a negative integer.
        Returns an error if the quantity exceeds the supply of the top 10 orders.
        """

        tax = settings.INSTA_BUY_UPSCALE_MULT \
            if settings.USE_INSTA_SELL \
            else 1

        coins = - tax * self._internal_price(
            item_id=item_id,
            quantity=quantity,

            insta_field='buy_summary',
            order_field='sell_summary',

            use_instant=settings.USE_INSTA_BUY
        )

        self.coins += coins
        return coins

    def sell(self, item_id: str, quantity=1, *, npc=False):
        """
        Function to sell an item at a certain quantity from the Bazaar.

        Returns the total cost as a negative integer.
        Returns an error if the quantity exceeds the supply of the top 10 orders.
        """

        from flipflop.flip.npc import get_npc_price

        if npc:
            coins = get_npc_price(item_id) * quantity
        else:
            coins = settings.TAX_MULT * self._internal_price(
                item_id=item_id,
                quantity=quantity,

                # Instant Selling goes directly to buy orders - thus, the highest price (coins someone is willing to
                # pay) for this is indicative of the current price. Market manipulation is deemed impossible, apart from
                # intentionally confusing bots (unlikely), as who would want to overpay?

                insta_field='sell_summary',
                order_field='buy_summary',

                use_instant=settings.USE_INSTA_SELL
            )

        self.coins += coins
        return coins

    def _internal_price(self, item_id: str, quantity=1, *, insta_field: str, order_field: str, use_instant: bool):
        """
        Internal function to get the buy or sell price of an item from the Bazaar.
        Returns an error if the quantity exceeds the supply of the top 10 orders.
        """

        if not self.in_session:
            raise Exception(
                'Attempting to alter a BazaarSession outside of a session! '
                'Use `with BazaarSession() as session` to create a new session.'
            )

        coins = 0

        # !
        # Buy Order
        # !

        if not use_instant:
            # The API `quick_status` field gives a weighted average of the top 2% of orders. This has the consequence
            # of, in certain circumstances, skewing the prices by very large amounts. Stupid decision on their end,
            # but we have to live with it.

            orders = fetch_bz()[item_id][order_field]

            if not orders:
                raise Exception(f'There are no available orders in field `{ order_field }` for item `{ item_id }`!')

            unit_price = orders[0]['pricePerUnit']

            return unit_price * quantity

        # !
        # Instant Buy
        # !

        orders = fetch_bz()[item_id][insta_field]

        order_idx = 0
        while quantity > 0 and order_idx < len(orders):
            order = orders[order_idx]

            order_qty = order['amount']
            unit_cost = order['pricePerUnit']

            # Buy whole order
            if quantity > order_qty:
                quantity -= order_qty
                coins += unit_cost * order_qty

            # Buy part of order
            elif quantity <= order_qty:
                coins += unit_cost * quantity
                quantity = 0

            order_idx += 1

        if quantity > 0:
            raise Exception('Quantity exceeds supply of first 10 orders!')

        return coins
