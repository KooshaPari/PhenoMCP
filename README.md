# PhenoMCP

> Polyglot Model Context Protocol implementation — a Rust core (`pheno-mcp`)
> with first-class bindings for Swift, Kotlin, and C#, plus reference adapters
> for Meilisearch, Qdrant, and SurrealDB.

PhenoMCP is the Phenotype-org canonical MCP toolkit. The core protocol crate
is implemented once in Rust and exposed to host languages through narrow,
generated bindings, so iOS, Android, and .NET hosts can speak MCP without
re-implementing framing, capability negotiation, or transport selection.

## Layout

```
PhenoMCP/
├── src/main.rs                       # pheno-mcp CLI entry point
├── crates/
│   ├── pheno-meilisearch/            # MCP server backed by Meilisearch
│   ├── pheno-qdrant/                 # MCP server backed by Qdrant
│   └── phenotype-surrealdb/          # MCP server backed by SurrealDB
├── bindings/
│   ├── swift/                        # SwiftPM package, UniFFI-generated
│   ├── kotlin/                       # Kotlin/JVM module
│   └── csharp/                       # .NET package
├── integration-tests/                # cross-language conformance suite
└── docs/                             # protocol notes, ADRs
```

Specs live in [PRD.md](PRD.md), [ADR.md](ADR.md), and [PLAN.md](PLAN.md).

## Install

### Rust

```bash
cargo install --git https://github.com/KooshaPari/PhenoMCP pheno-mcp
```

Or as a library:

```toml
[dependencies]
pheno-mcp = { git = "https://github.com/KooshaPari/PhenoMCP" }
```

### Swift, Kotlin, C#

See language-specific READMEs under [`bindings/`](bindings/). Bindings are
published per-platform; consult the relevant package manager (SwiftPM, Maven,
NuGet) for the latest version.

## Quick start

### Run a built-in server

```bash
# Search-backed MCP server (Meilisearch)
pheno-mcp serve meilisearch --url http://localhost:7700 --key $MEILI_KEY

# Vector-backed MCP server (Qdrant)
pheno-mcp serve qdrant --url http://localhost:6333

# Graph/document MCP server (SurrealDB)
pheno-mcp serve surrealdb --url ws://localhost:8000
```

### Embed in a Rust host

```rust
use pheno_mcp::{Server, transport::Stdio};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    Server::builder()
        .name("my-tool-host")
        .with_tool(my_tool::descriptor(), my_tool::handler)
        .serve(Stdio::default())
        .await
}
```

## Conformance

Cross-language tests live in `integration-tests/` and exercise every binding
against the Rust core to guarantee wire-compatible behavior:

```bash
cargo test --workspace
cd integration-tests && ./run.sh        # spins up bindings + runs probes
```

## Related repositories

- **[AgentMCP](https://github.com/KooshaPari/AgentMCP)** — Python agent-side
  harness and 391-test compliance battery.
- **[TestingKit](https://github.com/KooshaPari/TestingKit)** — shared test
  fixtures used by the integration suite.

## Contributing

See [AGENTS.md](AGENTS.md) and [CHARTER.md](CHARTER.md) for governance and
contribution norms. Issues and PRs welcome; protocol-shaping changes must
include an ADR update.

## License

Dual-licensed under [Apache License 2.0](LICENSE-APACHE) or
[MIT License](LICENSE-MIT) at your option.
