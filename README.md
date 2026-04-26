# PhenoMCP

[![Build](https://img.shields.io/github/actions/workflow/status/KooshaPari/PhenoMCP/ci.yml?branch=main&label=build)](https://github.com/KooshaPari/PhenoMCP/actions)
[![Release](https://img.shields.io/github/v/release/KooshaPari/PhenoMCP?include_prereleases&sort=semver)](https://github.com/KooshaPari/PhenoMCP/releases)
[![License](https://img.shields.io/github/license/KooshaPari/PhenoMCP)](LICENSE)
[![Phenotype](https://img.shields.io/badge/Phenotype-org-blueviolet)](https://github.com/KooshaPari)

[![License: MIT OR Apache-2.0](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/KooshaPari/PhenoMCP/actions/workflows/ci.yml/badge.svg)](https://github.com/KooshaPari/PhenoMCP/actions/workflows/ci.yml)
[![Language: Rust](https://img.shields.io/badge/language-Rust-orange.svg)](https://www.rust-lang.org/)

> **Status: Experimental / Pre-foundational — Work in Progress**
>
> This repository is an early scaffold. The top-level `pheno-mcp` binary
> (`src/main.rs`) is a placeholder. Real work is happening inside the
> `crates/` and `bindings/` directories described below.

PhenoMCP is the planned home for a Model Context Protocol server plus a set
of backend adapter crates and cross-language bindings used by the Phenotype
ecosystem. It is **not** a usable MCP server yet — there is no tool surface,
no resources layer, no auth, and no transport implementation in the root
binary.

## What actually exists today

### Workspace layout

```
.
├── Cargo.toml              # workspace root, members = ["crates/*"]
├── src/main.rs             # placeholder: prints "PhenoMCP"
├── crates/
│   ├── pheno-meilisearch/      # Meilisearch HTTP client (reqwest, scaffold)
│   ├── pheno-qdrant/           # Qdrant HTTP client (reqwest, scaffold)
│   └── phenotype-surrealdb/    # SurrealDB wrapper crate (surrealdb 3.0)
├── bindings/
│   ├── swift/Sources/PhenoMCP/   # Swift binding scaffold
│   ├── kotlin/src/               # Kotlin binding scaffold
│   └── csharp/src/               # C# binding scaffold
├── docs/                   # design notes
├── integration-tests/      # placeholder
├── go.mod                  # placeholder
├── package.json            # placeholder
├── pyproject.toml          # placeholder
└── ADR.md, CHARTER.md, PLAN.md, PRD.md, VERSION
```

### Backend adapter crates (`crates/`)

These are early-stage and exist primarily as workspace members with
dependencies wired up. None should be considered production-ready.

| Crate                  | Purpose                                                | Key deps                       |
|------------------------|--------------------------------------------------------|--------------------------------|
| `pheno-meilisearch`    | HTTP client for Meilisearch                            | `reqwest`, `tokio`, `thiserror`|
| `pheno-qdrant`         | HTTP client for Qdrant vector DB                       | `reqwest`, `tokio`, `thiserror`|
| `phenotype-surrealdb`  | Thin wrapper over upstream `surrealdb` 3.0 with the WS protocol feature | `surrealdb` 3.0, `tokio` |

Each crate currently has a single `src/lib.rs`. Treat APIs as unstable.

### Language bindings (`bindings/`)

Scaffolds only. There is no working FFI/UniFFI layer yet — these directories
exist so the Swift / Kotlin / C# packaging story can be developed in
parallel with the Rust core.

- `bindings/swift/Sources/PhenoMCP/`
- `bindings/kotlin/src/`
- `bindings/csharp/src/`

If you are looking for "import PhenoMCP and call an MCP server" — that does
not exist yet in any language.

## What does **not** exist yet

The previous version of this README claimed a Quick Start, a `src/tools/`
module, a `src/resources/` module, an `src/auth/` module, and an
`src/adapters/` module. **None of those exist.** They were aspirational and
have been removed from this README to avoid misleading readers.

There is currently:

- No MCP transport (stdio/HTTP/WebSocket) implementation in the root binary.
- No tool registry, resource provider, or prompt surface.
- No auth layer.
- No published packages on crates.io, npm, PyPI, or any binding registry.
- No CI gates verifying behavior beyond `cargo build`.

## Building

The workspace compiles with a recent stable Rust toolchain (edition 2024,
resolver 3 — Rust 1.85+ required):

```bash
cargo build --workspace
```

The `pheno-mcp` binary will compile and, when run, print the program name
and exit. That is its entire current behavior.

## Roadmap

See `PLAN.md`, `PRD.md`, `ADR.md`, and `CHARTER.md` in this repository for
the intended direction. Those documents describe the target architecture;
this README describes the current state.

## License

Dual-licensed under MIT or Apache-2.0, at your option. See `LICENSE-MIT`
and `LICENSE-APACHE`.
