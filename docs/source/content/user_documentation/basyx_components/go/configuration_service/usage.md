# Basic Usage

The BaSyx Configuration Service is designed as a run-once startup job. It executes its registered initialization sequences and then exits.

## Startup Flow

1. Load the configured PostgreSQL connection settings.
2. Connect to PostgreSQL.
3. Ensure the `basyxsystem` table exists and contains an initial version row.
4. Upload the base schema when the base schema tables are not present.
5. Apply registered schema patches if the database version is older than the patch target version.
6. Exit successfully or fail with a non-zero exit code.

## Command-Line Options

The service binary supports these options:

```bash
/app/basyxconfigurationservice \
  -config /app/config.yaml \
  -databaseSchema /app/base.sql \
  -customPatchPath /app/patches
```

| Option | Purpose | Default |
| --- | --- | --- |
| `-config` | Path to the BaSyx configuration file. | Empty path, using common config loading behavior. |
| `-databaseSchema` | Path to the base schema SQL file or a directory containing `base.sql`. | `/app/base.sql` |
| `-customPatchPath` | Directory containing registered patch files. | `/app/patches` |

## Configuration Example

The service uses the common BaSyx `postgres` configuration section.

```yaml
postgres:
  host: db
  port: 5432
  user: admin
  password: admin123
  dbname: basyxTestDB
  maxOpenConnections: 50
  maxIdleConnections: 25
  connMaxLifetimeMinutes: 5
```

Environment variables can also be used in the same style as other BaSyx services, for example:

```bash
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DBNAME=basyxTestDB
POSTGRES_MAXOPENCONNECTIONS=50
POSTGRES_MAXIDLECONNECTIONS=25
POSTGRES_CONNMAXLIFETIMEMINUTES=5
```

## Patch Execution

Patches are registered by the service implementation. The current service registers `101.sql` with target database version `v1.0.1`.

A patch is executed only if the current value in `basyxsystem.database_version` is lower than the registered target version. The patch SQL file itself must update the database version after successfully applying its changes.

See the developer documentation for details about creating new patches.

