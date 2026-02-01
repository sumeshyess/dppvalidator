______________________________________________________________________

## description: CLI reference for validating and exporting DPPs.

# CLI Usage

The dppvalidator CLI provides commands for validating DPPs, exporting to different formats, and inspecting schemas.

## Commands

### validate

Validate one or more Digital Product Passport JSON files.

```
dppvalidator validate <input>... [options]
```

**Arguments:**

- `input...` — Path(s) to JSON file(s), glob pattern(s), or `-` for stdin

**Options:**

- `-s, --strict` — Enable strict JSON Schema validation
- `-f, --format` — Output format: `text`, `json`, `table` (default: text)
- `--schema-version` — Schema version (default: 0.6.1)
- `--fail-fast` — Stop on first error
- `--max-errors` — Maximum errors to report (default: 100)

**Examples:**

```bash
# Validate a single file
dppvalidator validate passport.json

# Validate multiple files
dppvalidator validate passport1.json passport2.json passport3.json

# Validate with glob pattern (quote to prevent shell expansion)
dppvalidator validate "data/passports/*.json"

# Batch validate entire directory
dppvalidator validate "data/**/*.json" --strict

# Validate from stdin
cat passport.json | dppvalidator validate -

# JSON output for CI/CD (includes summary for batch)
dppvalidator validate "*.json" --format json

# Table output for quick overview
dppvalidator validate "*.json" --format table
```

**Batch Output:**

When validating multiple files, the output includes a summary:

- **Text format**: Individual results + summary counts
- **JSON format**: `{"files": [...], "summary": {"total": N, "valid": N, "invalid": N}}`
- **Table format**: Status table with error/warning counts per file

### export

Export a DPP to different formats.

```
dppvalidator export <input> [options]
```

**Options:**

- `-f, --format` — Output format: `json`, `jsonld` (default: jsonld)
- `-o, --output` — Output file path (default: stdout)

**Examples:**

```
# Export to JSON-LD
dppvalidator export passport.json --format jsonld

# Save to file
dppvalidator export passport.json --format jsonld -o output.jsonld
```

### schema

Manage DPP schemas.

```
dppvalidator schema <subcommand> [options]
```

**Subcommands:**

- `list` — List available schema versions
- `info` — Show schema information
- `download` — Download a schema version

**Options (for info/download):**

- `-v, --version` — Schema version (default: 0.6.1)
- `-o, --output` — Output directory for download

**Examples:**

```
# List available versions
dppvalidator schema list

# Show schema info
dppvalidator schema info -v 0.6.1

# Download schema to local directory
dppvalidator schema download -v 0.6.1 -o ./schemas/
```

## Exit Codes

| Code | Meaning                                    |
| ---- | ------------------------------------------ |
| 0    | Validation passed                          |
| 1    | Validation failed                          |
| 2    | Error (file not found, invalid JSON, etc.) |

## Environment Variables

| Variable                      | Description                                 |
| ----------------------------- | ------------------------------------------- |
| `DPPVALIDATOR_SCHEMA_VERSION` | Default schema version                      |
| `DPPVALIDATOR_LOG_LEVEL`      | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Next Steps

- [Validation Guide](validation.md) — Understanding validation layers
- [JSON-LD Export](jsonld.md) — Working with JSON-LD output
