# AAS Web UI

![Docker Pulls](https://img.shields.io/docker/pulls/eclipsebasyx/aas-gui)
![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-applications)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.0-yellow)
![API](https://img.shields.io/badge/API-v3.0-yellow)

The AAS Web UI is a vue.js 3 based web application that can be used to visualize and interact with Asset Administration Shells and their contents. It is designed to work with AAS V3 compliant registries and repositories as well as the AAS Discovery Service.

```{figure} ./images/aas_web_ui.png
---
width: 100%
alt: AAS Web UI
name: web_ui
---
```

## Features

* [Data Synchronization](./features/data_sync.md)
* [Docker Configuration](./features/docker_config.md)
* Dedicated components for different SubmodelElements:
  * SubmodelElementCollection
  * SubmodelElementList
  * Property
  * MultiLanguageProperty
  * Range
  * File
  * Blob
  * Operation
  * Entity
  * ReferenceElement
  * RelationshipElement
  * AnnotatedRelationshipElement
* [Role Based Access Control](./features/rbac.md)
* [Status Check and Error Notifications](./features/statuscheck.md)
* [Corporate Design](./features/corporate_design.md)
* [Mobile Support](./features/mobile_support.md)
* [Plugin Mechanism](./features/plugin_mechanism.md)
* [AAS Routing](./features/routing.md)
* [AAS Environment Integration](./features/aas_environment_integration.md)
* [Application Theme](./features/theme.md)

```{toctree}
:hidden:
:maxdepth: 1

features/data_sync
features/docker_config
features/rbac
features/statuscheck
features/corporate_design
features/mobile_support
features/plugin_mechanism
features/aas_environment_integration
features/routing
features/theme
```

## Download

```{note}
:class: margin
The AAS Web UI is now only compatible with the components of BaSyx V2 and the Asset Administration Shell V3.
```

The AAS Web UI can be downloaded from [Docker Hub](https://hub.docker.com/r/eclipsebasyx/aas-gui) as off-the-shelf component.
You can pull it by executing the following command:

```bash
docker pull eclipsebasyx/aas-gui
```

## Quick Start

```{hint}
:class: margin
Docker must be installed on your system to run the AAS Web UI.

Dockers official documentation provides a [detailed installation guide](https://docs.docker.com/get-docker/) for Windows, Mac and Linux.
```

The container for the AAS Web UI can be started by executing the following command:

```bash
docker run -p 3000:3000 --name=aas-web-ui eclipsebasyx/aas-gui
```

When the container is running, you can access the AAS Web UI by navigating to [http://localhost:3000](http://localhost:3000) in your browser.

There you will be able to connect to the Registries, Repositories and Discovery from the main menu.

```{figure} ./images/connect_to_basyx.png
---
width: 80%
alt: Connect to BaSyx Components
name: connect_basyx
---
```

## Introductory Example

```{seealso}
:class: margin
You can find a complete example on how to setup BaSyx in the [Quick Start](../../../introduction/quickstart) section.
```

You cant create a complete BaSyx example environment with Docker Compose. This includes the AAS Web UI, the BaSyx AAS and Submodel Registry, the AAS Environment (AAS Repository, Submodel Repository, Concept Description Repository) and the AAS Discovery Service.

This is a simple example of how to setup the AAS Web UI with Docker Compose in a `docker-compose.yml` file:

```yaml
services:
    aas-web-ui:
        image: eclipsebasyx/aas-gui
        container_name: aas-web-ui
        ports:
            - "3000:3000"
        environment:
            AAS_DISCOVERY_PATH: "<discovery_path>" (optional)
            AAS_REGISTRY_PATH: "<aas_registry_path>"
            SUBMODEL_REGISTRY_PATH: "<submodel_registry_path>"
            AAS_REPO_PATH: "<aas_repo_path>"
            SUBMODEL_REPO_PATH: "<submodel_repo_path>"
            CD_REPO_PATH: "<concept_description_repo_path>"
            DASHBOARD_SERVICE_PATH: "<dashboard_service_path>" (optional; Time Series Data)
            PRIMARY_COLOR: "<primary_color>" (optional; Corporate Design)
            PRIMARY_LIGHT_COLOR: "<primary_light_color>" (optional; Corporate Design light theme; ENV variable available starting with eclipsebasyx/aas-gui:v2-241114)
            PRIMARY_DARK_COLOR: "<primary_dark_color>" (optional; Corporate Design dark theme; ENV variable available starting with eclipsebasyx/aas-gui:v2-241114)
            LOGO_PATH: "<logo_path_in_container>" (optional; Corporate Design)
            LOGO_LIGHT_PATH: "<logo_light_path_in_container>" (optional; Corporate Design light theme; ENV variable available starting with eclipsebasyx/aas-gui:v2-241114)
            LOGO_DARK_PATH: "<logo_dark_path_in_container>" (optional; Corporate Design dark theme; ENV variable available starting with eclipsebasyx/aas-gui:v2-241114)
            BASE_PATH: "<base_path>" (optional)
            INFLUXDB_TOKEN: "<influxdb_token>" (optional; Time Series Data)
            KEYCLOAK_URL: "<keycloak_url>" (optional; RBAC feature)
            KEYCLOAK_REALM: "<keycloak_realm>" (optional; RBAC feature)
            KEYCLOAK_CLIENT_ID: "<keycloak_client_id>" (optional; RBAC feature)
            ENDPOINT_CONFIG_AVAILABLE: "<true/false>" (optional; ENV variable available starting with eclipsebasyx/aas-gui:v2-241114)
            SINGLE_AAS: "<true/>false>" (optional; ENV variable available starting with eclipsebasyx/aas-gui:v2-2412??)
            SINGLE_AAS_REDIRECT: "<URL>" (optional; ENV variable available starting with eclipsebasyx/aas-gui:v2-2412??)
        volumes:
            - <local_path_to_logo>:/usr/src/app/dist/Logo (optional; Corporate Design)
```

you can start the AAS Web UI with the following command:

```bash
docker-compose up -d
```

The AAS Web UI will be available at [http://localhost:3000](http://localhost:3000).

```{seealso}
The [Docker Configuration](./features/docker_config.md) page provides a detailed description of the configuration options for the AAS Web UI regarding the environment variables and the volumes.
```

## Interacting with AAS

```{figure} ./images/ui_sidebar.png
---
figclass: margin
alt: AAS List Sidebar
name: ui_sidebar
---
AAS List Sidebar
```

### AAS List Sidebar

The AAS List shows all Asset Administration Shells that are registered in the AAS Registry. The list can be filtered by entering a search term in the search bar.

There is also an option to show an information window for each Asset Administration Shell by clicking on the info icon. The information window shows the AAS ID, the AAS Name, the AAS Description and information regarding the asset like the global asset ID and a thumbnail.

In addition, the AAS can be removed by clicking on the **delete/close** icon. Clicking the **download** icon will download the AAS as an AASX file.

### AAS Treeview

```{figure} ./images/ui_treeview.png
---
figclass: margin
alt: AAS Treeview
name: ui_treeview
---
AAS Treeview
```

The AAS Treeview shows the Asset Administration Shell in a tree structure. The tree can be expanded by clicking on the expand icon on the left side of each Submodel/SubmodelElementCollection. Clicking directly on a Submodel/SubmodelElement will show the Submodel/SubmodelElement in the Element Details Page further to the right.

If a SubmodelElement is selected you are able to copy its path to the clipboard by clicking on the **copy** icon on the right side of the SubmodelElement.

### Element Details

```{figure} ./images/element_details.png
---
figclass: margin
alt: Element Details
name: element_details
---
Element Details
```

The Element Details Page shows the content of the selected SubmodelElement. This includes the following information:

* idShort
* modelType
* semanticId
* description
* value
* dataSpecificationContent (fetched from the Concept Description Repository)

The implemented SubmodelElements follow the specification for the AAS in Metamodel Version 3. Currently, the following SubmodelElements have their own visualization:

* SubmodelElementCollection
* SubmodelElementList
* Property
* MultiLanguageProperty
* File
* Blob
* Operation
* ReferenceElement
* Range
* Entity
* RelationshipElement
* AnnotatedRelationshipElement

```{note}
The Capability and Event SubmodelElements are not yet implemented in the AAS Web UI.
```

### Visualization Panel

The Visualization page shows the Submodel/SubmodelElement in a graphical representation. There are different criteria which enable a specific visualization for a Submodel/SubmodelElement.

1. The AAS Web UI checks for the presence of a SemanticId in the Submodel/SubmodelElement. If a SemanticId is present, the AAS Web UI will try to find a visualization for the SemanticId from the List of Submodel/SubmodelElement Plugins.

```{figure} ./images/ui_visualization.png
---
width: 60%
alt: Visualization Panel
name: ui_visualization
---
```

1. The File and Blob SubmodelElements have a special visualization. If the SubmodelElement contains an image, a PDF or a CAD file (.stl/.glTF/.obj), the AAS Web UI displays the file contents in the visualization page.

```{figure} ./images/image_preview.png
---
width: 80%
alt: Image Preview
name: image_preview
---
Image Preview in the Visualization Panel
```

```{figure} ./images/pdf_preview.png
---
width: 80%
alt: PDF Preview
name: pdf_preview
---
PDF Preview in the Visualization Panel
```

```{figure} ./images/cad_preview.png
---
width: 80%
alt: CAD Preview
name: cad_preview
---
CAD Preview in the Visualization Panel
```

## AAS Viewer

The AAS Viewer is a separate window that can be used to visualize the content of an Asset Administration Shell in a user friendly manner. It can be accessed via the main menu by clicking on the **AAS Viewer** button.
Like in the normal view, the AAS Viewer requires the selection of an AAS from the AAS List Sidebar.
After selecting an AAS, the user can navigate through a list of Submodels for the selected AAS.
In contrast to the normal view, the AAS Viewer does not show the SubmodelElements in a tree structure but only visualizes the top level Submodels.

The AAS Viewer shows the visualization of Submodels using the same criteria as the **Visualization Panel** in the normal view.
This means that primarily the SemanticId of the Submodel is used to find a suitable visualization using dedicated Submodel Plugins.
If no fitting Plugin is found, the AAS Viewer will try to display the Submodel in a generic way.

```{figure} ./images/aas_viewer.png
---
width: 100%
alt: AAS Viewer
name: aas_viewer
---
AAS Viewer Window
```

## Compatibility to BaSyx V1

If you still want to use the AAS Web UI with BaSyx V1, you can use an older version from Docker Hub.

```bash
docker pull eclipsebasyx/aas-gui:v230703
```

If you need to make changes to the AAS Web UI, you can also build the AAS Web UI from source. The source code for the AAS Web UI which is compatible with BaSyx V1 can be found here:

[GitHub AAS Web UI V1](https://github.com/eclipse-basyx/basyx-applications/tree/102e1c3cb7866c65d8c6e4f9211ba1c0db12f58d)

```{warning}
Please keep in mind that BaSyx V1 reached its end of life (eol) and is no longer supported.
```
