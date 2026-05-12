"""HTTP client helpers for the AEO Protocol discovery convention."""
from __future__ import annotations

import httpx

from aeo.document import Document

_WELL_KNOWN_PATH = "/.well-known/aeo.json"
_ACCEPTED_MEDIA_TYPES = "application/aeo+json, application/json"


def well_known_url(origin: str) -> str:
    """Return the canonical well-known URL for an origin.

    Strips trailing slashes from the origin and appends the
    AEO Protocol well-known path.
    """
    return origin.rstrip("/") + _WELL_KNOWN_PATH


def fetch_well_known(
    origin: str,
    *,
    timeout: float = 10.0,
    follow_redirects: bool = True,
) -> Document:
    """Fetch and parse the AEO declaration at ``origin``'s well-known URL.

    Raises ``httpx.HTTPStatusError`` for non-2xx responses and
    ``pydantic.ValidationError`` for malformed documents.
    """
    url = well_known_url(origin)
    with httpx.Client(
        timeout=timeout,
        follow_redirects=follow_redirects,
        headers={"Accept": _ACCEPTED_MEDIA_TYPES},
    ) as client:
        response = client.get(url)
        response.raise_for_status()
        return Document.from_json(response.text)


async def fetch_well_known_async(
    origin: str,
    *,
    timeout: float = 10.0,
    follow_redirects: bool = True,
) -> Document:
    """Async variant of ``fetch_well_known``."""
    url = well_known_url(origin)
    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=follow_redirects,
        headers={"Accept": _ACCEPTED_MEDIA_TYPES},
    ) as client:
        response = await client.get(url)
        response.raise_for_status()
        return Document.from_json(response.text)
