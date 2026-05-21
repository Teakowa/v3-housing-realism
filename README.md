# Housing Realism

Housing Realism is a *Victoria 3* economy mod that models housing as explicit local goods instead of leaving it implicit inside standard of living.

## Scope and Design Boundary

- Housing is modeled as **continuous residential cost**, not a one-time property purchase.
- The implementation follows vanilla cyclical pop consumption (`buy_packages` + `pop_needs`) rather than introducing a separate asset-buying system.
- The mod focuses on a binary structure: rental housing vs owner-occupied housing.

## Current Implementation

### Goods

- `rented_housing`
  - Local good (`local = yes`)
  - Category: `staple`
  - Intended for low to lower-middle wealth demand
- `owned_housing`
  - Local good (`local = yes`)
  - Category: `luxury`
  - Intended for middle to high wealth demand

### Buildings and PM Layers

- `building_hrro_rental_developer`
  - Produces rental housing through PM progression (`tenement` -> `apartment` -> `highrise`)
- `building_hrro_owned_developer`
  - Produces owner housing through PM progression (`rowhouse` -> `suburban_villa` -> `luxury_estate`)

### Pop Need and Wealth Stratification

- `popneed_rented_housing` is used for lower wealth tiers and fades out at higher wealth.
- `popneed_owned_housing` appears from mid wealth and scales strongly at high wealth.
- `common/buy_packages/00_buy_packages.txt` is fully overridden for `wealth_1` to `wealth_99` to encode this transition.

### Local Price Dynamics

Both housing goods are local goods, so housing pressure and price are state-level rather than a single national market signal.

## Compatibility

- Mod name: `Housing Realism`
- Mod ID: `com.housing_realism`
- Game: `victoria3`
- Supported game version: `1.13.*`
- Multiplayer synchronized: `false`

Source of truth: `.metadata/metadata.json`

## Repository Map

- `common/goods/`
  - Housing goods definitions
- `common/pop_needs/`
  - Housing pop-need definitions
- `common/buy_packages/`
  - Wealth-tier demand curves (`wealth_1` to `wealth_99`)
- `common/buildings/`
  - Housing building definitions
- `common/production_method_groups/`
  - PM group definitions for both housing chains
- `common/production_methods/`
  - PM details for construction and ownership structures
- `common/modifier_type_definitions/`
  - Modifier keys for housing outputs
- `localization/english/`
  - English localization entries
- `gui/`
  - Text icon definitions
- `.metadata/`
  - Mod declaration and compatibility metadata
- `docs/agents/`
  - Design and contributor guidance docs

## Collaboration Workflow (Developer-Facing)

### Pre-change Checklist

- Confirm target scope and keep changes minimal.
- Route to the relevant design doc under `docs/agents/` before changing gameplay data.
- Verify naming consistency for keys such as `rented_housing` and `owned_housing`.

### Change Boundaries

- Keep source-of-truth gameplay data under `common/*`.
- Avoid introducing extra systems outside requested scope.
- Do not promise or document unimplemented features as completed.

### Commit and PR Granularity

- One gameplay intent per commit (for example, goods tuning, PM tuning, or buy-package curve tuning).
- Keep localization and data key updates in the same change set when keys are added/renamed.
- Keep PR descriptions explicit about:
  - affected files
  - gameplay intent
  - compatibility assumptions

### PR Verification Checklist

- All claimed mechanics are present in source files.
- Metadata values in docs match `.metadata/metadata.json`.
- Key names are consistent across `common/*` and localization.
- No unrelated refactors are mixed into the same PR.

## Non-goals (Current Version)

- No law-system integration shipped yet.
- No dedicated company-system expansion shipped yet.
- No custom housing UI analytics panel shipped yet.

## Terminology

- **Local Goods**: goods priced per state (`local = yes`)
- **Ownership Housing**: `owned_housing` demand/supply chain
- **Production Methods (PMs)**: staged production/ownership configurations per building
