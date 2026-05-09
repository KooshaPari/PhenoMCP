//! PhenoMCP — minimal Model Context Protocol server entrypoint.
//!
//! Implements the MCP stdio transport: reads JSON-RPC 2.0 requests from stdin,
//! writes JSON-RPC 2.0 responses to stdout, one line per message.

use anyhow::Result;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::io::{self, BufRead, Write};

/// JSON-RPC 2.0 request object.
#[derive(Debug, Deserialize)]
struct JsonRpcRequest {
    jsonrpc: String,
    id: Value,
    method: String,
    #[serde(default)]
    params: Option<Value>,
}

/// JSON-RPC 2.0 response object (success or error encoded in `result`/`error`).
#[derive(Debug, Serialize)]
struct JsonRpcResponse {
    jsonrpc: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    id: Option<Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    result: Option<Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<Value>,
}

/// JSON-RPC 2.0 error object.
#[derive(Debug, Serialize)]
struct JsonRpcError {
    code: i32,
    message: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    data: Option<Value>,
}

const PROTOCOL_VERSION: &str = "2024-11-05";

fn handle_request(req: &JsonRpcRequest) -> Option<Value> {
    match req.method.as_str() {
        "initialize" => {
            let _client_info = req.params.as_ref().and_then(|p| p.get("clientInfo"));
            Some(serde_json::json!({
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "serverInfo": {
                    "name": "pheno-mcp",
                    "version": env!("CARGO_PKG_VERSION"),
                },
                "instructions": "PhenoMCP — Phenotype governance & ledger bridge. No tools registered yet.",
            }))
        }
        "tools/list" => {
            Some(serde_json::json!({
                "tools": []
            }))
        }
        "ping" => Some(serde_json::json!({})),
        _ => None,
    }
}

fn build_response(id: Value, result: Option<Value>, error: Option<JsonRpcError>) -> String {
    let resp = JsonRpcResponse {
        jsonrpc: "2.0".to_string(),
        id: Some(id),
        result,
        error: error.map(|e| serde_json::to_value(e).unwrap_or(serde_json::Value::Null)),
    };
    serde_json::to_string(&resp).unwrap_or_else(|_| r#"{"jsonrpc":"2.0","id":null,"error":{"code":-32603,"message":"Internal error"}}"#.to_string())
}

fn build_error_response(id: Value, code: i32, message: &str) -> String {
    build_response(
        id,
        None,
        Some(JsonRpcError {
            code,
            message: message.to_string(),
            data: None,
        }),
    )
}

fn main() -> Result<()> {
    let stdin = io::stdin();
    let mut reader = io::BufReader::new(stdin.lock()).lines();
    let mut stdout = io::stdout().lock();

    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::from_default_env()
                .add_directive(tracing::Level::INFO.into()),
        )
        .init();

    tracing::info!("PhenoMCP server started on stdio");

    while let Some(line) = reader.next() {
        let line = match line {
            Ok(l) => l,
            Err(_) => break,
        };

        let request: JsonRpcRequest = match serde_json::from_str(&line) {
            Ok(r) => r,
            Err(e) => {
                tracing::warn!("failed to parse JSON-RPC request: {}", e);
                let resp = build_error_response(
                    serde_json::Value::Null,
                    -32700,
                    &format!("Parse error: {}", e),
                );
                writeln!(stdout, "{}", resp).ok();
                stdout.flush().ok();
                continue;
            }
        };

        if request.jsonrpc != "2.0" {
            let resp = build_error_response(request.id, -32600, "Invalid Request: jsonrpc must be '2.0'");
            writeln!(stdout, "{}", resp).ok();
            stdout.flush().ok();
            continue;
        }

        tracing::debug!(method = %request.method, "handling request");

        let response = if let Some(result) = handle_request(&request) {
            build_response(request.id, Some(result), None)
        } else {
            build_error_response(request.id, -32601, &format!("Method not found: {}", request.method))
        };

        writeln!(stdout, "{}", response).map_err(|e| anyhow::anyhow!("write error: {}", e))?;
        stdout.flush().map_err(|e| anyhow::anyhow!("flush error: {}", e))?;
    }

    tracing::info!("PhenoMCP server stopped");
    Ok(())
}

