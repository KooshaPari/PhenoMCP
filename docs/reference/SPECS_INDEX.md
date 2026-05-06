# PhenoMCP Tools — Spec Index

**File:** `docs/reference/SPECS_INDEX.md`
**Updated:** 2026-05-05

## Tool Coverage

| Tool | Status | File | Notes |
|------|--------|------|-------|
| `session_suspend` | **DONE** | `python/src/pheno_mcp/tools/session_tools.py` | Calls `POST /api/v1/sessions/{session_id}/suspend` |
| `session_resume` | **DONE** | `python/src/pheno_mcp/tools/session_tools.py` | Calls `POST /api/v1/sessions/resume` with bundle_ref |
| `workflow_execute` | **DONE** | `python/src/pheno_mcp/tools/workflow_tools.py` | Calls `POST /workflows/{workflow_id}/execute` |
| `workflow_status` | **DONE** | `python/src/pheno_mcp/tools/workflow_tools.py` | Calls `GET /workflows/{workflow_id}` |
| `workflow_cancel` | **DONE** | `python/src/pheno_mcp/tools/workflow_tools.py` | Calls `POST /workflows/{workflow_id}/cancel` |
| `workflow_list` | **DONE** | `python/src/pheno_mcp/tools/workflow_tools.py` | Calls `GET /workflows` |
| `ledger_query` | **DONE** | `python/src/pheno_mcp/tools/governance_tools.py` | Calls `GET /api/v1/governance/ledger` |
| `ledger_verify` | **DONE** | `python/src/pheno_mcp/tools/governance_tools.py` | Calls `POST /api/v1/governance/ledger/verify` |
| `tool_execute` | TODO | — | Requires Parpoura tool execution endpoint |
| `tool_list` | TODO | — | Requires Parpoura agent tool registry |
| `tool_sandbox_run` | TODO | — | Requires Parpoura sandbox endpoint |

## Parpoura API Endpoints Added

| Endpoint | Status | File | Notes |
|----------|--------|------|-------|
| `POST /api/v1/sessions/{session_id}/suspend` | **DONE** | `venture/api/main.py` | In-memory bundle storage |
| `POST /api/v1/sessions/resume` | **DONE** | `venture/api/main.py` | In-memory bundle storage |
| `GET /api/v1/governance/ledger` | **DONE** | `venture/api/main.py` | Placeholder — wire LedgerService |
| `POST /api/v1/governance/ledger/verify` | **DONE** | `venture/api/main.py` | Placeholder — wire LedgerService |

## Backlog

- `tool_execute`, `tool_list`, `tool_sandbox_run` — Phase 4 items pending Parpoura tool execution API.
- Governance endpoints are functional stubs; wire `LedgerService.verify_audit_chain()` for production.
- Session bundle storage is in-memory; replace with persistent storage for production.
- Add `SESSION_SUSPEND` / `SESSION_RESUME` / `LEDGER_READ` / `LEDGER_WRITE` to `AuditEventType` and `Permission` enums.
