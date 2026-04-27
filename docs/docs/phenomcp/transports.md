---
title: Transport Architecture
---

# Transport Architecture

PhenoMCP is designed around a multi-protocol communication layer.

Supported transport directions in the current architecture:

- `stdio` for local CLI and editor integrations
- `HTTP/1.1` and `HTTP/2` for stateless and multiplexed remote calls
- `WebSocket` for duplex streaming
- `gRPC` for internal high-throughput services
- Unix domain sockets and raw TCP for specialized local deployments

See [ADR-001](../../adr/ADR-001).
