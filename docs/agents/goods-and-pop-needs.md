# Goods and Pop Needs

## Added Goods

| Good Key | Meaning | Good Properties | Design Notes |
|---|---|---|---|
| `rented_housing` | Rental housing | Local good, locally priced | Represents rent, occupancy cost, and basic residential upkeep, mainly for low-wealth and lower-middle-wealth Pops.[1][3] |
| `owned_housing` | Owner-occupied housing | Local good, locally priced | Represents mortgage, maintenance, property services, and ownership administration costs, mainly for upper-middle-wealth and high-wealth Pops.[1][2] |

## Goods Design Principles

`rented_housing` and `owned_housing` are not literal physical houses. They are abstract economic units for occupying and maintaining housing. This approach is used because Pop goods consumption in Victoria 3 is inherently cyclical, so housing must be designed as continuously consumed service/cost rather than as a one-time asset purchase.[2]

Housing goods follow the `local = yes` design logic, similar to vanilla Services, Transportation, and Electricity, with price formation primarily inside each state.[1][3] This ensures different states can experience independent housing tightness—for example, high housing prices in industrial states and lower prices in remote states—improving the economic readability of urbanization and migration.[3]

## Pop Needs and Wealth Stratification

Housing needs keep two demand directions to express wealth preference, but both directions now allow rent/ownership substitution inside the same need pool:

- `popneed_rented_housing` remains rent-led, and still carries a clear low-to-mid wealth orientation.
- `popneed_owned_housing` remains ownership-led, and still strengthens as wealth rises.
- Final rent-vs-own allocation is determined jointly by wealth preference and state-local price/supply conditions, so rich Pops can still rent when rental housing is the better market option.

This does not split housing into multiple goods such as "cheap houses" and "luxury houses." Instead, it keeps the rent/ownership binary structure and expresses internal layering through wealth curves, substitution shares, and building input structures. This balances complexity and gameplay usability.[2]
