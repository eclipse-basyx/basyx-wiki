# Sequences

## What Are Sequences?

A sequence is one executable initialization step. Sequences are small, ordered units of work that implement the common `Sequence` interface:

```go
type Sequence interface {
    Execute(int) (int, error)
    GetDescription(int) string
}
```

The integer argument is the one-based sequence index used for logging and error reporting.

## Why Sequences Exist

Sequences keep startup logic modular and deterministic. Each step has a narrow responsibility, such as connecting to the database or applying one patch.

This structure avoids embedding all startup behavior in `main.go` and makes it easier to add new initialization steps without changing the initializer execution logic.

## Relationship Between Sequences and Patches

A patch is represented by a `SchemaPatch` sequence. The sequence owns the decision whether the patch file should run by comparing the current database version with the patch target version.

The patch SQL file owns the actual schema changes and must update `basyxsystem.database_version` itself.

## Ordering Semantics

Sequences run in the exact order in which they are registered:

```go
schemInit.Register(steps.NewDatabaseConnection(execCtx, configPath))
schemInit.Register(steps.NewSystemTable(execCtx))
schemInit.Register(steps.NewSchemaUpload(execCtx, databaseSchema))
schemInit.Register(steps.NewSchemaPatch(execCtx, filepath.Join(patchBasePath, "101.sql"), "v1.0.1"))
```

There is no automatic dependency resolver. If a sequence depends on state created by another sequence, it must be registered after that sequence.

## Execution Guarantees

The initializer guarantees:

- Sequential execution in registration order.
- Stop-on-first-error behavior.
- Consistent logging before and after each successful sequence.

The initializer does not provide automatic rollback across multiple sequences. Individual sequences must define their own transactional behavior when needed.

## Transaction and Rollback Considerations

`SchemaPatch` executes the patch SQL inside a database transaction. If patch execution fails, the transaction is rolled back.

`SchemaUpload` executes the full base schema SQL through the database handle without an explicit transaction wrapper in Go. The SQL file itself should remain safe and repeatable for initialization scenarios.

