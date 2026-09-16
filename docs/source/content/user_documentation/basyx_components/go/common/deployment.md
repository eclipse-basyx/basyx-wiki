# Deployment, Versions, and Persistent State

Use this page to keep BaSyx binaries, database initialization assets, and persistent PostgreSQL data aligned. Component setup pages contain runnable examples; this page defines the shared deployment contract behind them.

(version-scope)=
## Version Scope

The examples in this documentation use BaSyx Go application and image release **1.0.11**. A release number, source revision, toolchain version, database schema version, and API version are separate compatibility dimensions:

| Dimension | Value for these examples | What it controls | Source |
| --- | --- | --- | --- |
| Application and Docker image release | `1.0.11` | The BaSyx executable behavior and the version tag used for every BaSyx image sharing a database | [Release `v1.0.11`](https://github.com/eclipse-basyx/basyx-go-components/releases/tag/v1.0.11) |
| Git source | tag `v1.0.11`; commit `81324eb3aad9d63baea93d3385bc9ca7e6a6a05a` | The immutable source, configuration, SQL assets, and examples used for native builds | [Pinned commit](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a) |
| Go toolchain | `1.27.0` | The Go language and toolchain requirement declared by this source revision | [Pinned `go.mod`](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/go.mod) |
| Database schema | `v1.1.17` | The schema version that the 1.0.11 runtimes validate and the matching Configuration Service prepares | [Pinned schema check](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/internal/common/database.go) |

Do not substitute one dimension for another: schema `v1.1.17` is not an application release, and Go `1.27.0` is not an API version. API versions belong to individual component contracts; consult each component overview and its release-pinned OpenAPI definition rather than assuming one universal API or metamodel version.

Use the same BaSyx application release for the Configuration Service and all runtime images that share a database. For a native build, use the matching tag or immutable commit and its database assets. Mutable `latest` and `SNAPSHOT` tags can move independently and are not equivalent to this baseline.

## First Startup

A database-backed BaSyx deployment starts in this order:

1. Start PostgreSQL and wait until it is healthy.
2. Run the matching BaSyx Configuration Service and require successful completion.
3. Start the release-matched runtime services.

The Configuration Service is a one-shot job, so exit code `0` is the expected successful state. In Docker Compose, runtime services can express this ordering with `condition: service_completed_successfully`.

On an empty database, the Configuration Service creates the BaSyx base schema and applies its registered patches. That is **initialization**. Running it against a database that already contains BaSyx data can be an **upgrade** and requires the release-specific migration precautions described under [Existing Databases](#existing-databases). Startup ordering alone does not make an in-use database safe to migrate.

## Native Builds and Database Preparation

Check out the same release used by the Docker examples before building:

```bash
git clone https://github.com/eclipse-basyx/basyx-go-components.git
cd basyx-go-components
git checkout v1.0.11
git rev-parse HEAD
```

The final command must print `81324eb3aad9d63baea93d3385bc9ca7e6a6a05a`. Use Go `1.27.0`, as declared in that checkout's `go.mod`.

Run the Configuration Service from the repository root so its source-matched schema and patch paths are unambiguous:

```bash
go run ./cmd/basyxconfigurationservice/main.go -config ./cmd/basyxconfigurationservice/config.yaml -databaseSchema ./database/base.sql -customPatchPath ./database/patches
```

Wait for this command to complete successfully before starting a native HTTP service built from the same checkout. The `database/base.sql` file and the complete `database/patches` directory must come from that revision; copying only the executable is insufficient for database preparation.

The packaged Configuration Service container uses container paths `/app/base.sql` and `/app/patches`. Those defaults are paths **inside that image**. A native process resolves the host paths supplied on its command line, and a custom container layout must bind-mount its host assets and pass their corresponding container paths. See [Configuration Service usage](../configuration_service/usage) for the CLI options and [General Configuration](configuration) for database connection settings.

(persistent-state)=
## Persistent State

PostgreSQL retains BaSyx domain content, Registry descriptors, Discovery mappings, schema state, and enabled database-backed features such as active ABAC policies and history data. Container replacement preserves this state only when the replacement attaches the same database storage.

Docker may create an anonymous volume for an image-declared data directory when the Compose file does not specify storage. That volume can outlive its container, but it has no stable Compose identity and a later `docker compose up` after `down` does not automatically reuse it. Declare a named volume for predictable reuse and include that volume in backup and restore procedures.

| Action | Container effect | Volume effect | Next-start implication |
| --- | --- | --- | --- |
| `docker compose stop` then `start` | Stops and restarts the same containers | Existing named or anonymous attachments remain | The same database storage is reused |
| `docker compose down` then `up` | Removes and recreates service containers and networks | Volumes are not removed by default, but an anonymous volume is not automatically reattached | A declared named volume is reused; an undeclared anonymous volume can leave the recreated database appearing empty |
| `docker compose down -v` | Removes the service containers and networks | Removes named volumes declared by the Compose project and anonymous volumes attached to its containers; external volumes are not removed | The next start initializes new storage unless an external/restored volume is attached |
| Change an existing service from anonymous storage to a named volume | Recreates or reconfigures the database container | The new named volume has a different storage identity and starts empty unless data is explicitly migrated | Adding the declaration does **not** copy or migrate the old database |

The correct mount target depends on the PostgreSQL image major version. PostgreSQL 18 changed the image's declared volume to `/var/lib/postgresql`; PostgreSQL 17 and earlier use `/var/lib/postgresql/data`. For PostgreSQL 18:

```yaml
services:
  postgres:
    image: postgres:18
    volumes:
      - postgres_data:/var/lib/postgresql

volumes:
  postgres_data:
```

The existing PostgreSQL 16 Configuration Service example must instead use:

```yaml
services:
  postgres:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Do not attach an existing data directory to the other major version's mount path or treat changing the image tag as a PostgreSQL upgrade. Follow a supported PostgreSQL backup/restore or major-upgrade procedure. See the [official PostgreSQL image documentation](https://hub.docker.com/_/postgres) for the version-specific layout and the [Compose `down` reference](https://docs.docker.com/reference/cli/docker/compose/down/) for removal behavior.

```{warning}
Switching from anonymous storage to `postgres_data`, renaming a volume, or changing the mount target does not migrate existing database contents. Back up the original database and perform an explicit restore or supported migration before removing its container or volume.
```

## Existing Databases

Do not treat an existing database like an empty first-start database. Before changing BaSyx releases or applying a newer schema, use the canonical [upgrading an existing database](../configuration_service/operations.md#upgrading-an-existing-database) procedure. It covers migration prerequisites, backup scope, workload quiescence, success checks, and restore-based rollback.

Use [Configuration Service usage](../configuration_service/usage) for the initializer's flags and registered-patch behavior. Keep application release, Configuration Service, source SQL assets, and target schema aligned; this page intentionally does not duplicate the migration checklist.
