"""EU DPP Core Ontology alignment and namespace mapping.

Provides term mappings between UNTP vocabulary and the official EU DPP Core
Ontology from CIRPASS-2.

Source: EU DPP Core Ontology v1.7.1 (Product and DPP module)
Namespace: http://dpp.taltech.ee/EUDPP#
DOI: 10.5281/zenodo.15270342
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


class EUDPPNamespace(str, Enum):
    """EU DPP Core Ontology and related namespaces.

    Based on official CIRPASS-2 ontology v1.7.1.
    """

    # Official EU DPP Core Ontology namespace (TalTech)
    EUDPP = "http://dpp.taltech.ee/EUDPP#"

    # LCA module namespace (CEA France) - different origin
    LCA = "http://dpp.cea.fr/EUDPP/LCA#"

    # SI Digital Framework (measurement units)
    SI = "https://si-digital-framework.org/SI#"

    # QUDT Quantities, Units, Dimensions and Types
    QUDT = "http://qudt.org/schema/qudt#"

    # W3C SHACL namespace
    SH = "http://www.w3.org/ns/shacl#"

    # EU DPP Vocabulary Hub
    DPP_HUB = "https://dpp.vocabulary-hub.eu/"

    # W3C Verifiable Credentials v2
    VC2 = "https://www.w3.org/ns/credentials/v2"

    # UNTP DPP vocabulary
    UNTP_DPP = "https://test.uncefact.org/vocabulary/untp/dpp/"

    # Schema.org
    SCHEMA = "https://schema.org/"

    # GS1 vocabulary
    GS1 = "https://gs1.org/voc/"


# Backward compatibility alias
CIRPASSNamespace = EUDPPNamespace


class DPPStatus(str, Enum):
    """DPP instance status per EU DPP Core Ontology.

    The status of the DPP instance as a digital resource.
    """

    ACTIVE = "Active"
    ARCHIVED = "Archived"


class DPPGranularity(str, Enum):
    """DPP granularity level per ESPR and SR5423.

    The level of granularity of the ProductID as per ESPR.
    Values from official EU DPP Core Ontology.
    """

    MODEL = "model"  # All units of a product version
    BATCH = "batch"  # Subset from specific plant/time
    PRODUCT = "product"  # Single unit (official term, not 'item')


@dataclass(frozen=True, slots=True)
class TermMapping:
    """Mapping between UNTP term and CIRPASS ontology URI."""

    untp_term: str
    cirpass_uri: str
    description: str
    espr_reference: str | None = None


# Term mappings from UNTP to EU DPP Core Ontology
# Based on official CIRPASS-2 ontology v1.7.1
TERM_MAPPINGS: tuple[TermMapping, ...] = (
    # Core DPP and Product classes
    TermMapping(
        untp_term="DigitalProductPassport",
        cirpass_uri="eudpp:DPP",
        description="Digital Product Passport",
        espr_reference="ESPR Art 2(28)",
    ),
    TermMapping(
        untp_term="Product",
        cirpass_uri="eudpp:Product",
        description="Physical product placed on market",
        espr_reference="ESPR Art 2(1)",
    ),
    # Product identification
    TermMapping(
        untp_term="id",
        cirpass_uri="eudpp:uniqueDPPID",
        description="Unique DPP identifier (URI)",
        espr_reference="ESPR Art 9(1)",
    ),
    TermMapping(
        untp_term="serialNumber",
        cirpass_uri="eudpp:uniqueProductID",
        description="Unique product identifier",
        espr_reference="ESPR Art 2(30)",
    ),
    TermMapping(
        untp_term="name",
        cirpass_uri="eudpp:productName",
        description="Product name",
        espr_reference="ESPR Annex III",
    ),
    TermMapping(
        untp_term="description",
        cirpass_uri="eudpp:description",
        description="Product description",
        espr_reference="ESPR Annex III",
    ),
    TermMapping(
        untp_term="productImage",
        cirpass_uri="eudpp:productImage",
        description="Product image URI",
        espr_reference="ESPR Annex III",
    ),
    TermMapping(
        untp_term="gtin",
        cirpass_uri="eudpp:GTIN",
        description="Global Trade Identification Number",
        espr_reference="ISO/IEC 15459-6",
    ),
    TermMapping(
        untp_term="productCategory",
        cirpass_uri="eudpp:commodityCode",
        description="TARIC or commodity code",
        espr_reference="Council Regulation (EEC) No 2658/87",
    ),
    # Actor identification
    TermMapping(
        untp_term="issuer",
        cirpass_uri="eudpp:hasIssuer",
        description="DPP issuer (economic operator)",
        espr_reference="ESPR Annex III (g)",
    ),
    TermMapping(
        untp_term="producedByParty",
        cirpass_uri="eudpp:hasManufacturer",
        description="Product manufacturer",
        espr_reference="ESPR Annex III (g)",
    ),
    TermMapping(
        untp_term="producedAtFacility",
        cirpass_uri="eudpp:facilityID",
        description="Unique facility identifier",
        espr_reference="ESPR Art 2(33)",
    ),
    # Substances of concern
    TermMapping(
        untp_term="hazardous",
        cirpass_uri="eudpp:containsSubstanceOfConcern",
        description="Product contains substance of concern",
        espr_reference="ESPR Art 7(5)",
    ),
    # Validity and lifecycle
    TermMapping(
        untp_term="validFrom",
        cirpass_uri="eudpp:validFrom",
        description="DPP valid from date",
        espr_reference="ESPR Art 9(2i)",
    ),
    TermMapping(
        untp_term="validUntil",
        cirpass_uri="eudpp:validUntil",
        description="DPP valid until date",
        espr_reference="ESPR Art 9(2i)",
    ),
    TermMapping(
        untp_term="lastUpdate",
        cirpass_uri="eudpp:lastUpdate",
        description="Last DPP update timestamp",
        espr_reference="ESPR Art 11",
    ),
    TermMapping(
        untp_term="schemaVersion",
        cirpass_uri="eudpp:schemaVersion",
        description="Reference standard version",
        espr_reference="ESPR Art 9",
    ),
    TermMapping(
        untp_term="previousDPP",
        cirpass_uri="eudpp:linkToPreviousDPP",
        description="Link to previous DPP",
        espr_reference="ESPR Art 11(d)",
    ),
    # Granularity
    TermMapping(
        untp_term="granularityLevel",
        cirpass_uri="eudpp:granularity",
        description="DPP granularity (model/batch/product)",
        espr_reference="SR5423 Annex II Part B 1.1",
    ),
    # Product properties
    TermMapping(
        untp_term="characteristics",
        cirpass_uri="eudpp:hasProperty",
        description="Product property",
        espr_reference="ESPR Annex I",
    ),
    TermMapping(
        untp_term="isEnergyRelated",
        cirpass_uri="eudpp:isEnergyRelated",
        description="Energy-related product indicator",
        espr_reference="ESPR Art 2(4)",
    ),
    # Product relations
    TermMapping(
        untp_term="isComponentOf",
        cirpass_uri="eudpp:isComponentOf",
        description="Product is component of another",
        espr_reference="ESPR Art 2",
    ),
    TermMapping(
        untp_term="isSparePartOf",
        cirpass_uri="eudpp:isSparePartOf",
        description="Product is spare part of another",
        espr_reference="ESPR Art 2",
    ),
)


class OntologyMapper:
    """Maps UNTP terms to CIRPASS ontology URIs."""

    def __init__(self) -> None:
        """Initialize mapper with term mappings."""
        self._untp_to_cirpass: dict[str, TermMapping] = {m.untp_term: m for m in TERM_MAPPINGS}
        self._cirpass_to_untp: dict[str, TermMapping] = {m.cirpass_uri: m for m in TERM_MAPPINGS}

    def to_cirpass(self, untp_term: str) -> str | None:
        """Get CIRPASS URI for a UNTP term.

        Args:
            untp_term: UNTP vocabulary term

        Returns:
            CIRPASS ontology URI or None if not mapped
        """
        mapping = self._untp_to_cirpass.get(untp_term)
        return mapping.cirpass_uri if mapping else None

    def to_untp(self, cirpass_uri: str) -> str | None:
        """Get UNTP term for a CIRPASS URI.

        Args:
            cirpass_uri: CIRPASS ontology URI

        Returns:
            UNTP term or None if not mapped
        """
        mapping = self._cirpass_to_untp.get(cirpass_uri)
        return mapping.untp_term if mapping else None

    def get_mapping(self, term: str) -> TermMapping | None:
        """Get full mapping for a term (UNTP or CIRPASS).

        Args:
            term: UNTP term or CIRPASS URI

        Returns:
            TermMapping or None if not found
        """
        return self._untp_to_cirpass.get(term) or self._cirpass_to_untp.get(term)

    def get_espr_reference(self, untp_term: str) -> str | None:
        """Get ESPR reference for a UNTP term.

        Args:
            untp_term: UNTP vocabulary term

        Returns:
            ESPR reference string or None
        """
        mapping = self._untp_to_cirpass.get(untp_term)
        return mapping.espr_reference if mapping else None

    def iter_mappings(self) -> Iterator[TermMapping]:
        """Iterate over all term mappings.

        Yields:
            TermMapping instances
        """
        yield from TERM_MAPPINGS

    @property
    def mapped_terms(self) -> list[str]:
        """List of all mapped UNTP terms."""
        return list(self._untp_to_cirpass.keys())

    @property
    def mapping_count(self) -> int:
        """Number of term mappings."""
        return len(TERM_MAPPINGS)


def get_eudpp_context() -> dict[str, str]:
    """Get JSON-LD context with EU DPP Core Ontology namespace prefixes.

    Returns:
        Dictionary of namespace prefixes for JSON-LD @context
    """
    return {
        "eudpp": EUDPPNamespace.EUDPP.value,
        "lca": EUDPPNamespace.LCA.value,
        "si": EUDPPNamespace.SI.value,
        "qudt": EUDPPNamespace.QUDT.value,
        "sh": EUDPPNamespace.SH.value,
        "dpp": EUDPPNamespace.DPP_HUB.value,
        "untp": EUDPPNamespace.UNTP_DPP.value,
        "schema": EUDPPNamespace.SCHEMA.value,
        "gs1": EUDPPNamespace.GS1.value,
    }


# Backward compatibility alias
def get_cirpass_context() -> dict[str, str]:
    """Deprecated: Use get_eudpp_context instead."""
    return get_eudpp_context()


def expand_eudpp_uri(compact_uri: str) -> str:
    """Expand a compact EU DPP URI to full form.

    Args:
        compact_uri: URI like "eudpp:Product"

    Returns:
        Full URI like "http://dpp.taltech.ee/EUDPP#Product"
    """
    if ":" not in compact_uri:
        return compact_uri

    prefix, local = compact_uri.split(":", 1)
    namespaces = {ns.name.lower(): ns.value for ns in EUDPPNamespace}

    base = namespaces.get(prefix.lower())
    if base:
        return f"{base}{local}"

    return compact_uri


def compact_eudpp_uri(full_uri: str) -> str:
    """Compact a full EU DPP URI to prefixed form.

    Args:
        full_uri: Full URI

    Returns:
        Compact URI with namespace prefix
    """
    for ns in EUDPPNamespace:
        if full_uri.startswith(ns.value):
            local = full_uri[len(ns.value) :]
            return f"{ns.name.lower()}:{local}"

    return full_uri


# Backward compatibility aliases
def expand_cirpass_uri(compact_uri: str) -> str:
    """Deprecated: Use expand_eudpp_uri instead."""
    return expand_eudpp_uri(compact_uri)


def compact_cirpass_uri(full_uri: str) -> str:
    """Deprecated: Use compact_eudpp_uri instead."""
    return compact_eudpp_uri(full_uri)
