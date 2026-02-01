# CIRPASS-2 Implementation

dppvalidator supports dual-mode validation for both UNTP and CIRPASS-2 schemas,
enabling compliance with EU Digital Product Passport requirements.

## Overview

The CIRPASS-2 project developed reference schemas and SHACL shapes for EU DPP
validation. dppvalidator bundles these artifacts for offline validation.

## Schema Support

| Schema                 | Version | Source                |
| ---------------------- | ------- | --------------------- |
| CIRPASS-2 JSON Schema  | v1.3.0  | dpp.vocabulary-hub.eu |
| CIRPASS-2 SHACL Shapes | v1.3.0  | dpp.vocabulary-hub.eu |
| UNTP DPP Schema        | v0.6.1  | test.uncefact.org     |

## Basic Usage

### CIRPASS-2 Validation

```python
from dppvalidator.validators import ValidationEngine

# Enable CIRPASS-2 schema validation
engine = ValidationEngine(schema_type="cirpass")
result = engine.validate(dpp_data)

if result.valid:
    print("✓ CIRPASS-2 compliant")
else:
    for error in result.errors:
        print(f"✗ {error.code}: {error.message}")
```

### With SHACL Validation

For RDF-based constraint validation (requires `[rdf]` extra):

```bash
uv add "dppvalidator[rdf]"
```

```python
from dppvalidator.validators import ValidationEngine

# Enable both CIRPASS schema and SHACL validation
engine = ValidationEngine(
    schema_type="cirpass",
    enable_shacl=True,
)
result = engine.validate(dpp_data)
```

## CIRPASS Semantic Rules

dppvalidator implements CIRPASS-specific business rules with `CQ` prefix codes:

| Code  | Rule                                 | ESPR Reference |
| ----- | ------------------------------------ | -------------- |
| CQ001 | Mandatory ESPR attributes            | Art 8(2)       |
| CQ004 | Substances of Concern identification | Art 7(5a)      |
| CQ011 | Economic operator ID required        | Art 8(2)(b)    |
| CQ016 | Validity period required             | Art 8(2)(h)    |
| CQ021 | Product identifier format            | Art 8(2)(a)    |

### Example: Checking CIRPASS Rules

```python
from dppvalidator.validators import ValidationEngine

engine = ValidationEngine(schema_type="cirpass")
result = engine.validate(dpp_data)

# Filter CIRPASS-specific errors
cirpass_errors = [e for e in result.errors if e.code.startswith("CQ")]
for error in cirpass_errors:
    print(f"{error.code}: {error.message}")
```

## Schema Loader API

Direct access to CIRPASS schema for custom integrations:

```python
from dppvalidator.schemas.cirpass_loader import CIRPASSSchemaLoader

loader = CIRPASSSchemaLoader()
schema = loader.load()

print(f"Schema version: {loader.SCHEMA_VERSION}")  # 1.3.0
print(f"Schema ID: {loader.schema_id}")
```

## SHACL Validation API

For advanced RDF validation workflows:

```python
from dppvalidator.validators.shacl import (
    RDFSHACLValidator,
    OfficialSHACLLoader,
    validate_jsonld_with_official_shacl,
)

# Quick validation
result = validate_jsonld_with_official_shacl(dpp_jsonld)

# Or with custom shapes
loader = OfficialSHACLLoader()
shapes = loader.load()

validator = RDFSHACLValidator(shapes_graph=shapes)
shacl_result = validator.validate(dpp_jsonld)

print(f"Conforms: {shacl_result.conforms}")
for violation in shacl_result.violations:
    print(f"  - {violation}")
```

## Bundled Data Files

CIRPASS schemas and shapes are bundled for offline use:

```
vocabularies/data/schemas/
├── cirpass_dpp_schema.json     # JSON Schema v1.3.0
├── cirpass_dpp_shacl.ttl       # SHACL shapes
├── cirpass_openapi.yaml        # OpenAPI specification
└── cirpass_dpp.xsd             # XML Schema (reference)
```

## CLI Usage

Validate with CIRPASS schema from command line:

```bash
# CIRPASS validation
dppvalidator validate passport.json --schema-type cirpass

# With verbose output
dppvalidator validate passport.json --schema-type cirpass -f table
```

## Migration from UNTP

To validate existing UNTP DPPs against CIRPASS requirements:

```python
from dppvalidator.validators import ValidationEngine

# First validate against UNTP
untp_engine = ValidationEngine(schema_type="untp")
untp_result = untp_engine.validate(dpp_data)

# Then check CIRPASS compliance
cirpass_engine = ValidationEngine(schema_type="cirpass")
cirpass_result = cirpass_engine.validate(dpp_data)

# Compare results
print(f"UNTP valid: {untp_result.valid}")
print(f"CIRPASS valid: {cirpass_result.valid}")

# CIRPASS may have additional requirements
extra_errors = len(cirpass_result.errors) - len(untp_result.errors)
if extra_errors > 0:
    print(f"CIRPASS requires {extra_errors} additional fixes")
```

## References

- [CIRPASS-2 Project](https://cirpassproject.eu/)
- [CIRPASS Vocabulary Hub](https://dpp.vocabulary-hub.eu/)
- [ESPR Regulation](https://eur-lex.europa.eu/eli/reg/2024/1781)
- [UNTP Specification](https://untp.unece.org/)

## See Also

- [EU DPP Ontology Alignment](eudpp-ontology-alignment.md)
- [Seven-Layer Validation](validation-layers.md)
- [Error Reference](../errors/index.md)
