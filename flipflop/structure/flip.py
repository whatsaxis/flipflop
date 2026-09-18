import abc

from flipflop.bz import get_buy_volume, get_sell_volume


class Flip(abc.ABC):
    """Base class for Flip() objects."""

    item: str
    profit: int

    buy_volume: int
    sell_volume: int

    def __init__(self, item_id: str, cost: int, profit: int):
        self.item = item_id

        self.cost = cost
        self.profit = profit

    @property
    @abc.abstractmethod
    def metric(self):
        raise NotImplementedError('Classes derived from Flip() need a metric property (X.metric) to be implemented!')

    '''Internals'''

    #
    # Comparison
    #

    def __gt__(self, other):
        return self.metric > other.metric

    def __ge__(self, other):
        return self.metric >= other.metric

    def __lt__(self, other):
        return self.metric < other.metric

    def __le__(self, other):
        return self.metric <= other.metric
    #
    # Formatting
    #

    def __str__(self):
        s = f'{ self.__class__.__name__ }['

        for attr, value in self.__dict__.items():
            if attr.startswith('__'):
                continue

            s += f'\n    { attr }: { value }'

        # TODO Ew
        for info, value in {
            'instabuy_vol_7d': get_buy_volume(self.item),
            'instasell_vol_7d': get_sell_volume(self.item),
            'metric': self.metric
        }.items():
            s += f'\n    { info }: { value }'

        s += '\n]'

        return s

    def __repr__(self):
        return str(self)
