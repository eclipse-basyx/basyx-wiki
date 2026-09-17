# Basic Usage

The BaSyx Configuration Service is designed as a run-once startup job. It executes its registered initialization sequences and then exits.

## Command-Line Options

```{hint}
These command-line options are only relevant when the service is not run as part of a Docker container.
```

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

The `/app` defaults match the Configuration Service container image, which copies the release's `database/base.sql` and `database/patches` assets into that directory. They generally do not exist in an arbitrary host working directory.

For native execution, use the source and Go toolchain from the same application release as the runtime services. From the root of that BaSyx Go Components checkout, pass the repository's matching database assets explicitly:

```bash
go run ./cmd/basyxconfigurationservice/main.go \
  -config ./cmd/basyxconfigurationservice/config.yaml \
  -databaseSchema ./database/base.sql \
  -customPatchPath ./database/patches
```

If the binary and SQL assets are packaged elsewhere, replace these paths together; do not mix a Configuration Service binary with the patch directory from another release. See [Deployment, Versions, and Persistent State](../common/deployment.md) for the shared version contract.

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
  connMaxIdleTimeMinutes: 0
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
POSTGRES_CONNMAXIDLETIMEMINUTES=0
```

The Configuration Service owns its own pool while the job is running. Include it in the PostgreSQL connection budget during startup and upgrades. Runtime services create separate pools in their own processes or pods. See [General Configuration](../common/configuration) for zero-value semantics and pool sizing.

## Patch Execution

Patches are registered by the service implementation. Filenames encode their target schema version with underscores; for example, `1_0_1.sql` targets schema `v1.0.1`. The selected Configuration Service release determines which patches are registered. Its source and packaged patch directory are the authoritative inventory.

A patch is executed only if the current value in `basyxsystem.schema_version` is lower than the registered target version. Successful initialization and patching leaves `basyxsystem.state` as `clean`.

See the developer documentation for details about creating new patches.
