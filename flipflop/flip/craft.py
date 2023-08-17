"""
Crafting Module

Used for obtaining materials for craft flips, and optimising the recipe for price.
"""

from collections import Counter

from flipflop.api import fetch_recipes
from flipflop.bz import is_bz_item, is_decomposable
from flipflop.structure import CraftFlip

from flipflop.utils.helpers import flip, multiply, to_tuple


def is_craftable(item_id: str):
    """Returns whether an item can be crafted or not."""

    return fetch_recipes()[item_id] is not None


def get_craft_materials(item_id: str) -> Counter[str]:
    """Returns the materials required to craft an item."""

    if not is_craftable(item_id):
        raise Exception(f'Unable to get craft materials. Item `{ item_id }` is not craftable!')

    # NOTE: One can use `defaultdict(int)` to achieve the same result.
    # An idiomatic expression; equivalent to `lambda: 0`
    frequencies = Counter()

    for craft_slot in fetch_recipes()[item_id].values():
        # Empty slot
        if not craft_slot:
            continue

        # Recipes come in the format of `ITEM_ID:QTY`
        craft_item, qty = craft_slot.split(':')
        frequencies[craft_item] += int(qty)

    return frequencies


def get_bz_materials(item_id: str):
    """
    A recursive version of get_craft_materials(), decomposing items into the simplest recipes where all materials are
    available on the Bazaar.
    """

    if not is_craftable(item_id):
        raise Exception(f'Unable to get Bazaar craft materials. Item `{ item_id }` is not craftable!')

    materials = Counter()

    for mat, qty in get_craft_materials(item_id).items():

        # Is listed on Bazaar
        if is_bz_item(mat):
            materials[mat] += qty

        # NOT on Bazaar, but materials listed on Bazaar
        elif is_decomposable(mat):

            # NOTE: There is a KNOWN bug with this method, to do with an (assumed) oversight in the
            # NEU recipes JSON data.

            # While each item has a recipe, there is no information on how many of each item is actually crafted
            # using said recipe. This causes issues such as returning that, for instance, 3 logs are required to craft 3
            # wooden planks, when it is, in reality, just 1 log, as each log gives 4 wooden planks.

            # However, this is largely insignificant and generally only applies to Vanilla items, so we
            # will just leave it be.

            materials += multiply(get_bz_materials(mat), qty)

        # Oops! Can't obtain a material!
        else:
            raise Exception(
                f'Unable to get craft materials for item `{ item_id }`. '
                f'Material `{ mat }` is not obtainable through the Bazaar!'
            )

    return materials


def is_craft_flippable(item_id: str):
    """
    Returns whether an item is craft flippable on the Bazaar.

    This involves checking whether the item is:

    - Listed on the Bazaar
    - Decomposable into materials which are available on the Bazaar
    """

    return is_bz_item(item_id) and is_decomposable(item_id)


@flip(CraftFlip)
def get_craft_flip(item_id: str):
    """Get the profit, materials, and steps for craft flipping an item."""

    from flipflop.bz import BazaarSession

    # Trivially passes for recursive calls
    if not is_craft_flippable(item_id):
        raise Exception(
            f'Unable to compute craft flip. Item `{ item_id }` is not listed on the Bazaar or is not '
            'obtainable through Bazaar materials!'
        )

    with BazaarSession() as session:

        materials = to_tuple(get_bz_materials(item_id))

        for material, quantity in materials:
            session.buy(material, quantity)

        # Obtain coins from selling the item after crafting to calculate profit
        session.sell(item_id)

        return item_id, session.coins, materials
