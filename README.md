# aeo-sdk-python

[![PyPI](https://img.shields.io/pypi/v/aeo-protocol.svg)](https://pypi.org/project/aeo-protocol/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/aeo-protocol.svg)](https://pypi.org/project/aeo-protocol/)
[![Python versions](https://img.shields.io/pypi/pyversions/aeo-protocol.svg)](https://pypi.org/project/aeo-protocol/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Python SDK for the [AEO Protocol v0.1](https://github.com/mizcausevic-dev/aeo-protocol-spec) — parse, build, validate, and fetch AEO declaration documents.

## Install

```bash
pip install aeo-protocol
```

## Quickstart

```python
from aeo import Document, fetch_well_known

# Fetch and parse from a live well-known URL
doc = fetch_well_known("https://mizcausevic-dev.github.io")
print(doc.entity.name)              # "Miz Causevic"
print(doc.claim_ids())               # ['current-role', 'location', ...]
print(doc.find_claim("years-experience").value)  # 30

# Parse from disk
doc = Document.from_file("aeo.json")

# Build programmatically
from aeo import Entity, Authority, Claim, Document
doc = Document(
    entity=Entity(
        id="https://example.com/#org",
        type="Organization",
        name="Example Org",
        canonical_url="https://example.com/",
    ),
    authority=Authority(primary_sources=["https://example.com/"]),
    claims=[Claim(id="tagline", predicate="description", value="A reference example.")],
)
print(doc.to_json())
```

Async variant:

```python
import asyncio
from aeo.client import fetch_well_known_async

doc = asyncio.run(fetch_well_known_async("https://mizcausevic-dev.github.io"))
```

## What it does

- **Parse** — `Document.from_json` / `from_file` / `from_dict`
- **Build** — pydantic v2 model classes for every type in the spec (`Entity`, `Authority`, `Claim`, `Verification`, `CitationPreferences`, `AnswerConstraints`, `Audit`)
- **Serialize** — `Document.to_json()` returns canonical JSON
- **Fetch** — `fetch_well_known(origin)` performs HTTP discovery against `/.well-known/aeo.json` with `Accept: application/aeo+json, application/json`
- **Query** — `doc.claim_ids()` and `doc.find_claim(id)` for convenience

## Conformance

This SDK supports the AEO Protocol at **conformance Level 1 (Declare)**. Signature verification (Level 2) and audit-endpoint posting (Level 3) are not yet implemented; signed documents parse fine but the signature is not verified.

## Dependencies

- [pydantic](https://github.com/pydantic/pydantic) >= 2.0 — model validation and serialization
- [httpx](https://github.com/encode/httpx) >= 0.27 — sync and async HTTP

## Development

```bash
pip install -e .[dev]
pytest -v
```

## Specification

Full spec at [github.com/mizcausevic-dev/aeo-protocol-spec](https://github.com/mizcausevic-dev/aeo-protocol-spec).

## License

MIT-licensed. Free for commercial and non-commercial use with attribution. The AEO Protocol specification this SDK implements is also MIT (see [aeo-protocol-spec](https://github.com/mizcausevic-dev/aeo-protocol-spec)).

## Kinetic Gain Protocol Suite

| Spec | Implementation |
|---|---|
| [AEO Protocol](https://github.com/mizcausevic-dev/aeo-protocol-spec) | **aeo-sdk-python** (this) · [aeo-sdk-typescript](https://github.com/mizcausevic-dev/aeo-sdk-typescript) · [aeo-sdk-rust](https://github.com/mizcausevic-dev/aeo-sdk-rust) · [aeo-sdk-go](https://github.com/mizcausevic-dev/aeo-sdk-go) · [aeo-cli](https://github.com/mizcausevic-dev/aeo-cli) · [aeo-crawler](https://github.com/mizcausevic-dev/aeo-crawler) |
| [Prompt Provenance](https://github.com/mizcausevic-dev/prompt-provenance-spec) | — |
| [Agent Cards](https://github.com/mizcausevic-dev/agent-cards-spec) | — |
| [AI Evidence Format](https://github.com/mizcausevic-dev/ai-evidence-format-spec) | — |
| [MCP Tool Cards](https://github.com/mizcausevic-dev/mcp-tool-card-spec) | — |

---

**Connect:** [LinkedIn](https://www.linkedin.com/in/mirzacausevic/) · [Kinetic Gain](https://kineticgain.com) · [Medium](https://medium.com/@mizcausevic/) · [Skills](https://mizcausevic.com/skills/)
