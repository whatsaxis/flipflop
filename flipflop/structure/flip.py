class Flip:
    """Base class for Flip() objects."""

    item: str
    profit: int

    buy_volume: int
    sell_volume: int

    def __init__(self, item_id: str, profit: int):

        from flipflop.bz import get_buy_volume, get_sell_volume

        self.item = item_id
        self.profit = profit

        self.buy_volume = get_buy_volume(item_id)
        self.sell_volume = get_sell_volume(item_id)

    '''Internals'''

    #
    # Comparison
    #

    def __gt__(self, other):
        return self.profit > other.profit

    def __ge__(self, other):
        return self.profit >= other.profit

    def __lt__(self, other):
        return self.profit < other.profit

    def __le__(self, other):
        return self.profit <= other.profit

    #
    # Formatting
    #

    def __str__(self):
        s = f'{ self.__class__.__name__ }['

        for attr, value in self.__dict__.items():
            if attr.startswith('__'):
                continue

            s += f'\n    { attr }: { value }'

        s += '\n]'

        return s

    def __repr__(self):
        return str(self)
