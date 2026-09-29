# AASX File Server

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![API](https://img.shields.io/badge/API-v3.2-yellow)

The BaSyx Go AASX File Server stores and serves complete AASX packages through the standardized AASX File Server API. It manages package files and their metadata without importing the contained AASs and Submodels into Repository APIs.

## Which Component Do I Need?

- The [AAS Repository](../aas_repository/index) stores and serves AAS resources through `/shells`; it is not a package-file store.
- The [Submodel Repository](../submodel_repository/index) stores and serves Submodel content through `/submodels`.
- The [AAS Environment](../aas_environment/index) imports model content and supplementary files from AASX through `/upload` and produces exports through `/serialization`.
- The AASX File Server manages complete packages through `/packages`. Uploading a package here does not import its AASs or Submodels into Repository APIs.

## Main Capabilities

- Upload and list AASX packages synchronously.
- Submit asynchronous package uploads and retrieve their status and result.
- Associate caller-supplied AAS identifiers with a package and filter the list by an AAS identifier.
- Download, replace, and delete a package by its package identifier.
- Enforce uploaded-file size and expanded-package safety limits.
- Expose health, service-description, and runtime API-documentation endpoints.

## Important Behavior

Uploads use `multipart/form-data`. The service generates an opaque package identifier and returns its Base64URL form for later `/packages/{packageId}` requests. AAS identifiers associated with a package are caller-supplied metadata; the File Server does not infer them from the package contents. See [Using the AASX File Server](usage) for multipart input and identifier representation.

Package metadata is stored in PostgreSQL and package bytes are stored as PostgreSQL Large Objects. Database backup and migration procedures must therefore include Large Objects. The BaSyx Configuration Service must initialize the database schema before startup.

`GET /description` reports the profiles enabled by the running service. SSP-001 identifies the synchronous package API. SSP-002 is present only when asynchronous upload processing is available. In that case the service exposes `POST /packages-async`, `GET /packages-async/status/{handleId}`, and `GET /packages-async/result/{handleId}`.

## Configuration and Security

See [General Configuration](../common/configuration) for database, upload-limit, environment-variable, and reader-pool settings. The service supports OIDC authentication, ABAC authorization, and experimental [relationship-based access control (ReBAC)](../common/rebac). These controls are disabled in the local example. See the [`oidc` and `abac`](../common/configuration.md#oidc-and-abac) and [Security Files](../common/configuration.md#security-files) sections for the shared security configuration.

## API Documentation

With the default empty context path, the running service exposes Swagger UI at `/swagger`, its OpenAPI document at `/api-docs/openapi.yaml`, and its self-description at `/description`. Use `/description` to determine whether the running instance provides SSP-001 only or both SSP-001 and SSP-002.

## Related Documentation

- [Setting Up the AASX File Server](setup)
- [Using the AASX File Server](usage)
- [AAS Environment](../aas_environment/index)
- [Asynchronous API Operations](../common/asynchronous_requests)
- [Relationship-Based Access Control (ReBAC)](../common/rebac)
- [Deployment and Persistence](../common/deployment)

```{toctree}
:hidden:
:maxdepth: 1

setup
usage
```
