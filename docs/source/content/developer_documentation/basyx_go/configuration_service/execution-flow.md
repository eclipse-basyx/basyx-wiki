# Execution Flow

## Startup Lifecycle

The service lifecycle is deterministic and runs before the BaSyx services start:

1. Parse command-line flags.
2. Create an empty `ExecutionContext`.
3. Create a `SchemaInitializer`.
4. Register sequences in the intended execution order.
5. Execute all sequences sequentially.
6. Close the database handle.
7. Exit with status `0` on success or status `1` on failure.

## Current Registered Order

The service currently registers:

1. `DatabaseConnection`
2. `SystemTable`
3. `SchemaUpload`
4. `SchemaPatch` for `101.sql` targeting `v1.0.1`

These components are described in the [architecture overview](architecture.md).

## Flow Diagram

```mermaid
sequenceDiagram
    participant Main as main.go
    participant Init as SchemaInitializer
    participant DB as DatabaseConnection
    participant System as SystemTable
    participant Upload as SchemaUpload
    participant Patch as SchemaPatch
    participant PG as PostgreSQL

    Main->>Init: Register sequences
    Main->>Init: Execute()
    Init->>DB: Execute(1)
    DB->>PG: Connect and ping
    DB-->>Init: ctx.DB populated
    Init->>System: Execute(2)
    System->>PG: Acquire advisory lock
    System->>PG: CREATE TABLE IF NOT EXISTS basyxsystem
    System->>PG: INSERT v1.0.0 if no row exists
    System->>PG: Release advisory lock
    Init->>Upload: Execute(3)
    Upload->>PG: Acquire advisory lock
    Upload->>PG: Check base schema marker tables
    alt Base schema missing
        Upload->>PG: Execute base.sql
    else Base schema present
        Upload-->>Init: Skip upload
    end
    Upload->>PG: Release advisory lock
    Init->>Patch: Execute(4)
    Patch->>PG: Acquire advisory lock
    Patch->>PG: Read basyxsystem.database_version
    alt Current version lower than target
        Patch->>PG: Begin transaction
        Patch->>PG: Execute patch SQL
        Patch->>PG: Commit transaction
    else Current version equal or newer
        Patch-->>Init: Skip patch
    end
    Patch->>PG: Release advisory lock
    Init-->>Main: Success or error
```

```{hint}
The diagram shows the current example with one registered patch path to `v1.0.1`. If multiple patches are registered, the `SchemaPatch` step repeats in registration order.
```

## Error Handling

`SchemaInitializer.Execute()` stops on the first sequence error. Errors are wrapped with `BASYXCFG-INIT-EXECSTEP`, including the failed sequence index and status code.

Sequences return:

- `0, nil` on success.
- Non-zero status and an error on failure.

The main function logs the wrapped error as `BASYXCFG-MAIN-EXECUTE` and exits with status `1`.

## Locking Behavior

`SystemTable`, `SchemaUpload`, and `SchemaPatch` use the same PostgreSQL advisory lock ID. This serializes schema changes across concurrent Configuration Service instances.

The patch sequence acquires the advisory lock before reading the current database version. This prevents two instances from both deciding that a patch must run based on the same old version.
