# CLI Reference

Complete reference for the dppvalidator command line interface.

## Synopsis

```
dppvalidator [OPTIONS] COMMAND [ARGS]...
```

## Global Options

```text
--version    Show version and exit
--help       Show help message and exit
-v           Verbose output
-q           Quiet mode (suppress output)
```

## Commands

### validate

Validate one or more Digital Product Passports.

```
dppvalidator validate INPUT... [OPTIONS]
```

**Arguments:**

| Argument | Description                                                |
| -------- | ---------------------------------------------------------- |
| INPUT... | Path(s) to JSON file(s), glob pattern(s), or `-` for stdin |

Supports multiple files and glob patterns for batch validation.

**Options:**

| Option             | Default | Description                       |
| ------------------ | ------- | --------------------------------- |
| `-s, --strict`     | false   | Enable strict validation          |
| `-f, --format`     | text    | Output format (text, json, table) |
| `--schema-version` | 0.6.1   | Schema version                    |
| `--fail-fast`      | false   | Stop on first error               |
| `--max-errors`     | 100     | Maximum errors to report          |

### export

Export a DPP to different formats.

```
dppvalidator export INPUT [OPTIONS]
```

**Options:**

| Option         | Default | Description                  |
| -------------- | ------- | ---------------------------- |
| `-f, --format` | json    | Output format (json, jsonld) |
| `-o, --output` | stdout  | Output file path             |

### schema

Display schema information.

```
dppvalidator schema [OPTIONS]
```

**Options:**

| Option      | Description               |
| ----------- | ------------------------- |
| `--version` | Schema version to display |
| `--list`    | List available versions   |

## Exit Codes

| Code | Meaning           |
| ---- | ----------------- |
| 0    | Success / Valid   |
| 1    | Validation failed |
| 2    | Error             |

## Examples

```bash
# Validate a single file
dppvalidator validate passport.json

# Validate multiple files
dppvalidator validate passport1.json passport2.json passport3.json

# Validate with glob pattern
dppvalidator validate "data/passports/*.json"

# Batch validate with strict mode and JSON output
dppvalidator validate "data/*.json" --strict --format json

# Validate with table output (summary view)
dppvalidator validate "*.json" --format table

# Export to JSON-LD
dppvalidator export passport.json -f jsonld -o output.jsonld

# List schema versions
dppvalidator schema --list
```
