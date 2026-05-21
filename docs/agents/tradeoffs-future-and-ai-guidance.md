# Tradeoffs, Future Work, and AI Guidance

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
