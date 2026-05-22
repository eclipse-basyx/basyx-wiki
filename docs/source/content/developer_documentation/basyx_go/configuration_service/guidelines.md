# Developer Guidelines

This page summarizes the development rules for changing or extending the BaSyx Configuration Service. It focuses on the areas where contributors most often affect runtime behavior: sequence registration, SQL patch handling, compatibility with existing databases, idempotent startup behavior, logging, and tests.

## Safe Extension Points

Preferred extension points are:

- New sequence implementations in `internal/basyxconfigurationservice/sequences`.
- Additional explicit sequence registrations in `cmd/basyxconfigurationservice/main.go`.
- New SQL patch files in `database/patches`.
- Additional tests for new sequence behavior.

## Stability Considerations

The Configuration Service runs before other BaSyx services. A failure blocks dependent services from starting, so changes should be conservative and deterministic.

When extending the service:

- Preserve the run-once-and-exit behavior.
- Avoid background goroutines or server loops unless the service goal changes explicitly.
- Keep startup work deterministic.
- Avoid non-idempotent operations in restartable sequences.
- Keep database patch history immutable.

## Backward Compatibility

Database changes must consider existing installations. If a database may already contain older data, patches should migrate that data safely.

Avoid assumptions that are only true for fresh databases. The service supports fresh initialization and upgrades from an existing version row.

## Idempotency

Initialization steps may be retried by container platforms. Sequences should therefore be safe to run more than once whenever possible.

Use patterns such as:

- `CREATE TABLE IF NOT EXISTS`
- `ALTER TABLE IF EXISTS ... ADD COLUMN IF NOT EXISTS`
- `CREATE INDEX IF NOT EXISTS`
- Version checks before patch execution

## Logging and Observability

Each sequence should provide a clear `GetDescription` result and return errors with stable error codes. This makes deployment logs useful when startup fails.

Recommended error-code format:

```text
BASYXCFG-COMPONENT-STEP: detailed error
```

Examples:

- `BASYXCFG-DB-CONNECT`
- `BASYXCFG-SYSTEM-CREATETABLE`
- `BASYXCFG-SCHEMA-EXECUTE`
- `BASYXCFG-PATCH-EXECUTE`

## Testing Recommendations

For sequence changes, add unit tests with SQL expectations where practical. Useful test cases include:

- Missing database handle.
- Successful execution.
- SQL execution failure.
- Skip behavior when initialization is already complete.
- Patch version comparison behavior.

For database patches, prefer integration testing against PostgreSQL before release because SQL syntax and DDL behavior are database-specific.
