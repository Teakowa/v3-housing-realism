# Overview and Goals

## Project Overview

Housing Realism is a housing-economy mod for *Victoria 3*. Its core goal is to separate "housing" from the abstract background of standard of living and rebuild it as a producible, consumable, locally priced economic object.[1][2][3]

The mod currently uses two added goods to represent housing consumption: `rented_housing` for rental housing, and `owned_housing` for owner-occupied housing. Both are designed as local goods so each state has independent housing supply-demand dynamics and price changes, rather than joining one unified national market flow.[1][3]

By design, this mod does not try to bypass Victoria 3's cyclical Pop goods-consumption mechanism. Instead, it follows vanilla `buy_packages` and `pop needs` logic and reinterprets housing as continuous "residential cost" and "ownership cost." This means "buying a home" is not a one-time purchase; it is abstracted as long-term spending such as mortgage payments, property management, maintenance, and ownership administration.[2][1]

## Core Design Goals

The design goals can be summarized in four points:

- Make housing an explicit economic variable instead of being implicitly absorbed by the standard-of-living system.[2]
- Create clear housing-consumption stratification across wealth levels: lower-wealth Pops lean toward rental housing, while higher-wealth Pops lean toward owner-occupied housing.[2]
- Make real-estate prices fluctuate independently at the state level to reflect urbanization, population density, and local supply-demand pressure.[1][3]
- Link the housing sector with existing vanilla industry chains such as furniture, porcelain, services, and electricity, instead of isolating it.[4][5]

## Design Rationale

Directly splitting housing into multiple consumer-goods tiers could theoretically represent more layers, but it would significantly increase good count, building count, and balancing complexity. The current approach keeps two housing goods and expresses high-end differences mainly through production methods, input chains, and service components in ownership housing buildings, which is better for long-term maintainability.[1][4]
