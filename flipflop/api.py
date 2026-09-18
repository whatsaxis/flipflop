"""
Hypixel API Interface

An interface for fetching and formatting raw Hypixel API data.
"""

import os
import json
import requests

import settings

from flipflop.utils.helpers import cache_json

BZ_ENDPOINT = 'https://api.hypixel.net/skyblock/bazaar'
ITEMS_ENDPOINT = 'https://api.hypixel.net/resources/skyblock/items'


@cache_json(settings.Modules.Bazaar)
def fetch_bz():
    """Fetch the data from the Bazaar."""

    return requests.get(BZ_ENDPOINT).json()['products']


@cache_json(settings.Modules.ItemData)
def fetch_item_data():
    """Fetch the item data from the SkyBlock resource service."""

    # `id` attribute maintained in the data, in case iteration of only the values takes place. Also, I'm lazy :3
    return {
        item['id']: item
        for item in requests.get(ITEMS_ENDPOINT).json()['items']
    }


# TODO Move elsewhere
def clean_recipes(*recipes):
    """Check if a recipe is a craft flip or not."""

    recipes_out = []

    for recipe in recipes:
        if recipe.get('type', 'crafting') == 'crafting':
            recipes_out.append(recipe)

    return recipes_out


@cache_json(settings.Modules.Recipes)
def fetch_recipes():
    """Fetch the item recipes from the NEU item compendium."""

    recipes = {}

    for item_file in os.listdir(settings.RECIPES_PATH):
        with open(os.path.join(settings.RECIPES_PATH, item_file), 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

            item_id = data['internalname']

            # TODO Change all of the Nones to use []

            recipe_single = data.get('recipe', None)
            recipes_many = data.get('recipes', None)

            if recipe_single is not None:
                recipe = clean_recipes(recipe_single)
            elif recipes_many is not None:
                recipe = clean_recipes(*recipes_many)
            else:
                recipe = []

            recipes[item_id] = recipe

    return recipes
