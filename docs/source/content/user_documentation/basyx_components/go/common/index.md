# Common

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)

This section covers features and configuration that are shared across multiple BaSyx Go components, including Swagger/OpenAPI, common configuration, observability, pagination, validation, and other common API behavior.

## Contents

- [Deployment and Versions](deployment) — Covers version alignment, database initialization, persistent state, and deployment considerations shared across BaSyx Go components.
- [Swagger UI and OpenAPI](swagger) — Describes the Swagger UI and OpenAPI documents exposed by BaSyx Go components.
- [General Configuration](configuration) — Provides the common YAML configuration options and their environment-variable mappings.
- [Shared Runtime Features](shared_features) — Describes runtime functionality implemented in shared BaSyx Go code and identifies where those features are available.
- [Observability](observability) — Covers the common logging, metrics, tracing, and health-related capabilities provided by BaSyx Go components.
- [Pagination](pagination) — Describes paged API responses, pagination parameters, and continuation cursors.
- [Validation and Verification](validation) — Describes model validation, verification behavior, and the handling of invalid resources.
- [Repository-to-Registry Integration](registry_integration) — Describes how repositories can create, update, and remove corresponding descriptors in registries.
- [Asynchronous API Operations](asynchronous_requests) — Describes the API operations that BaSyx Go provides asynchronously and how their results are retrieved.
- [Response Representations](representations) — Explains the supported AAS response representations, including normal, `$value`, `$metadata`, `$reference`, and `$path`.
- [Recent Changes, History, and Signed Reads](history_and_changes) — Covers recent-change queries, historical states, integrity and mutation evidence, and cryptographically signed reads.

```{toctree}
:hidden:
:maxdepth: 1

deployment
swagger
configuration
shared_features
observability
pagination
validation
registry_integration
asynchronous_requests
representations
history_and_changes
```
