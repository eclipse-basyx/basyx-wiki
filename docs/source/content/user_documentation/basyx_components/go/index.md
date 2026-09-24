# BaSyx Go

BaSyx Go provides Go-based BaSyx backend components and shared libraries for running registries, repositories, and related infrastructure services.

- [GitHub Repository (basyx-go-components)](https://github.com/eclipse-basyx/basyx-go-components)
- [DockerHub (Eclipse BaSyx images)](https://hub.docker.com/u/eclipsebasyx)

Repositories store the AAS model content that clients read and change. Registries store descriptors that advertise where content can be reached, while Discovery stores mappings from asset identifiers to AAS identifiers. The following table provides an overview of the available BaSyx Go components and their roles, dependencies, and integrations. Using a Repository and Registry together does not by itself enable synchronization.

## Component Overview

| User goal | Component | Manages or stores | Required dependencies | Optional integration | Next page |
| --- | --- | --- | --- | --- | --- |
| Use AAS, Submodel, Concept Description, Registry, Discovery, upload, and serialization APIs in one runtime | AAS Environment | AAS, Submodel, and Concept Description content; AAS and Submodel descriptors; asset-identifier mappings | PostgreSQL initialized by the BaSyx Configuration Service | Repository-to-Registry synchronization is controlled by explicit flags and maintains descriptors in the same PostgreSQL database; Discovery functionality is included | [AAS Environment](aas_environment/index) |
| Store and modify AAS content | AAS Repository | AAS content and its references to Submodels | PostgreSQL initialized by the BaSyx Configuration Service | When AAS Registry integration is enabled, Repository changes also maintain AAS Descriptors in the Repository's PostgreSQL database. A separately deployed AAS Registry can expose them only when it uses the same database | [AAS Repository](aas_repository/index) |
| Store and modify Submodel content | Submodel Repository | Submodels and Submodel Elements | PostgreSQL initialized by the BaSyx Configuration Service | When Submodel Registry integration is enabled, Repository changes also maintain Submodel Descriptors in the Repository's PostgreSQL database. A separately deployed Submodel Registry can expose them only when it uses the same database | [Submodel Repository](submodel_repository/index) |
| Store and expose Concept Descriptions independently | Concept Description Repository | Concept Description content | PostgreSQL initialized by the BaSyx Configuration Service | The AAS Environment provides the same API area when a combined runtime is preferred | [Concept Description Repository](concept_description_repository/index) |
| Store, list, download, replace, and delete AASX packages | AASX File Server | Complete AASX package files and package metadata | PostgreSQL initialized by the BaSyx Configuration Service | Package AAS identifiers can be used for list filtering; package contents are not imported into Repositories | [AASX File Server](aasx_file_server/index) |
| Advertise where AAS content is available | AAS Registry | AAS Descriptors and AAS-scoped Submodel Descriptors, not Repository content | PostgreSQL initialized by the BaSyx Configuration Service | Can expose descriptors automatically maintained by an AAS Repository when both use the same PostgreSQL database. When Discovery integration is enabled, descriptor changes also maintain asset-to-AAS mappings in that database | [AAS Registry](aas_registry/index) |
| Advertise independently managed Submodels | Submodel Registry | Standalone Submodel Descriptors, not Submodel content | PostgreSQL initialized by the BaSyx Configuration Service | Can expose descriptors automatically maintained by a Submodel Repository when both use the same PostgreSQL database | [Submodel Registry](submodel_registry/index) |
| Find AAS identifiers from global or specific asset identifiers | Basic Discovery | Asset-identifier-to-AAS-identifier mappings, not descriptors or Repository content | PostgreSQL initialized by the BaSyx Configuration Service | Can expose mappings maintained by an AAS Registry or Digital Twin Registry when they use the same PostgreSQL database | [Basic Discovery](basic_discovery/index) |
| Use the Catena-X-oriented combined AAS Registry and Discovery API | Digital Twin Registry (DTR) | AAS Descriptors and asset-identifier mappings, not AAS content | PostgreSQL initialized by the BaSyx Configuration Service | Combines AAS Registry and Discovery functionality in one service. Separately deployed Repositories can maintain descriptors in the same database when their Registry integration is enabled | [Digital Twin Registry](digital_twin_registry/index) |
| Discover company-provided service endpoints | Company Lookup | Company Descriptors containing company identity and service endpoints | PostgreSQL initialized by the BaSyx Configuration Service | Describes external services; it does not automatically connect or synchronize them | [Company Lookup](company_lookup/index) |
| Initialize or migrate the shared BaSyx database | Configuration Service | Database schema, schema version, and schema state; it is a one-shot job | PostgreSQL | Must complete successfully before database-backed BaSyx runtimes start | [Configuration Service](configuration_service/index) |

For separate Repository and Registry processes, read [Repository-to-Registry Integration](common/registry_integration) before enabling synchronization. The integration writes descriptor tables in their shared database; merely starting both HTTP services does not connect them.

## Shared Guidance

- [Deployment and Versions](common/deployment) — Covers version alignment, database initialization, persistent state, and deployment considerations shared across BaSyx Go components.
- [Swagger UI and OpenAPI](common/swagger) — Describes the Swagger UI and OpenAPI documents exposed by BaSyx Go components.
- [General Configuration](common/configuration) — Provides the common YAML configuration options and their environment-variable mappings.
- [Shared Runtime Features](common/shared_features) — Describes runtime functionality implemented in shared BaSyx Go code and identifies where those features are available.
- [Observability](common/observability) — Covers the common logging, metrics, tracing, and health-related capabilities provided by BaSyx Go components.
- [Pagination](common/pagination) — Describes paged API responses, pagination parameters, and continuation cursors.
- [Validation and Verification](common/validation) — Describes model validation, verification behavior, and the handling of invalid resources.
- [Repository-to-Registry Integration](common/registry_integration) — Describes how repositories can create, update, and remove corresponding descriptors in registries.
- [Asynchronous API Operations](common/asynchronous_requests) — Describes the API operations that BaSyx Go provides asynchronously and how their results are retrieved.
- [Response Representations](common/representations) — Explains the supported AAS response representations, including normal, `$value`, `$metadata`, `$reference`, and `$path`.
- [Recent Changes, History, and Signed Reads](common/history_and_changes) — Covers recent-change queries, historical states, integrity and mutation evidence, and cryptographically signed reads.

```{toctree}
:hidden:
:maxdepth: 1

common/index
basic_discovery/index
aas_registry/index
submodel_registry/index
digital_twin_registry/index
aas_repository/index
submodel_repository/index
concept_description_repository/index
aasx_file_server/index
aas_environment/index
company_lookup/index
configuration_service/index
supply_chain_security
```
