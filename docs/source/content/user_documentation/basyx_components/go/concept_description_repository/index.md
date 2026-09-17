# Concept Description Repository

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.2-yellow)
![API](https://img.shields.io/badge/API-v3.2-yellow)

The BaSyx Go Concept Description Repository stores and exposes Concept Descriptions independently through the standardized Concept Description Repository API. Concept Descriptions provide the semantic definitions referenced by AAS and Submodel content.

Use the combined [AAS Environment](../aas_environment/index) when one deployment should provide the AAS, Submodel, Concept Description, serialization, and import APIs. Use this standalone Repository when Concept Description storage and API access need an independent lifecycle, endpoint, or security boundary. The standalone service is not obsolete when an AAS Environment is also available.

## Main Capabilities

- Create, retrieve, replace, and delete Concept Descriptions.
- List Concept Descriptions with filters and [cursor-based pagination](../common/pagination).
- Query Concept Descriptions and inspect recent changes.
- Serialize selected Concept Descriptions through `/serialization`.
- Expose health, service-description, and runtime API-documentation endpoints.

## Important Behavior

The identifier in a resource URL is UTF-8 Base64URL-encoded without padding. Identifiers in JSON request bodies remain unencoded. A PUT creates a missing Concept Description or replaces an existing one; its body identifier must match the decoded path identifier.

This service stores Concept Descriptions only. It does not store AASs or Submodels and does not register endpoints in an AAS Registry. Applications remain responsible for using matching semantic identifiers in the resources that refer to a Concept Description.

The Repository uses PostgreSQL. The BaSyx Configuration Service must initialize the shared database schema before the Repository starts. See [Setup](setup).

## Configuration and Security

See [General Configuration](../common/configuration) for server, database, environment-variable, and reader-pool settings. The service supports the common OIDC and ABAC middleware; both are disabled in the local example. See [Runtime Security](../common/security) before exposing it.

## API Documentation

With the default empty context path, the running service exposes Swagger UI at `/swagger`, its OpenAPI document at `/api-docs/openapi.yaml`, and its self-description at `/description`. A configured `server.contextPath` prefixes all of these paths and the API routes.

The current [service source](https://github.com/eclipse-basyx/basyx-go-components/tree/main/cmd/conceptdescriptionrepositoryservice) and [OpenAPI document](https://github.com/eclipse-basyx/basyx-go-components/blob/main/cmd/conceptdescriptionrepositoryservice/openapi.yaml) are the reference for these pages. Use the running service's Swagger UI for the exact contract of the installed release.

## Related Documentation

- [Setting Up the Concept Description Repository](setup)
- [Using the Concept Description Repository](usage)
- [AAS Environment](../aas_environment/index)
- [Identifiers and Encoding](../common/encoding)
- [Runtime Security](../common/security)

```{toctree}
:hidden:
:maxdepth: 1

setup
usage
```
