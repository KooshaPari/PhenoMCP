---
title: Security Model
---

# Security Model

The security model uses defense in depth:

- Authentication via tokens, mTLS, or OAuth/OIDC where needed
- Capability-level and resource-level authorization
- Sandboxed tool execution
- Structured audit logging and retention
- Secret handling without exposure in schemas or logs

See [ADR-004](../../adr/ADR-004).
