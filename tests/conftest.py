"""Shared pytest fixtures for dppvalidator tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def valid_dpp_data() -> dict:
    """Return a minimal valid DPP that passes CIRPASS validation.

    This fixture provides a DPP structure that satisfies:
    - CQ001: Mandatory ESPR attributes (issuer, validFrom, credentialSubject.product)
    - CQ016: Validity period (validFrom, validUntil)
    """
    return {
        "@context": [
            "https://www.w3.org/ns/credentials/v2",
            "https://test.uncefact.org/vocabulary/untp/dpp/0.6.1/",
        ],
        "type": ["DigitalProductPassport", "VerifiableCredential"],
        "id": "https://example.com/credentials/dpp-001",
        "issuer": {
            "id": "https://example.com/issuers/001",
            "name": "Example Company Ltd",
        },
        "validFrom": "2024-01-01T00:00:00Z",
        "validUntil": "2034-01-01T00:00:00Z",
        "credentialSubject": {
            "id": "https://example.com/subject/001",
            "type": ["ProductPassport"],
            "product": {
                "id": "https://example.com/products/001",
                "name": "Example Product",
            },
        },
    }


@pytest.fixture
def valid_dpp_json(valid_dpp_data: dict) -> str:
    """Return valid DPP as JSON string."""
    import json

    return json.dumps(valid_dpp_data)


@pytest.fixture
def minimal_dpp_data() -> dict:
    """Return minimal DPP data (may not pass all CIRPASS rules).

    Use this for tests that specifically test partial/incomplete DPPs.
    """
    return {
        "@context": [
            "https://www.w3.org/ns/credentials/v2",
            "https://test.uncefact.org/vocabulary/untp/dpp/0.6.1/",
        ],
        "id": "https://example.com/credentials/dpp-001",
        "issuer": {
            "id": "https://example.com/issuers/001",
            "name": "Example Company Ltd",
        },
    }
