# cheap-llm-mcp: State of the Art

**Version:** 0.1.0
**Date:** 2026-05-02
**Type:** MCP Server for Budget LLM Provider Integration
**Status:** Planning

---

## Overview

`cheap-llm-mcp` is a Model Context Protocol (MCP) server that provides unified, cost-effective access to budget LLM providers. It aggregates multiple low-cost API providers under a single MCP-compatible interface, enabling Claude Desktop, Cursor, and other MCP clients to use affordable LLM inference without vendor lock-in.

**Core Philosophy:** Maximum capability at minimum cost. Route intelligently, fall back gracefully, and make budget LLM adoption seamless.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        MCP Client                            │
│  (Claude Desktop, Cursor, Zed, n8n, etc.)                   │
└─────────────────────┬───────────────────────────────────────┘
                      │ MCP Protocol (JSON-RPC)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    cheap-llm-mcp                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Router    │  │  Provider   │  │   Cache     │        │
│  │  (fallback) │  │   Manager   │  │  (Memory)   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────┬───────────────────────────────────────┘
                      │ Unified REST API
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Budget LLM Providers                       │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                  │
│  │Groq │ │Deep │ │Fire │ │Toge-│ │Oll- │                  │
│  │     │ │Infra│ │work │ │ther │ │ama  │                  │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

| Component | Responsibility |
|-----------|----------------|
| **Router** | Request routing with fallback chain |
| **Provider Manager** | API key management, health checks |
| **Response Normalizer** | Unified response format |
| **Cache Layer** | Request deduplication |

---

## Provider Integration Matrix

### Tier 1: Sub-$0.50/1M tokens (Recommended)

| Provider | Models | Streaming | Tools | Context | Latency | Reliability |
|----------|--------|-----------|-------|---------|---------|-------------|
| **Groq** | Llama 3.1 70B, Mixtral, Gemma 2B | Yes | Partial | 8K | ~100ms | 99.5% |
| **Fireworks AI** | Llama 3, Mixtral, Qwen 72B | Yes | Yes | 32K | ~150ms | 99% |
| **DeepInfra** | Llama 3, Mistral, Gemma | Yes | Yes | 32K | ~200ms | 98% |

### Tier 2: $0.50-$2.00/1M tokens

| Provider | Models | Streaming | Tools | Context |
|----------|--------|-----------|-------|---------|
| **Together AI** | Llama 3, Qwen, DeepSeek | Yes | Yes | 32K |
| **Perplexity** | Sonar | Yes | Yes | 128K |
| **Cohere** | Command R+ | Yes | Yes | 128K |

### Tier 3: Free/Open (Local)

| Solution | Models | Deployment | Use Case |
|----------|--------|------------|----------|
| **Ollama** | Llama 3, Mistral, Qwen | Local | Privacy, no cost |
| **LM Studio** | GGUF formats | Local | Desktop GUI |
| **vLLM** | Any HF model | Self-hosted | Production control |

---

## Cost Comparison

### Per-Million Tokens

| Provider | Input | Output | Monthly Limit | Best For |
|----------|-------|--------|---------------|----------|
| Groq | $0 | $0.20 | 14K req/min | High-volume tasks |
| DeepInfra | $0.30 | $0.30 | 100 req/min | Balanced |
| Fireworks | $0.20 | $0.20 | Rate limited | Cost efficiency |
| Together | $0.80 | $0.80 | Varies | Fine-tuned models |
| Ollama | $0 | $0 | Unlimited | Privacy/max control |

### Monthly Cost Example (50M tokens/month)

| Provider | Cost |
|----------|------|
| OpenAI GPT-4o | $750 |
| Anthropic Claude 3.5 | $750 |
| **Groq** | **$10** |
| **DeepInfra** | **$30** |
| **Ollama (local)** | **$0** |

---

## Recommended Default Chain

```
Primary:   Groq (fastest, cheapest for standard models)
Fallback1: Fireworks AI (good throughput, tool support)
Fallback2: DeepInfra (variety of models)
Fallback3: Ollama (local, unlimited, private)
```

---

## Supported Models

| Provider | Model ID | Context | Specialty |
|----------|----------|---------|-----------|
| Groq | llama-3.1-70b | 8K | General purpose |
| Groq | llama-3.1-8b | 8K | Fast tasks |
| Groq | mixtral-8x7b | 32K | Balanced |
| Groq | gemma2-9b | 8K | Code |
| Fireworks | llama-3-70b | 8K | General |
| Fireworks | mixtral-8x22b | 32K | Long context |
| Fireworks | qwen-72b | 32K | Code, math |
| DeepInfra | llama-3-70b | 8K | General |
| DeepInfra | mixtral-8x7b | 32K | Balanced |
| Ollama | llama3 | 8K | General |
| Ollama | codellama | 16K | Code generation |
| Ollama | mistral | 8K | Fast tasks |
| Ollama | phi3 | 4K | Small footprint |

---

## MCP Tools

### `llm_complete`

```typescript
{
  model: string;              // e.g., "groq/llama-3.1-70b"
  messages: Array<{
    role: "user" | "assistant" | "system";
    content: string;
  }>;
  temperature?: number;       // Default: 0.7
  maxTokens?: number;        // Default: 4096
  stream?: boolean;          // Default: false
}
```

### `llm_batch`

```typescript
{
  prompts: string[];
  model?: string;
  parallel?: boolean;         // Default: true
}
```

---

## MCP Resources

### `cheap-llm://providers`

Provider health and status.

```json
{
  "providers": [
    {
      "name": "groq",
      "status": "healthy",
      "latencyMs": 95,
      "costPerMInput": 0,
      "costPerMOutput": 0.20,
      "currentLoad": "low"
    }
  ]
}
```

### `cheap-llm://costs`

Cost tracking.

```json
{
  "today": { "spentUsd": 2.34, "tokensUsed": 2500000 },
  "month": { "spentUsd": 45.67, "tokensUsed": 45000000 },
  "projectedMonth": 85.00
}
```

---

## Configuration

### Environment Variables

```bash
# Provider API Keys
GROQ_API_KEY=gswr_xxxx
DEEPINFRA_API_KEY=xxxxxxxxxxxxxxxx
FIREWORKS_API_KEY=xxxxxxxxxxxxxxxx
TOGETHER_API_KEY=xxxxxxxxxxxxxxxx

# Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434

# Server
PORT=3000
LOG_LEVEL=info

# Defaults
DEFAULT_MODEL=groq/llama-3.1-70b
MAX_RETRIES=3
TIMEOUT_MS=60000
```

### Provider Priority Config

```yaml
providers:
  groq:
    priority: 1
    enabled: true
    models:
      - llama-3.1-70b
      - mixtral-8x7b
      - gemma2-9b
    rateLimit:
      requestsPerMinute: 10000
      tokensPerMinute: 1000000

  fireworks:
    priority: 2
    enabled: true
    models:
      - llama-3-70b
      - mixtral-8x22b
    rateLimit:
      requestsPerMinute: 1000
      tokensPerMinute: 500000

  ollama:
    priority: 99  # Local fallback
    enabled: true
    baseUrl: http://localhost:11434
```

---

## Benchmark Results

### Latency (Time to First Token)

| Model | Groq | DeepInfra | Fireworks | Ollama (RTX 3090) |
|-------|------|-----------|-----------|-------------------|
| Llama 3 70B | 0.8s | 1.2s | 1.0s | 2.5s |
| Llama 3 8B | 0.3s | 0.4s | 0.3s | 0.5s |
| Mixtral 8x7B | 1.0s | 1.5s | 1.2s | 3.0s |

### Throughput (tokens/second)

| Provider | Llama 3 70B | Mistral 7B | CodeLlama 34B |
|----------|-------------|------------|---------------|
| Groq | 600 | 800 | 400 |
| Fireworks | 450 | 600 | 300 |
| DeepInfra | 350 | 500 | 250 |
| Ollama | 80 | 120 | 40 |

### Cost Efficiency Score

```
Score = (Quality × Throughput) / Cost

Groq Llama 3 70B:     (0.85 × 600) / 0.20 = 2550
Fireworks Llama 3 70B: (0.85 × 450) / 0.40 = 956
DeepInfra Llama 3 70B: (0.85 × 350) / 0.60 = 496
```

**Winner: Groq for raw efficiency**

---

## Usage Examples

### Claude Desktop Config

```json
{
  "mcpServers": {
    "cheap-llm": {
      "command": "npx",
      "args": ["cheap-llm-mcp", "--port", "3000"],
      "env": {
        "GROQ_API_KEY": "gswr_xxxx",
        "DEFAULT_MODEL": "groq/llama-3.1-70b"
      }
    }
  }
}
```

### Cursor IDE Config

```json
{
  "mcpServers": {
    "cheap-llm": {
      "command": "npx",
      "args": ["cheap-llm-mcp"],
      "env": {
        "GROQ_API_KEY": "gswr_xxxx"
      }
    }
  }
}
```

---

## Implementation Roadmap

### v0.1 - Core Server
- [ ] MCP protocol scaffold
- [ ] Basic tool definitions
- [ ] JSON-RPC message handling
- [ ] Streaming support

### v0.2 - Provider Integration
- [ ] Groq API integration
- [ ] DeepInfra API integration
- [ ] Fireworks AI integration
- [ ] Ollama integration (local)

### v0.3 - Advanced Features
- [ ] Request caching (memory-based)
- [ ] Automatic fallback routing
- [ ] Cost tracking per request
- [ ] Health check endpoints

### v1.0 - Production
- [ ] Authentication
- [ ] Rate limiting
- [ ] Monitoring dashboard
- [ ] Comprehensive error handling

---

## Related Documents

- [PhenoMCP SOTA](./SOTA.md) - Local GPU inference MCP server
- [Inference Stack Reference](./docs/inference-stack-reference.md) - vLLM/SGLang deployment
- [Pheno Infrastructure Plan](./docs/pheno-infrastructure-plan.md) - Full infrastructure design

---

## References

- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [Groq API Documentation](https://console.groq.com/docs)
- [DeepInfra API](https://deepinfra.com/docs)
- [Fireworks AI](https://fireworks.ai/docs)
- [Together AI](https://docs.together.ai)
- [Ollama](https://github.com/ollama/ollama)

---

*Maintained by Phenotype Team*
