#!/usr/bin/env python3
"""Fix all phenomcp audit issues in workflow files and configs."""

import os
import re

REPO = "/Users/kooshapari/CodeProjects/Phenotype/repos/phenomcp"

# ---- Fix 1: Remove @v4 prefix before SHA in all workflow files ----
# Pattern: @v4@<sha> or @v3@<sha>  ->  @<sha>

DOUBLE_SHA_FILES = [
    ".github/workflows/cargo-audit.yml",
    ".github/workflows/cargo-machete.yml",
    ".github/workflows/cargo-semver-checks.yml",
    ".github/workflows/codeql-rust.yml",
    ".github/workflows/codeql.yml",
    ".github/workflows/pages.yml",
]

for f in DOUBLE_SHA_FILES:
    path = os.path.join(REPO, f)
    with open(path) as fh:
        content = fh.read()
    # Fix @v4@<sha> -> @<sha>
    content = content.replace("@v4@11bd71901bbe5b1630ceea73d27597364c9af683",
                               "@11bd71901bbe5b1630ceea73d27597364c9af683")
    # Only in pages.yml: @v3@<sha> -> @<sha>
    content = content.replace("@v3@fc324d3547104276b827a68afc52ff2a11cc49c9",
                               "@fc324d3547104276b827a68afc52ff2a11cc49c9")
    with open(path, "w") as fh:
        fh.write(content)
    print(f"Fixed double-SHA in {f}")

# ---- Fix 2: Replace invalid SHAs ----

# codeql-rust.yml: 865f5f5c36632f18690a3d569fa0a764f2da0c3e -> 53e96ec3b35fce51c141c0d6f0e31028a448722d (codeql v3)
path = os.path.join(REPO, ".github/workflows/codeql-rust.yml")
with open(path) as fh:
    content = fh.read()
content = content.replace("865f5f5c36632f18690a3d569fa0a764f2da0c3e",
                           "53e96ec3b35fce51c141c0d6f0e31028a448722d")
with open(path, "w") as fh:
    fh.write(content)
print("Fixed codeql SHA in codeql-rust.yml")

# codeql.yml: b25d0ebf40e5b63ee81e1bd6e5d2a12b7c2aeb61 -> 53e96ec3b35fce51c141c0d6f0e31028a448722d
path = os.path.join(REPO, ".github/workflows/codeql.yml")
with open(path) as fh:
    content = fh.read()
content = content.replace("b25d0ebf40e5b63ee81e1bd6e5d2a12b7c2aeb61",
                           "53e96ec3b35fce51c141c0d6f0e31028a448722d")
with open(path, "w") as fh:
    fh.write(content)
print("Fixed codeql SHA in codeql.yml")

# scorecard.yml: invalid SHAs
path = os.path.join(REPO, ".github/workflows/scorecard.yml")
with open(path) as fh:
    content = fh.read()
content = content.replace("ossf/scorecard-action@99c09fe975337306107572b4fdf4db224cf8e2f2",
                           "ossf/scorecard-action@4eaacf0543bb3f2c246792bd56e8cdeffafb205a")
content = content.replace("github/codeql-action/upload-sarif@b25d0ebf40e5b63ee81e1bd6e5d2a12b7c2aeb61",
                           "github/codeql-action/upload-sarif@53e96ec3b35fce51c141c0d6f0e31028a448722d")
with open(path, "w") as fh:
    fh.write(content)
print("Fixed SHAs in scorecard.yml")

# ci.yml: setup-python invalid SHA
path = os.path.join(REPO, ".github/workflows/ci.yml")
with open(path) as fh:
    content = fh.read()
content = content.replace("actions/setup-python@0c7785c5a13b57a1607be5e8b14f73a29e2e57a",
                           "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405")
with open(path, "w") as fh:
    fh.write(content)
print("Fixed setup-python SHA in ci.yml")

# lint.yml: setup-go and golangci-lint-action invalid SHAs
path = os.path.join(REPO, ".github/workflows/lint.yml")
with open(path) as fh:
    content = fh.read()
content = content.replace("actions/setup-go@0a12ed9e1a4ce4b1a02a5f2dd1e3a9c9e6c7f8b1",
                           "actions/setup-go@4a3601121dd01d1626a1e23e37211e3254c1c06c")
content = content.replace("golangci/golangci-lint-action@aa6339a8b9e0e1c4b5e7c4e6f8d7c3a2b1e0d9f8",
                           "golangci/golangci-lint-action@1e7e51e771db61008b38414a730f564565cf7c20")
with open(path, "w") as fh:
    fh.write(content)
print("Fixed SHAs in lint.yml")

# cargo-deny.yml: EmbarkStudios/cargo-deny-action invalid SHA
path = os.path.join(REPO, ".github/workflows/cargo-deny.yml")
with open(path) as fh:
    content = fh.read()
content = content.replace("EmbarkStudios/cargo-deny-action@5bb39ff5d5a0e94dc9e2dc94eced0c6129743a57",
                           "EmbarkStudios/cargo-deny-action@91bf2b620e09e18d6eb78b92e7861937469acedb")
with open(path, "w") as fh:
    fh.write(content)
print("Fixed cargo-deny SHA in cargo-deny.yml")

# ---- Fix 3: .golangci.yml - remove linter-settings typo block, keep linters-settings ----
path = os.path.join(REPO, ".golangci.yml")
with open(path) as fh:
    content = fh.read()

# Remove the entire linter-settings block (NOT linters-settings - note the 's')
# The block starts at "linter-settings:" and ends before "linters:"
lines = content.split('\n')
new_lines = []
skip_block = False
for line in lines:
    if line.strip().startswith('linter-settings:'):
        skip_block = True
        continue
    if skip_block:
        # Check if we've reached a top-level key (no indent)
        if line and not line[0].isspace():
            skip_block = False
            new_lines.append(line)
            continue
        # Also check for empty line followed by top-level key (just skip)
        continue
    new_lines.append(line)

content = '\n'.join(new_lines)
with open(path, "w") as fh:
    fh.write(content)
print("Fixed .golangci.yml (removed linter-settings typo)")

# ---- Fix 4: CLAUDE.md - fix PhenoMCP path ----
path = os.path.join(REPO, "CLAUDE.md")
with open(path) as fh:
    content = fh.read()
content = content.replace(
    "- **Location:** /Users/kooshapari/CodeProjects/Phenotype/repos/PhenoMCP",
    "- **Location:** /Users/kooshapari/CodeProjects/Phenotype/repos/phenomcp"
)
with open(path, "w") as fh:
    fh.write(content)
print("Fixed CLAUDE.md path")

print("\nAll fixes applied!")
