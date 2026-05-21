# Housing Realism - Agent Document Router

This file is the lightweight routing index for Housing Realism documentation.

Use this file as the entrypoint and load topic docs on demand. Do not load all topic files by default.

## Project Context

Housing Realism is a *Victoria 3* housing-economy mod centered on two local housing goods (`rented_housing` and `owned_housing`) and wealth-stratified Pop consumption under the game's cyclical goods-consumption framework.

## Routing Table

| Topic | When to load | Path |
|---|---|---|
| Overview and goals | Load when you need project intent, design objectives, or top-level rationale. | `docs/agents/overview-and-goals.md` |
| Goods and pop needs | Load when working on goods definitions, `local = yes`, `buy_packages`, or wealth-stratified housing demand. | `docs/agents/goods-and-pop-needs.md` |
| Buildings and PMs | Load when changing housing buildings, production methods, employment shape, or service-input semantics. | `docs/agents/buildings-and-pms.md` |
| Ownership, icons, and structure | Load when touching ownership PM policy, icon strategy, or mod declaration/structure assumptions. | `docs/agents/ownership-icons-and-structure.md` |
| Tradeoffs, future work, and AI guidance | Load when evaluating design tradeoffs, expansion direction, or contributor/AI implementation constraints. | `docs/agents/tradeoffs-future-and-ai-guidance.md` |

## Routing Conventions

- One topic maps to one canonical file.
- Route names are stable and human-readable.
- Load only the referenced topic docs for the current task.
- Keep gameplay/source-of-truth data under `common/*` independent from this documentation routing layer.
