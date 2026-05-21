# Ownership, Icons, and Mod Structure

## Ownership Structure

The mod currently defines separate ownership PMs for the two housing-building categories:

- Rental developer: private owner / national housing bureau
- Ownership developer: private developer / publicly traded real-estate company

The goal is not to create a completely new ownership system, but to provide clearer institutional switching for housing within vanilla framework constraints. Private modes strengthen capitalist dividends and market-driven operation; public or publicly traded modes simulate state management and finance-driven capital expansion respectively.[6]

## Current Icon Strategy

The mod's art implementation has three layers:

1. Goods icons: custom-generated, for `rented_housing` and `owned_housing`.
2. Building icons: custom-generated, for the two housing buildings.
3. Production method / ownership icons: reused vanilla Victoria 3 icon assets to reduce production cost and preserve UI consistency with vanilla style.[9][6]

## Production Method Icon Reuse Strategy

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
