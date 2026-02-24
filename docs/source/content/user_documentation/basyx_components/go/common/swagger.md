# Swagger UI Docs

All BaSyx Go components can expose a Swagger UI and the corresponding OpenAPI specification via shared infrastructure in `internal/common`.

## Default Endpoints

The following endpoints are used by the shared Swagger UI setup:

- `.../swagger` for the Swagger UI
- `.../api-docs/openapi.yaml` for the OpenAPI document

If a component uses a `contextPath`, both endpoints are served below that base path (for example `/my-component/swagger`).

## Base Path Redirect

The shared Swagger setup also redirects the component base path to the Swagger UI:

- `/` -> `/swagger` (when no `contextPath` is configured)
- `/{contextPath}` -> `/{contextPath}/swagger`

## Runtime OpenAPI Adjustments

The shared Swagger setup can inject runtime values into the served OpenAPI document:

- `servers` URL based on `server.host`, `server.port`, and `server.contextPath`
- `info.contact` based on `swagger.contactName`, `swagger.contactEmail`, and `swagger.contactUrl`

When `server.host` is `0.0.0.0`, the generated Swagger/OpenAPI server URL is rendered with `localhost` for display.
