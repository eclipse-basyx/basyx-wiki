# AAS Routing

>As AAS Web UI user
>I want to open the AAS Web UI with a specific AAS and Submodel/SubmodelElement as a starting point

The AAS Web UI provides a feature to directly route to a specific AAS, Submodel or SubmodelElement. This feature can be used to directly open the AAS Web UI with a specific AAS and Submodel/SubmodelElement as a starting point. This can be useful if you want to share a specific AAS or Submodel/SubmodelElement with other users.

## Default Route

The main AAS Viewer is available under the `/aasviewer` route. Navigating to the root path (`/`) will redirect to the configured start page (by default, the AAS Viewer).

```{hint}
If you have bookmarks or links pointing to `/`, they will automatically redirect to the correct start page. No manual changes are required.
```

## Configurable Start Page

You can configure which page the Web UI shows when first opened by setting the `START_PAGE_ROUTE_NAME` environment variable. This is useful if your primary workflow centers on a different view, such as the AAS Editor.

For example, to make the AAS Editor the default landing page, set:

```
START_PAGE_ROUTE_NAME=AASEditor
```

The application validates the configured route at startup. If the route does not exist or its associated feature flag is disabled, the Web UI falls back to the default start page.

```{seealso}
For details on setting environment variables in Docker, see the [Docker Configuration](./docker_config.md) page. For a full list of available environment variables, see the [Configuration & Environment](./configuration.md) page.
```

## Deep Linking with Query Parameters

There are two query parameters that can be used to route to a specific AAS, Submodel or SubmodelElement:

* **aas**: The URL of an Asset Administration Shell
* **path**: The URL to a specific Submodel or SubmodelElement
This feature allows for a few practical use cases:

    1. When reloading the page, the last opened Asset Administration Shell and the selected SubmodelElement will be opened again automatically.
    2. Opening a new Tab with both queries already set opens the GUI at the exact SubmodelElement which was given as filter over the URL.
    3. With the feature, it is possible to visualize and interact with shells which haven't been registered in a BaSyx-Registry. You can enter the endpoint for the AAS in the URL (e.g.: `http://localhost:3000/aasviewer?aas=<endpoint-of-the-aas>/shells/<aas-id>`).
