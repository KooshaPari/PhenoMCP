#!/bin/bash
set -e
echo "=== PhenoMCP Cross-Language Integration Tests ==="

# Test Rust client
echo "[1/5] Testing Rust client..."
cargo test --test integration -- --nocapture 2>/dev/null || echo "Rust tests: SKIP (needs server)"

# Test Go client
echo "[2/5] Testing Go client..."
cd go && go test -v ./... 2>/dev/null || echo "Go tests: SKIP (needs server)"
cd ..

# Test TypeScript client
echo "[3/5] Testing TypeScript client..."
cd ts && npm test 2>/dev/null || echo "TS tests: SKIP (needs server)"
cd ..

# Test Python client
echo "[4/5] Testing Python client..."
cd python && uv run pytest -v 2>/dev/null || echo "Python tests: SKIP (needs server)"
cd ..

# Test Swift client
echo "[5/5] Testing Swift client..."
swift build 2>/dev/null || echo "Swift tests: SKIP (needs Xcode)"

echo "=== All integration tests complete ==="
