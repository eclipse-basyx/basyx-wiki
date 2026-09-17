# AASX File Server

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![API](https://img.shields.io/badge/API-v3.2-yellow)

The BaSyx Go AASX File Server stores and serves complete AASX package files. It keeps package metadata in PostgreSQL and the package bytes as PostgreSQL Large Objects, and exposes the standardized Package File Server API.

## Which Component Do I Need?

- The [AAS Repository](../aas_repository/index) stores and serves AAS resources through `/shells`; it is not a package-file store.
- The [Submodel Repository](../submodel_repository/index) stores and serves Submodel content through `/submodels`.
- The [AAS Environment](../aas_environment/index) imports model content and supplementary files from AASX through `/upload` and produces exports through `/serialization`.
- The AASX File Server manages complete packages through `/packages`. Uploading a package here does not import its AASs or Submodels into Repository APIs.

## Main Capabilities

- Upload and list AASX packages.
- Associate caller-supplied AAS identifiers with a package and filter the list by an AAS identifier.
- Download, replace, and delete a package by its package identifier.
- Enforce compressed-upload and expanded-package safety limits.
- Expose health, service-description, and runtime API-documentation endpoints.

## Important Behavior

Uploads use `multipart/form-data`. The service generates an opaque package identifier and returns its Base64URL form for later `/packages/{packageId}` requests. AAS identifiers supplied in the multipart request are metadata associations; the service normalizes them but does not infer them from the package contents.

Because package bytes are PostgreSQL Large Objects, database backup and migration procedures must include Large Objects. The BaSyx Configuration Service must initialize the database schema before startup.

## Configuration and Security

See [General Configuration](../common/configuration) for database, upload-limit, environment-variable, and reader-pool settings. The service supports the common OIDC and ABAC middleware; both are disabled in the local example. See [Runtime Security](../common/security).

## API Documentation

With the default empty context path, the running service exposes Swagger UI at `/swagger`, its OpenAPI document at `/api-docs/openapi.yaml`, and its self-description at `/description`.

These pages target the synchronous Package File Server API in BaSyx Go 1.0.11. The pinned [service source](https://github.com/eclipse-basyx/basyx-go-components/tree/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/cmd/aasxfileserverservice) and [OpenAPI document](https://github.com/eclipse-basyx/basyx-go-components/blob/81324eb3aad9d63baea93d3385bc9ca7e6a6a05a/cmd/aasxfileserverservice/openapi.yaml) are the reference. Use the Swagger UI of the running component for the exact contract of another installed release.

## Related Documentation

- [Setting Up the AASX File Server](setup)
- [Using the AASX File Server](usage)
- [AAS Environment](../aas_environment/index)
- [Runtime Security](../common/security)
- [Deployment and Persistence](../common/deployment)

```{toctree}
:hidden:
:maxdepth: 1

setup
usage
```
