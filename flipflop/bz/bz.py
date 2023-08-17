"""
Bazaar Module

A module responsible for obtaining prices of various materials.
"""

from flipflop.api import fetch_bz
from flipflop.utils.helpers import to_tuple


def is_bz_item(item_id: str):
    """Returns whether an item is listed on the Bazaar or not."""

    return item_id in fetch_bz()


def is_obtainable(item_id: str, *, ignore_item=False):
    """
    Returns whether an item is obtainable through the Bazaar.

    Accepts an optional `ignore_item` parameter, used to check explicitly if the item is craftable on the Bazaar, and
    not just listed on it.

    Recursively decomposes items into crafting materials until all materials are Bazaar obtainable, or fails if a
    material is non-craftable and non-listable.
    """

    from flipflop.flip.craft import is_craftable, get_craft_materials

    # Check if the item is on the BZ
    if not ignore_item and is_bz_item(item_id):
        return True

    # Check if it can be decomposed into materials through a recipe
    if is_craftable(item_id):
        return is_recipe_obtainable(to_tuple(get_craft_materials(item_id)))

    return False


def is_decomposable(item_id: str):
    """
    Returns whether the item can be crafted from solely materials found on the Bazaar. Notably, ignores whether the
    item itself is actually listed on the Bazaar.

    Helper function to calling `is_obtainable()` with the `ignore_item` parameter set to `True`.
    """

    return is_obtainable(item_id, ignore_item=True)


def is_recipe_obtainable(materials: tuple[tuple[str, int]]):
    """
    Returns whether a list of materials (coined recipe, for this use case - the actual slots in the crafting table are
    arbitrary) is obtainable from the Bazaar.
    """

    return all(
        is_obtainable(mat)

        for mat, _ in materials
    )


def get_buy_volume(item_id: str):
    """Returns the weekly instant buy volume for the specific item."""

    return fetch_bz()[item_id]['quick_status']['buyMovingWeek']


def get_sell_volume(item_id: str):
    """Returns the weekly instant sell volume for the specific item."""

    return fetch_bz()[item_id]['quick_status']['sellMovingWeek']
