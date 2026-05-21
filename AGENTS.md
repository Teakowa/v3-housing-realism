# Housing Realism - Design Reference Document

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

## Goods System

### Added Goods

| Good Key | Meaning | Good Properties | Design Notes |
|---|---|---|---|
| `rented_housing` | Rental housing | Local good, locally priced | Represents rent and basic residential services, mainly for low-wealth and lower-middle-wealth Pops.[1][3] |
| `owned_housing` | Owner-occupied housing | Local good, locally priced | Represents mortgage, maintenance, property services, and ownership administration costs, mainly for upper-middle-wealth and high-wealth Pops.[1][2] |

### Goods Design Principles

`rented_housing` and `owned_housing` are not literal physical houses. They are abstract economic units for occupying and maintaining housing. This approach is used because Pop goods consumption in Victoria 3 is inherently cyclical, so housing must be designed as continuously consumed service/cost rather than as a one-time asset purchase.[2]

Housing goods follow the `local = yes` design logic, similar to vanilla Services, Transportation, and Electricity, with price formation primarily inside each state.[1][3] This ensures different states can experience independent housing tightness—for example, high housing prices in industrial states and lower prices in remote states—improving the economic readability of urbanization and migration.[3]

## Pop Needs and Wealth Stratification

### Consumption Structure

Housing needs use two separate demand directions to express wealth differences:

- `rented_housing` targets low- to lower-middle-wealth Pops, peaking around mid-range wealth and then gradually fading out.
- `owned_housing` appears from the middle class onward and keeps strengthening at high wealth, forming a clear preference for ownership housing.[2]

This does not split housing into multiple goods such as "cheap houses" and "luxury houses." Instead, it uses a rent/ownership binary structure and expresses internal layering through wealth curves and building input structures. This balances complexity and gameplay usability.[2]

### Design Rationale

Directly splitting housing into multiple consumer-goods tiers could theoretically represent more layers, but it would significantly increase good count, building count, and balancing complexity. The current approach keeps two housing goods and expresses high-end differences mainly through production methods, input chains, and service components in ownership housing buildings, which is better for long-term maintainability.[1][4]

## Building System

### Building List

The current design includes two core buildings:

| Building Key | Chinese Positioning | Purpose |
|---|---|---|
| `building_hrro_rental_developer` | Rental Housing Developer | Produces `rented_housing`, mainly serving low-wealth and lower-middle-wealth housing demand. |
| `building_hrro_owned_developer` | Ownership Housing Developer | Produces `owned_housing`, mainly serving upper-middle-wealth and high-wealth housing demand. |

Both are positioned as urban economic buildings and use different production methods to represent technological progression, material upgrades, and increasing service intensity.[6][5]

### Building Design Philosophy

The rental developer leans toward dense urban housing supply, representing low-rent blocks, apartment blocks, and high-rise rentals where residential density is central. The ownership developer leans toward a composite "real-estate development + sales + supporting services" industry. It consumes not only construction materials but also higher-end lifestyle goods and services, modeling the stronger capital and service-sector characteristics of real-estate development.[6][5]

## Production Method Design

### Rental Developer Production Methods

| PM Key | Stage Positioning | Core Inputs | Core Characteristics |
|---|---|---|---|
| `pm_hrro_tenement` | Low-end rental | Wood, small amount of furniture | Cheap, dense, basic maintenance, mainly for working-class residents. |
| `pm_hrro_apartment` | Mid-end rental | Wood, steel, glass, small amount of furniture | More modern urban apartments with higher output and increased technology/management input. |
| `pm_hrro_highrise_rental` | High-end/high-density rental | Steel, glass, furniture, electricity | High-rise and core-urban form, emphasizing space efficiency. |

Rental buildings are allowed to consume furniture, but intentionally at a low level to represent basic interior support without turning rental housing into heavily decorated premium housing.[4]

### Ownership Developer Production Methods

| PM Key | Stage Positioning | Core Inputs | Core Characteristics |
|---|---|---|---|
| `pm_hrro_rowhouse` | Entry-level owner housing | Wood, glass, furniture | Targets early middle class; represents basic owner-occupied housing. |
| `pm_hrro_suburban_villa` | Mid-end owner housing | Steel, glass, furniture, porcelain, services | Stronger quality-of-life and service-chain dependence; models suburban villas and middle-class upgrade housing. |
| `pm_hrro_luxury_estate` | High-end owner housing | Steel, glass, luxury furniture, porcelain, services, electricity | Premium development projects emphasizing luxury consumption and service-heavy operations. |

Mid/high-end ownership PMs consume porcelain and services to reflect stronger dependence of owner-occupied housing on interior quality, property management, ownership transactions, and related support services.[4][5]

### Meaning of Service Inputs

Introducing the `services` good to ownership housing buildings does not mean housing itself is a pure service industry. It abstracts real-world property management, title registration, transaction brokerage, financial processing, and maintenance systems.[5] This design creates stronger linkage between ownership housing and the urban service sector, while limiting `services` to mid/high-tier PMs to avoid making low-end housing fully dependent on service supply.[5]

## Employment Structure Design

### Rental Developer

Rental buildings still lean toward construction and urban management overall, with higher laborer share and lower shopkeeper/engineer share. As PMs progress from tenements to high-rise rentals, laborer share declines while machinist/engineer share increases, reflecting rising technical and equipment requirements.

### Ownership Developer

Ownership buildings are intentionally designed to be more service- and capital-operation-oriented. Entry-level ownership housing still keeps a relatively high laborer share, but at mid/high tiers, the shares of shopkeepers, capitalists, engineers, and machinists rise significantly while laborer share drops. This better matches a "real-estate development + sales + service operations" industry shape rather than a pure construction-crew logic.

### Occupation Field Notes

This mod keeps the vanilla occupation key `machinists`, interpreted in Chinese semantics as "技工" rather than "机械师." This is to stay aligned with Victoria 3's vanilla occupation system and avoid introducing non-native occupation types.[7][8]

## Ownership Structure

The mod currently defines separate ownership PMs for the two housing-building categories:

- Rental developer: private owner / national housing bureau
- Ownership developer: private developer / publicly traded real-estate company

The goal is not to create a completely new ownership system, but to provide clearer institutional switching for housing within vanilla framework constraints. Private modes strengthen capitalist dividends and market-driven operation; public or publicly traded modes simulate state management and finance-driven capital expansion respectively.[6]

## Icons and Art Implementation

### Current Icon Strategy

The mod's art implementation has three layers:

1. Goods icons: custom-generated, for `rented_housing` and `owned_housing`.
2. Building icons: custom-generated, for the two housing buildings.
3. Production method / ownership icons: reused vanilla Victoria 3 icon assets to reduce production cost and preserve UI consistency with vanilla style.[9][6]

### Production Method Icon Reuse Strategy

Current PM icons use vanilla asset paths, for example:

- Basic construction PMs use `pm_simple_construction.dds`
- Modern construction PMs use `pm_modern_construction.dds`
- Electrified/high-rise PMs use `pm_electric_tools.dds`
- Private/public/publicly-traded ownership PMs use vanilla ownership icon paths.[9]

Advantages of this approach are consistent UI appearance, lower workload, and easier functional interpretation by players through existing vanilla experience.[6]

## Mod Structure and Declaration Method

This mod currently follows the newer Victoria 3 mod structure by using `.metadata/metadata.json` for declaration, instead of legacy `.mod` files. This is a required adjustment for newer game versions.

The overall directory structure is roughly:

```text
housing_realism/
├── .metadata/
│   └── metadata.json
├── common/
│   ├── goods/
│   ├── pop_needs/
│   ├── buy_packages/
│   ├── buildings/
│   ├── production_methods/
│   ├── production_method_groups/
│   └── modifier_type_definitions/
├── localization/
└── gui/
```

## Key Tradeoffs in Current Implementation

### Tradeoff 1: Two housing goods instead of a multi-goods tier ladder

The current solution does not continue splitting into final-consumption goods such as "low-rent housing, standard housing, luxury housing." It keeps a fixed binary structure of "rental / ownership" to reduce system complexity and avoid expansion of good count and demand-substitution logic.

### Tradeoff 2: Express high-end differences through production methods

High-end housing differences are mainly represented through PM design rather than additional goods. This allows "high-end housing" to be expressed as more expensive materials, higher-end interior goods, greater service demand, and a more capital/service-oriented employment structure.

### Tradeoff 3: Respect the vanilla cyclical-consumption framework

The current design explicitly accepts Victoria 3's cyclical Pop-consumption logic. Therefore housing is not a one-time purchase but abstracted as long-term continuous housing expenditure. This is the foundation for stable integration into the vanilla system.[2]

## Future Expansion Directions

If deeper expansion is needed in the future, this mod can continue along directions such as:

- Law linkage: let housing policy, welfare laws, and taxation affect rental vs ownership supply structure.
- Regional modifiers: let different states further affect housing cost or supply efficiency through state modifiers.
- Company system: design dedicated company bonuses for real-estate developers.
- Urbanization linkage: bind urban centers, infrastructure, and housing prices more strongly.
- Visualization: add housing-related UI hints that directly show state-level housing prices and supply-demand pressure.

## Implementation Guidance for Other AI Assistants

If other AI assistants continue development later, it is recommended to enforce these principles:

1. Do not introduce good keys or occupation keys that do not exist in vanilla Victoria 3 unless you also provide the full industry-chain and localization support.[4][7]
2. Prefer reusing vanilla icons and vanilla ownership logic to reduce art and compatibility cost.[6][9]
3. In balancing design, always treat housing as "continuous residential cost," not a one-time asset purchase.[2]
4. Keep the overall direction of "rental housing = basic housing, ownership housing = service- and capital-oriented housing," and do not homogenize the two building categories.
5. Confirm requirements before adding changes, because this mod prioritizes maintainability and overall economic-chain coherence rather than single-point feature stacking.

## Conclusion

Housing Realism - Rent & Own currently has a clear design framework: two local housing goods as the core, two housing buildings as supply entities, and wealth stratification plus PM differentiation as the main expression method, integrating housing into Victoria 3's local pricing, industry-chain linkage, and class structure.[1][2][3]

For future development, the key is not to keep expanding the number of goods, but to build more robust balancing, law linkage, and UI presentation around the existing binary structure. This keeps the design clean while ensuring long-term maintainability of the mod.
