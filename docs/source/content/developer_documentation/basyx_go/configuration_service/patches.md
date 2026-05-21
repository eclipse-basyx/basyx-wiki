# Creating and Managing Patches

Patches are SQL files applied by `SchemaPatch` sequences. They are used for schema changes after the base schema version.

## Patch Structure

A patch should include:

- A header describing the patch version and purpose.
- Idempotent schema changes where practical.
- A final update to `basyxsystem.database_version`.

Example:

```sql
-- ============================================================================
-- Project        : Eclipse BaSyx
-- File Type      : SQL Patch Script
-- Patch Version  : 1.0.2
-- Description    : Adds example table indexes.
-- ============================================================================

CREATE INDEX IF NOT EXISTS ix_example_table_name ON example_table(name);

UPDATE basyxsystem
SET database_version = 'v1.0.2'
WHERE identifier = (
  SELECT identifier
  FROM basyxsystem
  ORDER BY identifier ASC
  LIMIT 1
);
```

## Version Handling Requirements

The Go code decides whether to execute a patch by comparing:

- The current database version from `basyxsystem.database_version`.
- The target version passed to `NewSchemaPatch`.

The patch SQL file is responsible for updating the database version. The Go patch sequence does not update the version after executing the patch.

This means every patch that changes the schema version must include an `UPDATE basyxsystem SET database_version = ...` statement.

## Registering a Patch

Patch files are registered explicitly in `main.go`:

```go
schemInit.Register(steps.NewSchemaPatch(execCtx, filepath.Join(patchBasePath, "101.sql"), "v1.0.1"))
```

To add a new patch, register it after older patches:

```go
schemInit.Register(steps.NewSchemaPatch(execCtx, filepath.Join(patchBasePath, "102.sql"), "v1.0.2"))
schemInit.Register(steps.NewSchemaPatch(execCtx, filepath.Join(patchBasePath, "110.sql"), "v1.1.0"))
```

## Mandatory Patch Contents

Every released patch must include:

- SQL changes required for that version.
- Safe guards such as `IF EXISTS` or `IF NOT EXISTS` where appropriate.
- A database version update to the target version.
- A version value matching the target version registered in Go.

## Important Patch Disclaimer

> Existing patches must NEVER be modified after release.

Released patches are part of the migration history. Changing an already released patch can break reproducibility because two installations may both claim to have applied the same patch version while having different database structures.

If a released patch contains an issue, create a new patch that corrects it. Do not edit the old patch.

## Why This Rule Matters

Immutable patches provide:

- Reproducible migrations across environments.
- Consistent troubleshooting and support.
- Deterministic upgrade paths.
- Clear auditability of database changes.

