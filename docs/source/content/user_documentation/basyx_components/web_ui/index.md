# AAS Web UI

![Docker Pulls](https://img.shields.io/docker/pulls/eclipsebasyx/aas-gui)
![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/eclipsebasyx/aas-gui)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/eclipse-basyx/basyx-applications)
![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/eclipse-basyx/basyx-applications)
![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-applications)

The AAS Web UI is a vue.js 3 based web application and can be used to visualize and interact with Asset Administration Shells. It is intended to work in conjunction with the BaSyx Registry and the BaSyx AAS Environment.

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
*  Dedicated components for different SubmodelElements:
      * SubmodelElementCollection
      * Property
      * MultiLanguageProperty
      * File
      * Operation
      * ReferenceElement
* [Status Check and Error Notifications](./features/statuscheck.md)
* [Corporate Design](./features/corporate_design.md)
* [Mobile Support](./features/mobile_support.md)
* [Plugin Mechanism](./features/plugin_mechanism.md)
* [AAS Routing](./features/routing.md)
* [AAS Server integration](./features/aas_server_integration.md)
* [Application Theme](./features/theme.md)
* [Register New Shells](./features/register_new_shells.md)


```{toctree}
:hidden:
:maxdepth: 1

features/data_sync
features/docker_config
features/statuscheck
features/corporate_design
features/mobile_support
features/plugin_mechanism
features/aas_server_integration
features/routing
features/theme
features/register_new_shells
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

There you will be able to connect to the BaSyx Registry and the AAS Environment (AAS Repository, Submodel Repository, Concept Description Repository) from the main menu.

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

You cant create a complete BaSyx example environment with Docker Compose. This includes the AAS Web UI, the BaSyx Registry and the AAS Environment (AAS Repository, Submodel Repository, Concept Description Repository).

This is a simple example of how to setup the AAS Web UI with Docker Compose in a `docker-compose.yml` file:

```yaml
version: "3.8"
services:
    aas-web-gui:
        image: eclipsebasyx/aas-gui
        container_name: aas-web-gui
        ports:
            - "3000:3000"
        environment:
            CHOKIDAR_USEPOLLING: "true"
            VITE_REGISTRY_PATH: "<registry_path>"
            VITE_AAS_REPO_PATH: "<aas_repo_path>"
            VITE_SUBMODEL_REPO_PATH: "<submodel_repo_path>"
            VITE_CD_REPO_PATH: "<concept_description_repo_path>"
            VITE_PRIMARY_COLOR: "<primary_color>"
            VITE_BASE_PATH: "<base_path>"
        volumes:
            - <local_path_to_logo>:/app/src/assets/Logo
            - <local_path_to_plugins>:/app/src/UserPlugins
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

The AAS List shows all Asset Administration Shells that are registered. The list can be filtered by entering a search term in the search bar.

There is also an option to show an information window for each Asset Administration Shell by clicking on the info icon. The information window shows the AAS ID, the AAS Name, the AAS Description and information regarding the asset like the global asset ID and a thumbnail.

In addition, the AAS can be removed from the registry by clicking on the **delete/close** icon. Clicking the **download** icon will download the AAS as an AASX file.

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

- idShort
- modelType
- semanticId
- description
- value
- dataSpecificationContent (fetched from the Concept Description Repository)

The implemented SubmodelElements follow the specification for the AAS in Metamodel Version 3. Currently, the following SubmodelElements have their own visualization:

- SubmodelElementCollection
- SubmodelElementList
- Property
- MultiLanguageProperty
- File
- Blob
- Operation
- ReferenceElement
- Range
- Entity
- RelationshipElement
- AnnotatedRelationshipElement

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

2. The File and Blob SubmodelElements have a special visualization. If the SubmodelElement contains an image or a PDF, the AAS Web UI displays the image/PDF in the visualization page.

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
