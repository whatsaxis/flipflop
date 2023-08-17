"""
Settings File

A collection of settings, options, and constants that control how FlipFlop operates.
"""

import os
import enum


'''
File
'''

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(ROOT_DIR, 'cache')

# In order to regenerate the recipes, use a GitHub directory downloader
# to download the NotEnoughUpdates /items folder, containing item crafting data.
# Link: [https://github.com/NotEnoughUpdates/NotEnoughUpdates-REPO/tree/master/items]
RECIPES_PATH = None

'''
API
'''


class Modules(enum.Enum):

    # Format:
    #   Module  = Save Path

    Bazaar    = 'bz.json'
    ItemData  = 'item_data.json'
    Recipes   = 'recipes.json'


# Whether to use cached data or to regenerate all files
CACHE = True

# Modules to regenerate. Ignored if ``CACHE = False``.
REGENERATE_CACHE = (Modules.Bazaar,)

'''
Profit Calculation
'''

# BZ scales prices by 4% on instant buy orders, to account for small fluctuations in prices
# so that the buy order is not restarted; despite coins are refunded, this is still accounted for
USE_INSTA_BUY_UPSCALE = False
INSTA_BUY_UPSCALE_PERCENTAGE = 4

# Sell tax percentage
TAX_PERCENTAGE = 1.125

# NPC Daily sale limit
NPC_DAILY_LIMIT = 200_000_000

# INSTANT BUY OPTION
#   Setting to use instant buy in unit calculations.
#
# > True
#    Uses instant buy prices (sell orders) for computing the unit cost of items
#
#    + No wait times for materials
#    - Higher prices
#    - Runs a risk of market manipulation
#
#
# > False
#    Uses buy order prices for computing the unit cost of items.
#
#    + Saves coins
#    - Longer wait times, particularly on lower volume items
#
# In all cases, it is strongly recommended to double-check price histories
# when dealing with high-value items.

USE_INSTA_BUY = False

# INSTANT SELL OPTION
#   Setting to use instant sell in item flip calculations.
#
# > True
#    Uses instant sell prices for computing flip profits.
#
#    + No wait times for selling flips
#    - Lower profits
#
# > False
#     Uses sell order prices for computing flip profits.
#
#     + Higher profits
#     + Variety of flip selection
#     - Longer wait times

USE_INSTA_SELL = True

'''
Computed Settings

[!] Do NOT change these unless you know what you are doing!
'''

INSTA_BUY_UPSCALE_MULT = (1 + INSTA_BUY_UPSCALE_PERCENTAGE / 100) \
    if USE_INSTA_BUY_UPSCALE \
    else 1

TAX_MULT = 1 - TAX_PERCENTAGE / 100
