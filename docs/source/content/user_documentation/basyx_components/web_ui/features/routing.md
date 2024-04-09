# AAS Routing
>As AAS Web UI user
>I want to open the AAS Web UI with a specific AAS and Submodel/SubmodelElement as a starting point

The AAS Web UI provides a feature to directly route to a specific AAS, Submodel or SubmodelElement. This feature can be used to directly open the AAS Web UI with a specific AAS and Submodel/SubmodelElement as a starting point. This can be useful if you want to share a specific AAS or Submodel/SubmodelElement with other users.

# Feature Overview
There are two query parameters that can be used to route to a specific AAS, Submodel or SubmodelElement:

* **aas**: The URL of an Asset Administration Shell
* **path**: The URL to a specific Submodel or SubmodelElement
This feature allows for a few practical use cases:

    1. When reloading the page, the last opened Asset Administration Shell and the selected SubmodelElement will be opened again automatically.
    2. Opening a new Tab with both queries already set opens the GUI at the exact SubmodelElement which was given as filter over the URL.
    3. With the feature, it is possible to visualize and interact with shells which haven't been registered in a BaSyx-Registry. You can enter the endpoint for the AAS in the URL (e.g.: http://localhost:3000/?aas=endpoint-of-the-aas/aas)