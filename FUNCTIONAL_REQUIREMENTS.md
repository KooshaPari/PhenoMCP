# Functional Requirements — PhenoMCP

Traces to: PRD.md epics E1–E7.
ID format: FR-PHENOMCP-{NNN}.

---

## MCP Server Implementation

**FR-PHENOMCP-001**: The system SHALL implement the Model Context Protocol 2.13+ specification with full tool, resource, and prompt support.
Traces to: E1.1

**FR-PHENOMCP-002**: The system SHALL expose Phenotype capabilities (agents, services, knowledge) as MCP resources and tools.
Traces to: E1.2

**FR-PHENOMCP-003**: The system SHALL support multiple transport types (stdio, HTTP, WebSocket) for connecting to Claude and other MCP clients.
Traces to: E1.3

---

## Resource Management

**FR-PHENOMCP-004**: The system SHALL provide resource listings with metadata, URIs, and MIME types for discoverable capability exposure.
Traces to: E2.1

**FR-PHENOMCP-005**: The system SHALL support server-side pagination for resource lists to handle large collections.
Traces to: E2.2

---

## Tool & Prompt Handlers

**FR-PHENOMCP-006**: The system SHALL provide tool handlers that validate inputs, execute operations, and return structured results.
Traces to: E3.1

**FR-PHENOMCP-007**: The system SHALL support custom prompt templates for common Phenotype workflows.
Traces to: E3.2

---

## Trace & Test Guidance

All tests MUST reference a Functional Requirement (FR):

```rust
// Traces to: FR-PHENOMCP-NNN
#[test]
fn test_mcp_tool_execution() { ... }
```
