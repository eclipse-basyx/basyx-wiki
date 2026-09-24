# Common

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)

This section documents features and configuration aspects that are implemented in shared BaSyx Go code and reused by multiple components (for example Swagger/OpenAPI exposure, common configuration handling, and shared runtime helpers).

## Contents
* [Deployment, Versions, and Persistent State](deployment) — choose matching application, source, schema, and toolchain versions; then preserve database state across container lifecycles.
* [Swagger UI Docs](swagger)
* [General Configuration](configuration) — look up the canonical YAML settings and environment-variable mappings.
* [Common / Shared Features](shared_features)
* [Observability](observability)
* [Pagination](pagination)
* [Identifiers and Encoding](encoding)
* [Validation](validation)
* [Repository-to-Registry Integration](registry_integration)
* [Asynchronous API Operations](asynchronous_requests)
* [Response Representations](representations)
* [History, Timestamps, and Signed Reads](history_and_changes)

```{toctree}
:hidden:
:maxdepth: 1

deployment
security
swagger
configuration
shared_features
observability
pagination
encoding
validation
registry_integration
asynchronous_requests
representations
history_and_changes
```
