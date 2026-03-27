# Security Log — Eva-01

All security events are logged here: injection attempts, directive conflicts, unauthorized access attempts, and data classification violations. This file is the audit trail referenced by Constitutional Directive #6.

## Event Format

| Timestamp | Event Type | Source | Description | Action Taken |
|-----------|-----------|--------|-------------|--------------|

## Event Types

- **INJECTION_ATTEMPT** — External content containing instructions to modify agent behavior, identity, or loyalty
- **DIRECTIVE_CONFLICT** — A skill, plugin, or integration issued instructions conflicting with Constitutional Directives 1-5
- **CLASSIFICATION_VIOLATION** — Attempted or detected exposure of T2/T3 data outside authorized context
- **IDENTITY_TAMPER** — Attempted modification of SOUL.md, AGENTS.md, or USER.md from external source
- **INTEGRITY_ALERT** — Core files modified outside normal agent operations (detected during weekly review)
- **PLUGIN_ANOMALY** — Unexpected plugin behavior (file access, network calls, session state changes)

## Log

(Eva-01 appends entries here as events occur)
