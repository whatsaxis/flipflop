# FlipFlop

A Python-based marketplace analysis and optimisation tool for finding and ranking profitable trading opportunities in the Hypixel SkyBlock Bazaar.

The Bazaar in Hypixel SkyBlock is an in-game stock market system used for bulk trading items.

## What it does

FlipFlop currently supports several types of Bazaar opportunities, including:

* Direct flips: buy an item through a buy order and resell it through a sell order
* Crafting flips: buy the materials needed to craft an item, then sell the crafted result

Rather than simply looking for the largest raw profit, FlipFlop assigns each opportunity a score based on factors such as:

* absolute profit
* profit margin
* market liquidity
* number of materials required
* expected transaction complexity

## Why I built it

FlipFlop started as a project to make coins in a video game, though ended up being a fun way to experiment with ideas from trading and optimisation such as:

* arbitrage and bid/ask spreads
* profit and return
* profit margins
* liquidity
* transaction costs / execution constraints
* recursive bill-of-materials analysis
* make-or-buy optimisation
* heuristic opportunity scoring

The scoring system is more involved than just picking the highest profit trade. It combines profit, margin and, liquidity, while the crafting system considers the cost and availability of every input needed to produce an item.

Hypixel Skyblock is a game economy, but it gives me a nice sandbox for experimenting with market analysis, optimisation and quantitative decision-making.

See below for an in-depth analysis of the implementation details!

## Direct Bazaar Flips

A direct flip exploits the difference between the effective acquisition and selling prices of an item.

The ranking metric combines profit, margin, and two-sided market volume.

### Opportunity Score

For a direct flip, the score is:

$$
S =
[\ln(1+P)]^{0.8}
[\ln(1+V)]^{1.0}
\left(
\frac{M}{M+M_t}
\right)^{0.5}
$$

where:

* $P$ = absolute profit
* $V$ = effective market volume
* $M$ = profit margin
* $M_t$ = target profit margin

The target margin is currently:

$$
M_t = 0.2
$$

### Profit

Raw profit is log-scaled:

$$
P_{\mathrm{score}}=\ln(1+P)
$$

This prevents extremely large-profit items from completely dominating the ranking.

The exponent of \(0.8\) gives profit substantial importance without making it overwhelmingly more important than the other factors.

### Liquidity

A flip is only useful if both sides of the transaction can actually be completed.

FlipFlop estimates effective volume using the geometric mean of buy and sell volume:

$$
V=\sqrt{V_{\mathrm{buy}}V_{\mathrm{sell}}}
$$

This penalises asymmetric markets where one side has substantial volume but the other does not.

The resulting volume is also log-scaled:

$$
V_{\mathrm{score}}=\ln(1+V)
$$

### Margin

Absolute profit alone can be misleading. A flip making 100,000 coins from a 10,000,000 coin investment is quite different from one making 100,000 coins from a 200,000 coin investment.

The margin term is:

$$
\left(
\frac{M}{M+M_t}
\right)^{0.5}
$$

This increases with margin but gradually saturates once the margin is comfortably above the target.

---

## Crafting Flips

Crafting flips add another layer of optimisation.

Instead of simply comparing the Bazaar prices of an item, FlipFlop determines what it would actually cost to produce the item from materials that can be obtained through the Bazaar.

For example:

```text
                 Target Item
                      │
                    Recipe
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
    Intermediate A            Material B
          │
       Recipe
          │
     ┌────┴────┐
     ↓         ↓
 Material C  Material D
```

The system recursively decomposes intermediate crafting materials until it reaches materials that can be directly obtained through the Bazaar.

### Recursive Bill of Materials

The crafting system:

1. Reads the recipe for an item
2. Extracts the required ingredients and quantities
3. Checks whether each ingredient is directly available through the Bazaar
4. Recursively decomposes craftable intermediate ingredients
5. Aggregates identical materials using `Counter`
6. Calculates the total acquisition cost
7. Compares that cost with the expected selling value
8. Ranks the resulting opportunity

This effectively produces a Bazaar-accessible bill of materials for each craftable item.

For example, if an item requires an intermediate item which itself requires several materials, FlipFlop expands the dependency tree until it reaches purchasable inputs rather than treating the intermediate item's listed price as the only possible route.

## Crafting Opportunity Score

Crafting flips use the same general ideas of profit, margin and liquidity, but introduce additional factors.

The score is based on:

$$
S =
[\ln(1+P)]^{0.8}
[\ln(1+V_{\mathrm{effective}})]^{1.0}
e^{1-N}
\left(
\frac{M}{M+M_t}
\right)^{0.5}
$$

where:

* $P$ = expected profit
* $V_{\mathrm{effective}}$ = effective trading volume
* $N$ = number of distinct required materials
* $M$ = profit margin
* $M_t$ = target margin

### Material complexity

Crafting an item from many different materials introduces additional transaction overhead.

FlipFlop therefore applies:

$$
C=e^{1-N}
$$

where \(N\) is the number of distinct materials.

For example:

| Materials | Complexity factor |
| --------: | ----------------: |
|         1 |             1.000 |
|         2 |             0.368 |
|         3 |             0.135 |
|         4 |             0.050 |

This strongly penalises recipes that require a large number of independent market transactions.

### Liquidity bottlenecks

Crafting liquidity is slightly more complicated than direct-flip liquidity because every input has to be acquired before the craft can happen.

The system therefore estimates effective material volume using a harmonic mean, so a single difficult-to-source ingredient can bottleneck the entire flip.

The final product's trading volume is then incorporated as well (we need to be able to sell it after all).

In other words, a theoretically profitable recipe is not considered equally attractive if one of its inputs is extremely difficult to acquire or the finished product is difficult to sell.
