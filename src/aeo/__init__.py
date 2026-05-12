"""Python SDK for the AEO Protocol v0.1.

Parse, build, validate, and fetch AEO declaration documents.

Specification: https://github.com/mizcausevic-dev/aeo-protocol-spec
"""
from aeo.document import (
    AnswerConstraints,
    Audit,
    Authority,
    CitationPreferences,
    Claim,
    Document,
    Entity,
    Verification,
)
from aeo.client import fetch_well_known, well_known_url

__all__ = [
    "AnswerConstraints",
    "Audit",
    "Authority",
    "CitationPreferences",
    "Claim",
    "Document",
    "Entity",
    "Verification",
    "fetch_well_known",
    "well_known_url",
]

__version__ = "0.1.0"
PROTOCOL_VERSION = "0.1"
