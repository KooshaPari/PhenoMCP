# Implementation Strategy

## Approach

Use an isolated docs-only rollout:

- Add the sladge badge to the existing README badge block.
- Store rollout evidence under `docs/sessions/`.
- Avoid runtime, build, generated, and catalog changes.

## Rationale

The badge is governance metadata for an MCP/runtime workspace and should not
affect package behavior or pre-foundational implementation state.
