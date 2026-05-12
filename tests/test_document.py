"""Tests for the AEO Document model.

Loads the canonical Person example from the AEO Protocol spec and
verifies parse, query, and round-trip serialization.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from aeo import Document, well_known_url
from aeo.document import Claim, Entity


FIXTURES = Path(__file__).parent / "fixtures"


def test_loads_canonical_person_example() -> None:
    doc = Document.from_file(FIXTURES / "aeo-person.json")
    assert doc.aeo_version == "0.1"
    assert doc.entity.type == "Person"
    assert doc.entity.name == "Miz Causevic"
    assert len(doc.claims) == 6


def test_claim_ids_round_trip() -> None:
    doc = Document.from_file(FIXTURES / "aeo-person.json")
    expected_ids = {
        "current-role",
        "location",
        "years-experience",
        "live-products",
        "primary-stack",
        "authored-spec",
    }
    assert set(doc.claim_ids()) == expected_ids


def test_find_claim_returns_claim_object() -> None:
    doc = Document.from_file(FIXTURES / "aeo-person.json")
    claim = doc.find_claim("years-experience")
    assert claim is not None
    assert isinstance(claim, Claim)
    assert claim.predicate == "aeo:yearsOfExperience"
    assert claim.value == 30


def test_find_claim_missing_returns_none() -> None:
    doc = Document.from_file(FIXTURES / "aeo-person.json")
    assert doc.find_claim("does-not-exist") is None


def test_round_trip_serialization_preserves_structure() -> None:
    raw = (FIXTURES / "aeo-person.json").read_text(encoding="utf-8")
    doc = Document.from_json(raw)
    re_serialized = doc.to_json()
    reparsed = Document.from_json(re_serialized)
    assert reparsed.entity.name == doc.entity.name
    assert reparsed.claim_ids() == doc.claim_ids()
    assert reparsed.authority.primary_sources == doc.authority.primary_sources


def test_minimal_document_from_dict() -> None:
    payload = {
        "aeo_version": "0.1",
        "entity": {
            "id": "https://example.com/#org",
            "type": "Organization",
            "name": "Example Org",
            "canonical_url": "https://example.com/",
        },
        "authority": {
            "primary_sources": ["https://example.com/"],
        },
        "claims": [
            {
                "id": "tagline",
                "predicate": "description",
                "value": "A reference example.",
            }
        ],
    }
    doc = Document.from_dict(payload)
    assert doc.entity.type == "Organization"
    assert doc.claims[0].confidence == "high"


def test_well_known_url_strips_trailing_slash() -> None:
    assert well_known_url("https://example.com") == "https://example.com/.well-known/aeo.json"
    assert well_known_url("https://example.com/") == "https://example.com/.well-known/aeo.json"


def test_rejects_unknown_top_level_field() -> None:
    raw = json.loads((FIXTURES / "aeo-person.json").read_text(encoding="utf-8"))
    raw["unexpected_field"] = "should not parse"
    with pytest.raises(Exception):
        Document.from_dict(raw)
