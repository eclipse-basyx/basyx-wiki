# Database Patch Structure

This page describes how database patch files are organized and named for the BaSyx Configuration Service. The structure keeps fresh installations, upgrades, and release reviews predictable.

## Versioning Strategy

Patch target versions use semantic versioning in the format:

```text
vMAJOR.MINOR.PATCH
```

The comparison also accepts values without the leading `v`, but repository patches should use the `v` prefix consistently.

## Recommended Folder Structure

```text
database/
  base.sql
  patches/
    1_0_1.sql
    1_0_2.sql
    1_1_0.sql
```

The Docker image copies the repository `database/` directory into `/app`, resulting in:

```text
/app/base.sql
/app/patches/1_0_1.sql
```

## File Naming Convention

Use sortable semantic-version-derived names that reflect version progression.

Examples:

| File | Target Version |
| --- | --- |
| `1_0_1.sql` | `v1.0.1` |
| `1_0_2.sql` | `v1.0.2` |
| `1_1_0.sql` | `v1.1.0` |

The current code does not discover patches automatically from filenames. The filename convention is for maintainability and review clarity.

## Ordering Strategy

Register patches in ascending version order. For example:

```go
schemInit.Register(steps.NewSchemaPatch(execCtx, filepath.Join(patchBasePath, "1_0_1.sql"), "v1.0.1"))
schemInit.Register(steps.NewSchemaPatch(execCtx, filepath.Join(patchBasePath, "1_0_2.sql"), "v1.0.2"))
schemInit.Register(steps.NewSchemaPatch(execCtx, filepath.Join(patchBasePath, "1_1_0.sql"), "v1.1.0"))
```

If the database is already at `v1.0.1`, the `v1.0.1` patch is skipped and later patches can run.

## Mandatory Version Update

Each patch must update the first row in `basyxsystem` to the patch target version:

```sql
UPDATE basyxsystem
SET database_version = 'v1.0.2'
WHERE identifier = (
  SELECT identifier
  FROM basyxsystem
  ORDER BY identifier ASC
  LIMIT 1
);
```

The `SystemTable` sequence guarantees that the table exists and contains a row before patches run.
