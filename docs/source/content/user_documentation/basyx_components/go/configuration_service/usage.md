# Basic Usage

The BaSyx Configuration Service is designed as a run-once startup job. It executes its registered initialization sequences and then exits.

## Command-Line Options

The service binary supports these options for native and containerized execution. In Docker Compose or Kubernetes, pass them through the container command or arguments.

```bash
/app/basyxconfigurationservice \
  -databaseSchema /app/base.sql \
  -customPatchPath /app/patches
```

This example uses paths included in the official image. The image contains the default schema and registered patch files, but it does not contain `/app/config.yaml`. To use `-config`, provide the referenced file, for example by mounting it into the container. Schema and patch path overrides are normally needed only when custom files have been mounted or packaged.

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

Schema patches are explicitly registered by the Configuration Service. Each registered patch has a filename and target schema version. For example, `1_0_1.sql` targets schema version `v1.0.1`. `-customPatchPath` changes the directory used to resolve those registered filenames. It does not discover arbitrary additional SQL files, and a registered patch file that is required but missing from that directory causes migration to fail.

A patch is executed only if the current value in `basyxsystem.schema_version` is lower than the registered target version. After a required patch succeeds, the Configuration Service records its target version and `clean` state. A skipped patch does not modify the database state.

See the developer documentation for details about creating new patches.
