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


@cache_json(settings.Modules.Recipes)
def fetch_recipes():
    """Fetch the item recipes from the NEU item compendium."""

    recipes = {}

    for item_file in os.listdir(settings.RECIPES_PATH):
        with open(os.path.join(settings.RECIPES_PATH, item_file), 'r') as f:
            data = json.loads(f.read())

            item_id = data['internalname']
            recipe = data.get('recipe', None)

            recipes[item_id] = recipe

    return recipes
