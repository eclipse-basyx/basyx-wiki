# Database Patch Structure

## Recommended Folder Structure

```text
database/
  base.sql
  patches/
    101.sql
    102.sql
    110.sql
```

The Docker image copies the repository `database/` directory into `/app`, resulting in:

```text
/app/base.sql
/app/patches/101.sql
```

## File Naming Convention

Use sortable numeric names that reflect version progression.

Examples:

| File | Target Version |
| --- | --- |
| `101.sql` | `v1.0.1` |
| `102.sql` | `v1.0.2` |
| `110.sql` | `v1.1.0` |

The current code does not discover patches automatically from filenames. The filename convention is for maintainability and review clarity.

## Ordering Strategy

Register patches in ascending version order. For example:

```go
schemInit.Register(steps.NewSchemaPatch(execCtx, filepath.Join(patchBasePath, "101.sql"), "v1.0.1"))
schemInit.Register(steps.NewSchemaPatch(execCtx, filepath.Join(patchBasePath, "102.sql"), "v1.0.2"))
schemInit.Register(steps.NewSchemaPatch(execCtx, filepath.Join(patchBasePath, "110.sql"), "v1.1.0"))
```

If the database is already at `v1.0.1`, the `v1.0.1` patch is skipped and later patches can run.

## Versioning Strategy

Patch target versions use semantic versioning in the format:

```text
vMAJOR.MINOR.PATCH
```

The comparison also accepts values without the leading `v`, but repository patches should use the `v` prefix consistently.

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

