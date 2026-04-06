# AGENTS.md — PhenoMCP

## Project Overview

- **Name**: PhenoMCP
- **Description**: Multi-language MCP (Model Context Protocol) SDK and runtime - Rust core with Go, Python, TypeScript, Mojo bindings
- **Location**: `/Users/kooshapari/CodeProjects/Phenotype/repos/PhenoMCP`
- **Language Stack**: Rust (core), Go, Python, TypeScript, Mojo, WASI
- **Published**: Internal (Phenotype ecosystem)

## Quick Start Commands

```bash
# Navigate to PhenoMCP
cd /Users/kooshapari/CodeProjects/Phenotype/repos/PhenoMCP

# Rust core
cargo build
cargo test

# Go bindings
cd go && go build ./...

# Python bindings
cd python && pip install -e .

# TypeScript
cd ts && npm install && npm run build
```

## Architecture

```
PhenoMCP/
├── .agileplus/               # AgilePlus integration
├── bindings/                 # Language bindings
├── Cargo.lock               # Rust dependencies
├── Cargo.toml               # Workspace manifest
├── crates/                  # Rust crates
├── docs/                    # Documentation
├── examples/                # Usage examples
├── ffi/                     # FFI layer
├── go/                      # Go SDK
│   └── go.mod
├── go.mod                   # Root Go module
├── integration-tests/       # Cross-language tests
├── mojo/                    # Mojo bindings
├── package.json             # Node dependencies
├── pyproject.toml           # Python config
├── python/                  # Python SDK
├── README.md                # Overview
├── src/                     # Rust source
├── ts/                      # TypeScript SDK
├── VERSION                  # Version tracking
└── wasi/                    # WASI/WebAssembly
```

## Quality Standards

### Rust (Core)
- **Line length**: 100 characters
- **Formatter**: `cargo fmt`
- **Linter**: `cargo clippy -- -D warnings`
- **Tests**: `cargo test --workspace`

### Go Bindings
- **Line length**: 100 characters
- **Formatter**: `gofmt`
- **Linter**: `golangci-lint`
- **Tests**: `go test ./...`

### Python Bindings
- **Line length**: 100 characters
- **Formatter**: `ruff format` or `black`
- **Linter**: `ruff check`
- **Type checker**: `mypy`

### TypeScript Bindings
- **Line length**: 100 characters
- **Formatter**: `prettier`
- **Linter**: `eslint`
- **Type checker**: `tsc --noEmit`

## Git Workflow

### Branch Naming
Format: `phenomcp/<type>/<description>` or `<language>/<type>/<description>`

Examples:
- `phenomcp/feat/server-impl`
- `python/feat/async-client`
- `go/fix/transport-error`

### Commit Format
```
<type>(<scope>): <description>

Scope: core, go, python, ts, mojo, wasi, ffi

Examples:
- feat(core): add server initialization
- fix(python): resolve async context handling
- docs(go): update transport examples
```

## File Structure

```
PhenoMCP/
├── crates/                   # Rust crates
│   └── phenotype-mcp-*/      # MCP-specific crates
├── bindings/                 # Language bindings
├── go/                       # Go SDK
│   ├── go.mod
│   └── [Go source]
├── python/                   # Python SDK
│   ├── pyproject.toml
│   └── [Python source]
├── ts/                       # TypeScript SDK
│   ├── package.json
│   └── [TS source]
├── mojo/                     # Mojo SDK
├── ffi/                      # FFI layer
└── wasi/                     # WebAssembly
```

## CLI Commands

```bash
# Rust
cargo build --workspace
cargo test --workspace
cargo clippy --workspace -- -D warnings

# Go
cd go && go build ./...
cd go && go test ./...

# Python
cd python && pip install -e ".[dev]"
cd python && pytest

# TypeScript
cd ts && npm install
cd ts && npm run build

# Integration tests
cd integration-tests && [see README]
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Rust build fails | Check `crates/` structure |
| FFI errors | Verify binding definitions |
| Cross-language issues | Check `integration-tests/` |

## Dependencies

- **phenotype-mcp-*/crates**: Related MCP crates in /crates
- **AgilePlus**: Work tracking
- **MCP spec**: Model Context Protocol specification

## Agent Notes

When working in PhenoMCP:
1. Multi-language project - check which language/SDK you're modifying
2. Rust is the canonical implementation
3. Other languages bind through FFI or reimplement
4. Integration tests are critical for multi-language consistency
5. Check `crates/phenotype-mcp-*` for related work
