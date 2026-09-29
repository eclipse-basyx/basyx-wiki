# Concept Description Repository

![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-go-components)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.2-yellow)
![API](https://img.shields.io/badge/API-v3.2-yellow)

The BaSyx Go Concept Description Repository stores and exposes Concept Descriptions independently through the standardized Concept Description Repository API. Concept Descriptions provide the semantic definitions referenced by AAS and Submodel content.

Use the [AAS Environment](../aas_environment/index) when AASs, Submodels, Concept Descriptions, serialization, and import should be provided by one deployment. Use the standalone Concept Description Repository when Concept Description storage needs its own endpoint, lifecycle, or security boundary.

## Main Capabilities

- Create, retrieve, replace, and delete Concept Descriptions.
- List Concept Descriptions with filters and [cursor-based pagination](../common/pagination).
- Query Concept Descriptions with structured conditions and inspect recent changes.
- Expose health, service-description, and runtime API-documentation endpoints.

## Important Behavior

The identifier in a resource URL is UTF-8 Base64URL-encoded without padding. Identifiers in JSON request bodies remain unencoded. A PUT creates a missing Concept Description or replaces an existing one; its body identifier must match the decoded path identifier.

The Repository stores Concept Descriptions independently of the AAS and Submodel resources that reference them. It does not validate or synchronize semantic references in those resources.

Creating, replacing, or deleting a Concept Description does not modify AASs or Submodels that reference its identifier. Deleting a Concept Description can therefore leave existing semantic references pointing to an identifier that is no longer available from this Repository.

The Repository uses PostgreSQL. The BaSyx Configuration Service must initialize the shared database schema before the Repository starts. See [Setup](setup).

## Configuration and Security

See [General Configuration](../common/configuration) for server, database, environment-variable, reader-pool, OIDC, and ABAC settings. Authentication and authorization are disabled in the local example.

## API Documentation

With the default empty context path, the service exposes Swagger UI at `/swagger`, its OpenAPI document at `/api-docs/openapi.yaml`, and its self-description at `/description`. A configured `server.contextPath` prefixes these paths and the API routes. Use the availability note below when comparing the bundled OpenAPI document with the standalone runtime.

### Availability Notes

The standalone Concept Description Repository does not provide `/serialization` or `/upload`. Use the [AAS Environment](../aas_environment/index) when serialization or environment import is required.

## Related Documentation

- [Setting Up the Concept Description Repository](setup)
- [Using the Concept Description Repository](usage)
- [AAS Environment](../aas_environment/index)
- [General Configuration](../common/configuration)

```{toctree}
:hidden:
:maxdepth: 1

setup
usage
```
