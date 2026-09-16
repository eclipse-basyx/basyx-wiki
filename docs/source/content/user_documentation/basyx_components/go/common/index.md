# Common

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)

This section documents features and configuration aspects that are implemented in shared BaSyx Go code and reused by multiple components (for example Swagger/OpenAPI exposure, common configuration handling, and shared runtime helpers).

## Contents
* [Deployment, Versions, and Persistent State](deployment) — choose matching application, source, schema, and toolchain versions; then preserve database state across container lifecycles.
* [Runtime Security](security) — follow the OIDC and ABAC workflow, policy lifecycle, and security troubleshooting path.
* [General Configuration](configuration) — look up the canonical YAML settings and environment-variable mappings.
* [Swagger UI Docs](swagger)
* [Common / Shared Features](shared_features)
* [Observability](observability)
* [Pagination](pagination)
* [Identifiers and Encoding](encoding)
* [Validation](validation)
* [Repository-to-Registry Integration](registry_integration)
* [Asynchronous Requests](asynchronous_requests)
* [Response Representations](representations)
* [History, Timestamps, and Signed Reads](history_and_changes)
* [Understanding API Errors](api_errors)

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
api_errors
```
