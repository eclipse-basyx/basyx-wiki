# Swagger UI and OpenAPI

BaSyx Go HTTP services can expose a Swagger UI and the corresponding OpenAPI specification. Set `swagger.enabled: false` to leave the UI and specification endpoints unregistered. The shared Swagger setup also omits its base-path redirect.

## Default Endpoints

The following endpoints are used by the shared Swagger UI setup:

- `.../swagger` for the Swagger UI
- `.../api-docs/openapi.yaml` for the OpenAPI document

If a component uses a `contextPath`, both endpoints are served below that base path (for example `/my-component/swagger`).

## Base Path Redirect

The shared Swagger setup also redirects the component base path to the Swagger UI:

- `/` -> `/swagger` (when no `contextPath` is configured)
- `/{contextPath}` -> `/{contextPath}/swagger`

The standalone DPP API additionally registers this redirect outside the shared Swagger setup. With Swagger disabled, its base path still redirects to the unregistered Swagger URL, which then returns `404 Not Found`.

## Runtime OpenAPI Adjustments

The shared Swagger setup can inject runtime values into the served OpenAPI document:

- `servers` URL based on `server.host`, `server.port`, and `server.contextPath`
- `info.contact` based on `swagger.contactName`, `swagger.contactEmail`, and `swagger.contactUrl`
- shared `/verify`, ABAC/ReBAC management, and Event Feed paths when the corresponding feature is enabled and supported by the service

When `server.host` is `0.0.0.0`, the generated Swagger/OpenAPI server URL is rendered with `localhost` for display.

When serving the OpenAPI document, BaSyx replaces external references to the AAS Part 1 and Part 2 schemas with references to versioned copies served locally under `/api-docs`. The served document can therefore differ from the OpenAPI YAML packaged in the image.
