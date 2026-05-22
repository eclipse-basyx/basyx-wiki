# Architecture Overview

The BaSyx Configuration Service is a one-shot command-line service. It does not expose API endpoints and does not run as a daemon.

## Main Components

```{uml} charts/configuration_service_architecture.puml
```

| No. | Component | Responsibility |
| --- | --- | --- |
| 1 | Service entry point | Parses flags, creates the shared execution context, registers sequences, and executes the initializer. |
| 2 | Schema initializer | Stores ordered sequences and executes them one after another. |
| 3 | Sequence interface | Defines the executable contract for initialization steps. |
| 4 | Execution context | Shares loaded configuration and the database handle between sequences. |
| 5 | Database connection sequence | Loads config, builds the PostgreSQL DSN, opens the database connection, and applies pool settings. |
| 6 | System table sequence | Creates and seeds `basyxsystem` when required. |
| 7 | Schema upload sequence | Uploads `base.sql` when the base schema is not initialized. |
| 8 | Schema patch sequence | Applies a registered patch when the database version is older than the patch target version. |
| 9 | PostgreSQL database | Stores the BaSyx schema, system version row, and application data. |
| 10 | Configuration object | Holds the loaded service and PostgreSQL settings used by later sequences. |
| 11 | Database handle object | Provides the opened PostgreSQL connection handle stored in the execution context. |

Implementation locations:

- 1: `cmd/basyxconfigurationservice/main.go`
- 2: `internal/basyxconfigurationservice/schema_initializer.go`
- 3: `internal/basyxconfigurationservice/sequences/i_sequence.go`
- 4: `internal/basyxconfigurationservice/sequences/execution_context.go`
- 5: `internal/basyxconfigurationservice/sequences/database.go`
- 6: `internal/basyxconfigurationservice/sequences/system_table.go`
- 7: `internal/basyxconfigurationservice/sequences/schema_upload.go`
- 8: `internal/basyxconfigurationservice/sequences/schema_patch.go`

## Interaction Overview

The entry point registers sequences explicitly. The initializer does not discover sequences automatically. Each sequence receives the same `ExecutionContext`, allowing earlier sequences to provide state for later sequences.

The database connection sequence populates the context with `Config` and `DB`. `Config` provides the loaded configuration values, especially PostgreSQL connection and pool settings. `DB` is the opened PostgreSQL handle used by all later database-related sequences to execute SQL against PostgreSQL.
