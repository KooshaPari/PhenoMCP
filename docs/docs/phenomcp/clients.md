---
title: Client SDK Architecture
---

# Client SDK Architecture

Client SDKs are intended to give TypeScript, Python, Rust, Go, and other
languages the same high-level MCP behavior with language-appropriate async
patterns.

Current goals:

- Keep a consistent API shape across languages
- Support capability discovery and generated types
- Hide transport details behind a narrow client interface
- Provide test utilities for mocking and replay

See [ADR-003](../../adr/ADR-003).
