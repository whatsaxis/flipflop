from flipflop.api import fetch_bz
from flipflop.flip import get_craft_flip, get_npc_flip, get_order_flip


BZ_PRODUCTS = fetch_bz().keys()

craft_flips = []
order_flips = []
npc_flips = []

for product in BZ_PRODUCTS:
    try:
        cflip = get_craft_flip(product)
        craft_flips.append(cflip)
    except Exception:
        # print('No craft flip for ', product)
        pass

    try:
        oflip = get_order_flip(product)
        order_flips.append(oflip)
    except Exception:
        # print('No order flip for ', product)
        pass

    try:
        npc_flip = get_npc_flip(product)
        npc_flips.append(npc_flip)
    except Exception as e:
        # print(e)
        pass


from pprint import pp

N = 5

print(f'------------------- Craft flips (best { N }) -------------------')
pp(sorted(craft_flips, reverse=True)[:5])

print()
print(f'------------------- Direct flips (best { N }) -------------------')
pp(sorted(order_flips, reverse=True)[:5])
