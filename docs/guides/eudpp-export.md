# EU DPP JSON-LD Export Guide

> **Status:** ✅ Available
> **Since:** v0.7.0
> **Source:** CIRPASS-2 Official Ontology v1.7.1

This guide covers exporting Digital Product Passports to EU DPP-aligned JSON-LD
format using the CIRPASS-2 vocabulary.

## Overview

The EU DPP export functionality transforms UNTP DPP models to use the official
EU DPP Core Ontology vocabulary. The key principle is:

> **UNTP models remain unchanged** — the export layer transforms vocabulary
> at export time.

This means you can:

- Use the same UNTP models throughout your application
- Export to EU DPP-aligned format when needed
- Maintain full UNTP compatibility

## Quick Start

```python
from dppvalidator.exporters import EUDPPJsonLDExporter

# Create exporter with term mapping enabled
exporter = EUDPPJsonLDExporter(map_terms=True)

# Export passport to EU DPP JSON-LD
jsonld = exporter.export(passport)
print(jsonld)
```

## Exporter Options

### EUDPPJsonLDExporter

The main exporter class with configurable options:

```python
from dppvalidator.exporters import EUDPPJsonLDExporter

# Full control
exporter = EUDPPJsonLDExporter(
    map_terms=True,  # Map UNTP terms to EU DPP (default: True)
    include_untp_context=False,  # Include UNTP context in output (default: False)
)

# Export methods
jsonld_str = exporter.export(passport)  # Returns JSON string
jsonld_dict = exporter.export_dict(passport)  # Returns dictionary
exporter.export_to_file(passport, "output.jsonld")  # Writes to file
```

### Convenience Functions

For simple use cases:

```python
from dppvalidator.exporters import (
    export_eudpp_jsonld,
    export_eudpp_jsonld_dict,
)

# String output
jsonld = export_eudpp_jsonld(passport)

# Dictionary output
data = export_eudpp_jsonld_dict(passport, map_terms=True)
```

## Term Mapping

The exporter maps UNTP terms to EU DPP Core Ontology terms:

| UNTP Term                | EU DPP Term       |
| ------------------------ | ----------------- |
| `id`                     | `uniqueDPPID`     |
| `DigitalProductPassport` | `eudpp:DPP`       |
| `Product`                | `eudpp:Product`   |
| `validFrom`              | `eudpp:validFrom` |
| `issuer`                 | `eudpp:hasIssuer` |

### Viewing Term Mappings

```python
from dppvalidator.exporters import get_term_mapping_summary

mappings = get_term_mapping_summary()
for untp_term, eudpp_term in mappings.items():
    print(f"{untp_term} → {eudpp_term}")
```

## JSON-LD Context

The exported JSON-LD includes the proper EU DPP context:

```python
from dppvalidator.exporters import get_eudpp_jsonld_context

context = get_eudpp_jsonld_context()
# Returns:
# [
#   "https://www.w3.org/ns/credentials/v2",
#   {"eudpp": "http://dpp.taltech.ee/EUDPP#", ...}
# ]
```

## Validating Exports

Validate that an export has the required EU DPP structure:

```python
from dppvalidator.exporters import validate_eudpp_export

data = exporter.export_dict(passport)
issues = validate_eudpp_export(data)

if issues:
    print("Export validation issues:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✅ Valid EU DPP export")
```

## Example Output

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    {
      "eudpp": "http://dpp.taltech.ee/EUDPP#",
      "schema": "https://schema.org/",
      "xsd": "http://www.w3.org/2001/XMLSchema#"
    }
  ],
  "type": ["eudpp:DPP", "VerifiableCredential"],
  "uniqueDPPID": "urn:uuid:12345-abcde",
  "schemaVersion": "CIRPASS-2 v1.3.0",
  "granularity": "model",
  "credentialSubject": {
    "product": {
      "type": "eudpp:Product",
      "productName": "Sustainable T-Shirt",
      "uniqueProductID": "urn:gtin:1234567890123"
    }
  }
}
```

## Dual-Mode Validation

Combine EU DPP export with CIRPASS schema validation:

```python
from dppvalidator.validators import SchemaValidator
from dppvalidator.exporters import EUDPPJsonLDExporter

# Validate with CIRPASS schema
validator = SchemaValidator(schema_type="cirpass")
result = validator.validate(dpp_data)

if result.valid:
    # Export to EU DPP format
    exporter = EUDPPJsonLDExporter()
    jsonld = exporter.export(passport)
```

## SHACL Validation (Optional)

For full RDF-based SHACL validation, install the RDF extras:

```bash
pip install dppvalidator[rdf]
```

Then validate against official SHACL shapes:

```python
from dppvalidator.validators import (
    RDFSHACLValidator,
    is_shacl_validation_available,
)

if is_shacl_validation_available():
    validator = RDFSHACLValidator(use_official_shapes=True)
    result = validator.validate_jsonld(jsonld_data)

    if result.conforms:
        print("✅ Valid against SHACL shapes")
    else:
        for violation in result.violations:
            print(f"✗ {violation['path']}: {violation['message']}")
```

## API Reference

### Classes

| Class                 | Description          |
| --------------------- | -------------------- |
| `EUDPPJsonLDExporter` | Main exporter class  |
| `EUDPPTermMapper`     | Term mapping utility |

### Functions

| Function                     | Description               |
| ---------------------------- | ------------------------- |
| `export_eudpp_jsonld()`      | Export to JSON-LD string  |
| `export_eudpp_jsonld_dict()` | Export to dictionary      |
| `get_eudpp_jsonld_context()` | Get JSON-LD @context      |
| `get_term_mapping_summary()` | Get term mapping dict     |
| `validate_eudpp_export()`    | Validate export structure |

## See Also

- [CIRPASS-2 Integration](../concepts/cirpass-implementation.md)
- [EU DPP Ontology Alignment](../concepts/eudpp-ontology-alignment.md)
- [JSON-LD Export](jsonld.md)
