# Repository-to-Registry Integration

Enable Registry integration when descriptors should follow Repository content automatically. Clients can then discover the Repository resources through a Registry without your application maintaining a separate descriptor for each supported change.

## Shared Database and Transactions

Synchronization writes Registry tables in the Repository's PostgreSQL database. Configure the corresponding Registry service against that same database to expose the descriptors. Initialize the database using the [Configuration Service](../configuration_service/index) as described in the component setup.

The Repository does not POST descriptors to a remote Registry URL. The Registry HTTP service need not be running for synchronization to write its tables. Repository changes and required descriptor writes use the same transaction; a required descriptor-write failure rolls back the synchronized operation.

## Choose the Integration Flag

| Service | Supported configuration | Effect |
| --- | --- | --- |
| Standalone AAS Repository | `general.aasRegistryIntegration: true` | Maintains AAS Descriptors and applicable embedded Submodel Descriptors. It does not create standalone Submodel Registry entries under this flag. |
| Standalone Submodel Repository | `general.submodelRegistryIntegration: true` | Maintains standalone Submodel Descriptors and applicable embedded descriptors in existing AAS Descriptors. |
| Composed AAS Environment | AAS and/or Submodel integration flags | Enables the corresponding integration within the composed service. |

Integration is disabled by default. The standalone AAS Repository rejects the Submodel flag; the standalone Submodel Repository rejects the AAS flag. Follow the component guide for the exact lifecycle effects.

## Advertise a Reachable Repository URL

`general.externalUrl` is the client-facing **Repository** base URL. When integration is enabled, supply at least one absolute HTTP(S) URL with scheme and host. Include any public context path; omit query strings and fragments. Comma-separated base URLs generate multiple endpoints.

For example, merge this into an AAS Repository configuration:

```yaml
server:
  port: 8084
general:
  aasRegistryIntegration: true
  externalUrl: "http://localhost:8084"
```

Creating `urn:example:aas:1` then advertises an endpoint such as `http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE`. Use `localhost` only when clients reach the Repository on their own machine. Behind a reverse proxy, advertise the public URL and path.

Generated Submodel endpoints append `/submodels/{id}` to the same base URL. A standalone AAS Repository does not serve that root route. When synchronizing embedded Submodel Descriptors, provide public routing to a Submodel Repository sharing the database, as in the combined example below, or use the [AAS Environment setup](../aas_environment/setup).

## Existing Resources and Manual Changes

Integration is driven by mutations; enabling it does not backfill all existing resources at startup. Full-resource PUT synchronization compares the descriptors derived from the old and new resource. An unchanged replacement, or a change only to content outside the descriptor, can skip the Registry write. A no-change PUT is therefore not a guaranteed repair action.

Plan explicit registration or reconciliation for existing data. Generated updates can replace manually maintained descriptor fields, so maintain synchronized information in the Repository resource.

## Combined Compose Example

This local example runs both Repositories and both Registries against one database. A reverse proxy exposes both Repository APIs at `http://localhost:8080`, which both Repositories advertise in generated descriptors. The direct Repository ports remain available for the usage walkthroughs.

Save this as `docker-compose.yml` in a new directory and run it.

```yaml
x-database: &database
  POSTGRES_HOST: postgres
  POSTGRES_PORT: "5432"
  POSTGRES_USER: admin
  POSTGRES_PASSWORD: admin123
  POSTGRES_DBNAME: basyxTestDB

x-basyx: &basyx
  pull_policy: always
  depends_on:
    basyx_configuration:
      condition: service_completed_successfully

services:
  postgres:
    image: postgres:18
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DB: basyxTestDB
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d basyxTestDB"]
      interval: 10s
      timeout: 5s
      retries: 5

  basyx_configuration:
    image: eclipsebasyx/basyxconfigurationservice-go:latest
    pull_policy: always
    environment: *database
    depends_on:
      postgres:
        condition: service_healthy

  aas_repository:
    <<: *basyx
    image: eclipsebasyx/aasrepository-go:latest
    environment:
      <<: *database
      SERVER_PORT: "8084"
      GENERAL_AASREGISTRYINTEGRATION: "true"
      GENERAL_EXTERNALURL: http://localhost:8080
    ports:
      - "8084:8084"

  submodel_repository:
    <<: *basyx
    image: eclipsebasyx/submodelrepository-go:latest
    environment:
      <<: *database
      SERVER_PORT: "8085"
      GENERAL_SUBMODELREGISTRYINTEGRATION: "true"
      GENERAL_EXTERNALURL: http://localhost:8080
    ports:
      - "8085:8085"

  aas_registry:
    <<: *basyx
    image: eclipsebasyx/aasregistry-go:latest
    environment:
      <<: *database
      SERVER_PORT: "8082"
    ports:
      - "8082:8082"

  submodel_registry:
    <<: *basyx
    image: eclipsebasyx/submodelregistry-go:latest
    environment:
      <<: *database
      SERVER_PORT: "8083"
    ports:
      - "8083:8083"

  repository_proxy:
    image: nginx:stable-alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - aas_repository
      - submodel_repository
```

The YAML anchors reuse the database connection and startup dependency. No fixed container names are needed. Save the following as `nginx.conf` alongside the Compose file:

```nginx
server {
    listen 80;
    client_max_body_size 0;

    location /shells {
        proxy_pass http://aas_repository:8084;
        proxy_set_header Host $http_host;
    }

    location /submodels {
        proxy_pass http://submodel_repository:8085;
        proxy_set_header Host $http_host;
    }
}
```

The proxy preserves the request path. It routes the generated resource URLs; use the direct service ports for Swagger, health, query, and Registry APIs. Upload size limits remain enforced by the Repositories. This example uses an empty context path and unsecured services for local use. Replace `localhost` in the advertised URL when clients run elsewhere.

Start and check the services:

```bash
docker compose up -d
curl -i http://localhost:8084/health
curl -i http://localhost:8085/health
curl -i http://localhost:8082/health
curl -i http://localhost:8083/health
```

Expect the Configuration Service to exit with code `0`, and each health request to return `200 OK` with `{"status":"UP"}` once startup finishes. For startup failures, inspect `docker compose logs basyx_configuration aas_repository submodel_repository aas_registry submodel_registry`.

First, save the following as
`integration-aas.json`:

```json
{
  "modelType": "AssetAdministrationShell",
  "id": "urn:example:aas:1",
  "idShort": "RegistryIntegrationAAS",
  "assetInformation": {
    "assetKind": "Instance",
    "globalAssetId": "urn:example:asset:1",
    "assetType": "Motor",
    "specificAssetIds": [
      { "name": "serialNumber", "value": "SN-001" }
    ]
  }
}
```

Create it through the AAS Repository:

```bash
curl -i -X POST http://localhost:8084/shells -H 'Content-Type: application/json' --data-binary '@integration-aas.json'
```

Expect `201 Created`. Save this AAS-scoped Submodel as
`integration-embedded-submodel.json`:

```json
{
  "modelType": "Submodel",
  "id": "urn:example:submodel:1",
  "idShort": "EmbeddedNameplate",
  "submodelElements": [
    {
      "modelType": "Property",
      "idShort": "SerialNumber",
      "valueType": "xs:string",
      "value": "SN-001"
    }
  ]
}
```

Store it through the AAS-scoped API. This also adds its reference to the AAS:

```bash
curl -i -X PUT http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ -H 'Content-Type: application/json' --data-binary '@integration-embedded-submodel.json'
```

Expect `201 Created` for unused identifiers. Now read the generated AAS
Descriptor and follow its advertised AAS and embedded Submodel endpoints
through the proxy:

```bash
curl -i http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE
curl -i http://localhost:8080/shells/dXJuOmV4YW1wbGU6YWFzOjE
curl -i http://localhost:8080/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
```

Expect `200 OK` for all three requests. Confirm that the descriptor's AAS and embedded Submodel endpoint URLs match the two proxy URLs above. This verifies that discovery leads to readable content. Creating the Submodel through the AAS Repository maintains its embedded descriptor; it does not create a standalone Submodel Registry entry under the AAS integration flag.

To verify the standalone Submodel integration independently, save the following
as `integration-standalone-submodel.json`. It deliberately uses a different
identifier from the embedded example:

```json
{
  "modelType": "Submodel",
  "id": "urn:example:submodel:standalone:1",
  "idShort": "StandaloneNameplate",
  "semanticId": {
    "type": "ExternalReference",
    "keys": [
      { "type": "GlobalReference", "value": "urn:example:semantic:nameplate" }
    ]
  },
  "submodelElements": [
    {
      "modelType": "Property",
      "idShort": "ManufacturerName",
      "valueType": "xs:string",
      "value": "Example Motors"
    }
  ]
}
```

Create the Submodel through the standalone Submodel Repository, retrieve its
generated standalone descriptor, and follow its advertised endpoint:

```bash
curl -i -X POST http://localhost:8085/submodels -H 'Content-Type: application/json' --data-binary '@integration-standalone-submodel.json'
curl -i http://localhost:8083/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6c3RhbmRhbG9uZTox
curl -i http://localhost:8080/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6c3RhbmRhbG9uZTox
```

Expect `201 Created` for the POST and `200 OK` for both GET requests. The
descriptor's endpoint URL must match the proxy URL above. This confirms that
`submodelRegistryIntegration` created a standalone Submodel Descriptor and
that clients can follow it to the stored Submodel.

Remove the example resources and verify that synchronization also removes the
descriptors:

```bash
curl -i -X DELETE http://localhost:8085/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6c3RhbmRhbG9uZTox
curl -i http://localhost:8083/submodel-descriptors/dXJuOmV4YW1wbGU6c3VibW9kZWw6c3RhbmRhbG9uZTox
curl -i -X DELETE http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE/submodels/dXJuOmV4YW1wbGU6c3VibW9kZWw6MQ
curl -i http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE
curl -i -X DELETE http://localhost:8084/shells/dXJuOmV4YW1wbGU6YWFzOjE
curl -i http://localhost:8082/shell-descriptors/dXJuOmV4YW1wbGU6YWFzOjE
```

Each DELETE returns `204 No Content`. The standalone descriptor GET returns
`404 Not Found`. After the AAS-scoped Submodel deletion, the AAS Descriptor
still returns `200 OK` but no longer contains that embedded Submodel
Descriptor. After deleting the AAS, its descriptor GET returns `404 Not
Found`.
