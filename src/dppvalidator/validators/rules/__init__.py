"""Pluggable semantic validation rules."""

from dppvalidator.validators.rules.base import (
    CircularityContentRule,
    ConformityClaimRule,
    GranularitySerialNumberRule,
    GTINChecksumRule,
    HazardousMaterialRule,
    HSCodeRule,
    MassFractionSumRule,
    MaterialCodeRule,
    OperationalScopeRule,
    ValidityDateRule,
)
from dppvalidator.validators.rules.cirpass import (
    CIRPASS_RULES,
    CIRPASSGranularityConsistencyRule,
    CIRPASSMandatoryAttributesRule,
    CIRPASSOperatorIdentifierRule,
    CIRPASSSubstancesOfConcernRule,
    CIRPASSValidityPeriodRule,
    CIRPASSWeightVolumeRule,
)
from dppvalidator.validators.rules.textile import (
    TEXTILE_RULES,
    TextileCareInstructionsRule,
    TextileDurabilityRule,
    TextileEnvironmentalCategory,
    TextileHSCodeRule,
    TextileMaterialCompositionRule,
    TextileMicroplasticRule,
    get_textile_environmental_categories,
    is_textile_product,
)

ALL_RULES = [
    # Base UNTP rules
    MassFractionSumRule(),
    ValidityDateRule(),
    HazardousMaterialRule(),
    CircularityContentRule(),
    ConformityClaimRule(),
    GranularitySerialNumberRule(),
    OperationalScopeRule(),
    MaterialCodeRule(),
    HSCodeRule(),
    GTINChecksumRule(),
    # CIRPASS-2 rules (CQ-based)
    *CIRPASS_RULES,
]

__all__ = [
    "ALL_RULES",
    # Base rules
    "MassFractionSumRule",
    "ValidityDateRule",
    "HazardousMaterialRule",
    "CircularityContentRule",
    "ConformityClaimRule",
    "GranularitySerialNumberRule",
    "OperationalScopeRule",
    "MaterialCodeRule",
    "HSCodeRule",
    "GTINChecksumRule",
    # CIRPASS-2 rules
    "CIRPASS_RULES",
    "CIRPASSMandatoryAttributesRule",
    "CIRPASSSubstancesOfConcernRule",
    "CIRPASSOperatorIdentifierRule",
    "CIRPASSValidityPeriodRule",
    "CIRPASSWeightVolumeRule",
    "CIRPASSGranularityConsistencyRule",
    # Textile sector rules
    "TEXTILE_RULES",
    "TextileHSCodeRule",
    "TextileMaterialCompositionRule",
    "TextileMicroplasticRule",
    "TextileDurabilityRule",
    "TextileCareInstructionsRule",
    "TextileEnvironmentalCategory",
    "is_textile_product",
    "get_textile_environmental_categories",
]
