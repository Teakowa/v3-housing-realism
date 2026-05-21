# Buildings and Production Methods

## Building List

The current design includes two core buildings:

| Building Key | Chinese Positioning | Purpose |
|---|---|---|
| `building_hrro_rental_developer` | Rental Housing District | Produces `rented_housing`, mainly serving low-wealth and lower-middle-wealth housing demand. |
| `building_hrro_owned_developer` | Homeownership Housing District | Produces `owned_housing`, mainly serving upper-middle-wealth and high-wealth housing demand. |

Both are positioned as urban economic buildings and use different production methods to represent technological progression, material upgrades, and increasing service intensity.[6][5]
The internal building keys are unchanged and still use the `building_hrro_*_developer` naming for compatibility.

## Building Design Philosophy

The rental housing district leans toward dense urban housing supply, representing low-rent blocks, apartment blocks, and high-rise rentals where residential density is central. The homeownership housing district leans toward a composite "real-estate development + sales + supporting services" industry. It consumes not only construction materials but also higher-end lifestyle goods and services, modeling the stronger capital and service-sector characteristics of real-estate development.[6][5]

## Rental Housing District Production Methods

| PM Key | Stage Positioning | Core Inputs | Core Characteristics |
|---|---|---|---|
| `pm_hrro_tenement` | Low-end rental | Wood, small amount of furniture | Cheap, dense, basic maintenance, mainly for working-class residents. |
| `pm_hrro_apartment` | Mid-end rental | Wood, steel, glass, small amount of furniture | More modern urban apartments with higher output and increased technology/management input. |
| `pm_hrro_highrise_rental` | High-end/high-density rental | Steel, glass, furniture, electricity | High-rise and core-urban form, emphasizing space efficiency. |

Rental buildings are allowed to consume furniture, but intentionally at a low level to represent basic interior support without turning rental housing into heavily decorated premium housing.[4]

## Homeownership Housing District Production Methods

| PM Key | Stage Positioning | Core Inputs | Core Characteristics |
|---|---|---|---|
| `pm_hrro_rowhouse` | Entry-level owner housing | Wood, glass, furniture | Targets early middle class; represents basic owner-occupied housing. |
| `pm_hrro_suburban_villa` | Mid-end owner housing | Steel, glass, furniture, porcelain, services | Stronger quality-of-life and service-chain dependence; models suburban villas and middle-class upgrade housing. |
| `pm_hrro_luxury_estate` | High-end owner housing | Steel, glass, luxury furniture, porcelain, services, electricity | Premium development projects emphasizing luxury consumption and service-heavy operations. |

Mid/high-end ownership PMs consume porcelain and services to reflect stronger dependence of owner-occupied housing on interior quality, property management, ownership transactions, and related support services.[4][5]

## Meaning of Service Inputs

Introducing the `services` good to ownership housing buildings does not mean housing itself is a pure service industry. It abstracts real-world property management, title registration, transaction brokerage, financial processing, and maintenance systems.[5] This design creates stronger linkage between ownership housing and the urban service sector, while limiting `services` to mid/high-tier PMs to avoid making low-end housing fully dependent on service supply.[5]

## Employment Structure

### Rental Housing District

Rental buildings still lean toward construction and urban management overall, with higher laborer share and lower shopkeeper/engineer share. As PMs progress from tenements to high-rise rentals, laborer share declines while machinist/engineer share increases, reflecting rising technical and equipment requirements.

### Homeownership Housing District

Ownership buildings are intentionally designed to be more service- and capital-operation-oriented. Entry-level ownership housing still keeps a relatively high laborer share, but at mid/high tiers, the shares of shopkeepers, capitalists, engineers, and machinists rise significantly while laborer share drops. This better matches a "real-estate development + sales + service operations" industry shape rather than a pure construction-crew logic.

### Occupation Field Notes

This mod keeps the vanilla occupation key `machinists`, interpreted in Chinese semantics as "技工" rather than "机械师." This is to stay aligned with Victoria 3's vanilla occupation system and avoid introducing non-native occupation types.[7][8]
