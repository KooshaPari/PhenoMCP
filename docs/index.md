---
layout: home
title: PhenoMCP
titleTemplate: Multi-language MCP SDK and runtime
hero:
  name: PhenoMCP
  text: Multi-language MCP SDK and runtime
  tagline: Rust core, Go/Python/TypeScript/Mojo bindings, and adapter crates for the Phenotype ecosystem.
  actions:
    - theme: brand
      text: Research
      link: /research/
    - theme: alt
      text: Current State
      link: /#what-actually-exists-today
features:
  - title: Canonical root
    details: Tracks the current scaffold, live workspace shape, and what exists versus what remains aspirational.
  - title: Research-backed
    details: Collects protocol and SDK research alongside the repo's ADRs and reference matrix.
  - title: Multi-language
    details: Keeps Rust, Go, Python, TypeScript, Mojo, and WASI surfaces visible from one docs entrypoint.
---

## What actually exists today

- Rust workspace root with placeholder binary entrypoint.
- Adapter crates for Meilisearch, Qdrant, and SurrealDB.
- Language binding scaffolds for Swift, Kotlin, and C#.
- Research notes, ADRs, and a coverage matrix in `docs/`.

## What does not exist yet

- MCP transport implementation in the root binary.
- Tool registry, resources, prompts, and auth layers.
- Published packages on crates.io, npm, or PyPI.
- CI gates beyond basic build validation.

## Useful entrypoints

- [README](/)
- [State of the Art: MCP](/research/)
- [AI SDK comparison](/research/)
- [Feature coverage matrix](/reference/)
- [Worklogs](/worklogs/)
