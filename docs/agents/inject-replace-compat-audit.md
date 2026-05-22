# Inject/Replace Compatibility Audit (Vanilla Extension Points)

Date: 2026-05-22
Scope: `common/buildings`, `common/production_method_groups`, `common/production_methods`

## Audit Result

- `common/buildings/hrro_housing_buildings.txt`: `无需改造`
  - Only defines custom keys (`building_hrro_*`), no vanilla same-name override.
- `common/production_method_groups/hrro_housing_pmgs.txt`: `无需改造`
  - Only defines custom keys (`pmg_hrro_*`), no vanilla same-name override.
- `common/production_methods/hrro_housing_pms.txt`: `无需改造`
  - Only defines custom keys (`pm_hrro_*`), no vanilla same-name override.

## Classification Summary

- `可 INJECT`: none in current scope
- `必须 REPLACE`: none in current scope
- `无需改造`: all audited objects

## Decision

No data-file rewrite is needed for this scope. Current compatibility risk is already low because objects are additive custom definitions rather than vanilla overwrites.
