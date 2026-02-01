"""EU DPP-aligned JSON-LD export for Digital Product Passports.

Provides optional EU DPP-aligned JSON-LD output that transforms UNTP models
to the EU DPP Core Ontology vocabulary. The UNTP models remain unchanged;
this export layer performs vocabulary mapping at export time.

Source: EU DPP Core Ontology v1.7.1
Namespace: http://dpp.taltech.ee/EUDPP#
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING, Any

from dppvalidator.logging import get_logger
from dppvalidator.vocabularies.ontology import (
    TERM_MAPPINGS,
    EUDPPNamespace,
    OntologyMapper,
    get_eudpp_context,
)

if TYPE_CHECKING:
    from dppvalidator.models.passport import DigitalProductPassport

logger = get_logger(__name__)


# =============================================================================
# EU DPP Context Definitions
# =============================================================================


EUDPP_CONTEXT_URL = "https://dpp.vocabulary-hub.eu/context/v1"


def get_eudpp_jsonld_context() -> list[Any]:
    """Get the EU DPP JSON-LD @context array.

    Returns a context that includes:
    - W3C Verifiable Credentials v2
    - EU DPP Core Ontology namespaces
    - Term mappings for UNTP → EU DPP

    Returns:
        List of context definitions for JSON-LD @context
    """
    return [
        EUDPPNamespace.VC2.value,
        get_eudpp_context(),
    ]


# =============================================================================
# Term Mapping
# =============================================================================


class EUDPPTermMapper:
    """Map UNTP terms to EU DPP Core Ontology terms.

    Provides bidirectional mapping between UNTP vocabulary and
    EU DPP Core Ontology vocabulary for JSON-LD export.
    """

    def __init__(self) -> None:
        """Initialize term mapper."""
        self._mapper = OntologyMapper()
        self._untp_to_eudpp: dict[str, str] = {}
        self._eudpp_to_untp: dict[str, str] = {}

        for mapping in TERM_MAPPINGS:
            # Extract local name from compact URI (e.g., "eudpp:Product" -> "Product")
            eudpp_local = (
                mapping.cirpass_uri.split(":")[-1]
                if ":" in mapping.cirpass_uri
                else mapping.cirpass_uri
            )
            self._untp_to_eudpp[mapping.untp_term] = eudpp_local
            self._eudpp_to_untp[eudpp_local] = mapping.untp_term

    def map_key(self, untp_key: str) -> str:
        """Map a UNTP key to EU DPP equivalent.

        Args:
            untp_key: UNTP vocabulary key

        Returns:
            EU DPP key (or original if no mapping exists)
        """
        return self._untp_to_eudpp.get(untp_key, untp_key)

    def map_type(self, untp_type: str) -> str:
        """Map a UNTP type to EU DPP equivalent.

        Args:
            untp_type: UNTP type name

        Returns:
            EU DPP type with namespace prefix
        """
        mapped = self._untp_to_eudpp.get(untp_type)
        if mapped:
            return f"eudpp:{mapped}"
        return untp_type

    def get_eudpp_key(self, untp_key: str) -> str | None:
        """Get EU DPP key for UNTP key if mapped.

        Args:
            untp_key: UNTP vocabulary key

        Returns:
            EU DPP key or None if not mapped
        """
        return self._untp_to_eudpp.get(untp_key)

    @property
    def mapped_keys(self) -> list[str]:
        """List of UNTP keys that have EU DPP mappings."""
        return list(self._untp_to_eudpp.keys())


# =============================================================================
# EU DPP JSON-LD Exporter
# =============================================================================


class EUDPPJsonLDExporter:
    """Export UNTP models as EU DPP-aligned JSON-LD.

    This exporter transforms UNTP DPP models to use EU DPP Core Ontology
    vocabulary while preserving the original data structure. The UNTP
    models remain unchanged; only the export representation uses EU DPP terms.

    Example:
        >>> exporter = EUDPPJsonLDExporter()
        >>> jsonld = exporter.export(passport)
        >>> # Result uses EU DPP vocabulary with @context

    Attributes:
        include_untp_context: Include UNTP context alongside EU DPP
        map_terms: Apply term mapping (UNTP → EU DPP)
    """

    def __init__(
        self,
        *,
        include_untp_context: bool = False,
        map_terms: bool = True,
    ) -> None:
        """Initialize EU DPP exporter.

        Args:
            include_untp_context: Include UNTP context in output
            map_terms: Map UNTP terms to EU DPP equivalents
        """
        self._include_untp = include_untp_context
        self._map_terms = map_terms
        self._term_mapper = EUDPPTermMapper()

    def export(
        self,
        passport: DigitalProductPassport,
        *,
        indent: int | None = 2,
    ) -> str:
        """Export passport to EU DPP JSON-LD string.

        Args:
            passport: Validated DigitalProductPassport
            indent: JSON indentation (None for compact)

        Returns:
            EU DPP JSON-LD formatted string
        """
        data = self.export_dict(passport)
        return json.dumps(data, indent=indent, ensure_ascii=False, default=str)

    def export_dict(
        self,
        passport: DigitalProductPassport,
    ) -> dict[str, Any]:
        """Export passport to EU DPP JSON-LD dictionary.

        Args:
            passport: Validated DigitalProductPassport

        Returns:
            EU DPP JSON-LD formatted dictionary
        """
        # Get base UNTP JSON-LD representation
        base = passport.model_dump(mode="json", by_alias=True, exclude_none=True)

        # Apply EU DPP context
        data = self._apply_eudpp_context(base)

        # Map terms if enabled
        if self._map_terms:
            data = self._map_document_terms(data)

        # Add EU DPP-specific metadata
        data = self._add_eudpp_metadata(data, passport)

        logger.debug("Exported DPP to EU DPP JSON-LD format")
        return data

    def export_to_file(
        self,
        passport: DigitalProductPassport,
        path: Path | str,
        *,
        indent: int | None = 2,
    ) -> None:
        """Export passport to EU DPP JSON-LD file.

        Args:
            passport: Validated DigitalProductPassport
            path: Output file path
            indent: JSON indentation
        """
        content = self.export(passport, indent=indent)
        Path(path).write_text(content, encoding="utf-8")
        logger.info("Exported EU DPP JSON-LD to %s", path)

    def _apply_eudpp_context(self, data: dict[str, Any]) -> dict[str, Any]:
        """Apply EU DPP @context to the document.

        Args:
            data: JSON-LD dictionary

        Returns:
            Dictionary with EU DPP @context
        """
        result = deepcopy(data)

        # Build context array
        context: list[Any] = [EUDPPNamespace.VC2.value]

        # Add EU DPP namespace context
        context.append(get_eudpp_context())

        # Optionally include UNTP context
        if self._include_untp:
            context.append({"untp": EUDPPNamespace.UNTP_DPP.value})

        result["@context"] = context
        return result

    def _map_document_terms(self, data: dict[str, Any]) -> dict[str, Any]:
        """Recursively map UNTP terms to EU DPP equivalents.

        Args:
            data: JSON-LD dictionary

        Returns:
            Dictionary with mapped terms
        """
        if not isinstance(data, dict):
            return data

        result: dict[str, Any] = {}

        for key, value in data.items():
            # Don't map special JSON-LD keys
            if key.startswith("@"):
                result[key] = value
                continue

            # Map the key
            mapped_key = self._term_mapper.map_key(key)

            # Recursively process values
            if isinstance(value, dict):
                result[mapped_key] = self._map_document_terms(value)
            elif isinstance(value, list):
                result[mapped_key] = [
                    self._map_document_terms(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[mapped_key] = value

        # Map type values
        if "type" in result:
            result["type"] = self._map_type_value(result["type"])

        return result

    def _map_type_value(self, type_value: Any) -> Any:
        """Map type values to EU DPP equivalents.

        Args:
            type_value: Type string or list

        Returns:
            Mapped type value(s)
        """
        if isinstance(type_value, str):
            return self._term_mapper.map_type(type_value)
        elif isinstance(type_value, list):
            return [self._term_mapper.map_type(t) if isinstance(t, str) else t for t in type_value]
        return type_value

    def _add_eudpp_metadata(
        self, data: dict[str, Any], passport: DigitalProductPassport
    ) -> dict[str, Any]:
        """Add EU DPP-specific metadata to the document.

        Args:
            data: JSON-LD dictionary
            passport: Source passport

        Returns:
            Dictionary with EU DPP metadata
        """
        # Add schema reference
        if "schemaVersion" not in data:
            data["schemaVersion"] = "CIRPASS-2 v1.3.0"

        # Add status if credential subject has it
        if passport.credential_subject:
            cs = passport.credential_subject
            # Add granularity level with EU DPP term
            if hasattr(cs, "granularity_level") and cs.granularity_level:
                data["granularity"] = cs.granularity_level

        return data


# =============================================================================
# Convenience Functions
# =============================================================================


def export_eudpp_jsonld(
    passport: DigitalProductPassport,
    *,
    indent: int = 2,
    map_terms: bool = True,
) -> str:
    """Export a DPP to EU DPP-aligned JSON-LD format.

    Convenience function for simple exports. For more control,
    use EUDPPJsonLDExporter directly.

    Args:
        passport: Validated DigitalProductPassport
        indent: JSON indentation
        map_terms: Map UNTP terms to EU DPP equivalents

    Returns:
        EU DPP JSON-LD formatted string
    """
    exporter = EUDPPJsonLDExporter(map_terms=map_terms)
    return exporter.export(passport, indent=indent)


def export_eudpp_jsonld_dict(
    passport: DigitalProductPassport,
    *,
    map_terms: bool = True,
) -> dict[str, Any]:
    """Export a DPP to EU DPP-aligned JSON-LD dictionary.

    Convenience function for dictionary output.

    Args:
        passport: Validated DigitalProductPassport
        map_terms: Map UNTP terms to EU DPP equivalents

    Returns:
        EU DPP JSON-LD dictionary
    """
    exporter = EUDPPJsonLDExporter(map_terms=map_terms)
    return exporter.export_dict(passport)


def validate_eudpp_export(data: dict[str, Any]) -> list[str]:
    """Validate EU DPP JSON-LD export structure.

    Checks that the export contains required EU DPP elements.

    Args:
        data: Exported JSON-LD dictionary

    Returns:
        List of validation issues (empty if valid)
    """
    issues: list[str] = []

    # Check @context
    if "@context" not in data:
        issues.append("Missing @context")
    else:
        context = data["@context"]
        if not isinstance(context, list):
            issues.append("@context should be a list")
        else:
            # Check for VC2 context
            if EUDPPNamespace.VC2.value not in context:
                issues.append("Missing W3C VC2 context")

            # Check for EU DPP namespace
            has_eudpp = any(isinstance(c, dict) and "eudpp" in c for c in context)
            if not has_eudpp:
                issues.append("Missing EU DPP namespace in context")

    # Check for type
    if "type" not in data:
        issues.append("Missing type")

    return issues


def get_term_mapping_summary() -> dict[str, str]:
    """Get a summary of UNTP to EU DPP term mappings.

    Returns:
        Dictionary mapping UNTP terms to EU DPP terms
    """
    mapper = EUDPPTermMapper()
    return {term: mapper.map_key(term) for term in mapper.mapped_keys}
