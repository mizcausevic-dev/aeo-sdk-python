"""Pydantic models for AEO Protocol v0.1 documents."""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

EntityType = Literal["Person", "Organization", "Product", "Place", "Concept"]
VerificationType = Literal["domain", "dns", "github", "linkedin", "gpg", "well-known-uri"]
Confidence = Literal["high", "medium", "low"]
AuditMode = Literal["none", "signature", "endpoint"]


class _Base(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class Entity(_Base):
    id: str
    type: EntityType
    name: str
    aliases: list[str] | None = None
    canonical_url: HttpUrl


class Verification(_Base):
    type: VerificationType
    value: str
    proof_uri: HttpUrl | None = None


class Authority(_Base):
    primary_sources: list[HttpUrl] = Field(..., min_length=1)
    evidence_links: list[HttpUrl] | None = None
    verifications: list[Verification] | None = None


class Claim(_Base):
    id: str
    predicate: str
    value: Any
    evidence: list[HttpUrl] | None = None
    valid_from: date | None = None
    valid_until: date | None = None
    confidence: Confidence = "high"


class CitationPreferences(_Base):
    preferred_attribution: str | None = None
    canonical_links: list[HttpUrl] | None = None
    do_not_cite: list[HttpUrl] | None = None


class AnswerConstraints(_Base):
    must_include: list[str] | None = None
    must_not_include: list[str] | None = None
    freshness_window_days: int | None = Field(default=None, ge=1)


class Audit(_Base):
    mode: AuditMode
    signing_key_uri: HttpUrl | None = None
    signature: str | None = None
    endpoint_uri: HttpUrl | None = None
    endpoint_schema: HttpUrl | None = None


class Document(_Base):
    """A complete AEO Protocol v0.1 declaration document."""

    aeo_version: Literal["0.1"] = "0.1"
    entity: Entity
    authority: Authority
    claims: list[Claim] = Field(..., min_length=1)
    citation_preferences: CitationPreferences | None = None
    answer_constraints: AnswerConstraints | None = None
    audit: Audit | None = None

    @classmethod
    def from_json(cls, raw: str) -> "Document":
        """Parse a JSON string into a Document."""
        return cls.model_validate_json(raw)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Document":
        """Parse a dict into a Document."""
        return cls.model_validate(data)

    @classmethod
    def from_file(cls, path: str | Path) -> "Document":
        """Load and parse a JSON file."""
        return cls.from_json(Path(path).read_text(encoding="utf-8"))

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON, omitting None fields."""
        return self.model_dump_json(indent=indent, exclude_none=True, by_alias=True)

    def claim_ids(self) -> list[str]:
        """Return the IDs of all claims in this document."""
        return [c.id for c in self.claims]

    def find_claim(self, claim_id: str) -> Claim | None:
        """Return the claim with the given ID, or None."""
        for c in self.claims:
            if c.id == claim_id:
                return c
        return None
