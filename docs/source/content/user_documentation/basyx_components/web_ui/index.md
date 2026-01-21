# AAS Web UI

![Docker Pulls](https://img.shields.io/docker/pulls/eclipsebasyx/aas-gui)
![GitHub](https://img.shields.io/github/license/eclipse-basyx/basyx-applications)
![Metamodel](https://img.shields.io/badge/Metamodel-v3.0-yellow)
![API](https://img.shields.io/badge/API-v3.0-yellow)

The Eclipse **BaSyx AAS Web UI** is a Vue.js 3 based web application that can be used to visualize and interact with Asset Administration Shells and their contents. It is designed to work with AAS V3 compliant registries and repositories as well as the AAS Discovery Service.

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
The AAS Web UI is compatible with the Asset Administration Shell `V3.X.X`.
```

The AAS Web UI can be downloaded from [Docker Hub](https://hub.docker.com/r/eclipsebasyx/aas-gui) as off-the-shelf component.
You can pull it by running the following command:

```bash
docker pull eclipsebasyx/aas-gui
```

## Quick Start

```{hint}
Docker must be installed on your system to run the AAS Web UI.

Dockers official documentation provides a [detailed installation guide](https://docs.docker.com/get-docker/) for Windows, Mac and Linux.
```

The container for the AAS Web UI can be started by executing the following command:

```bash
docker run -p 3000:3000 --name=aas-web-ui eclipsebasyx/aas-gui
```

When the container is running, you can access the AAS Web UI by navigating to [http://localhost:3000](http://localhost:3000) in your browser.

To connect to an AAS infrastructure, open the settings by clicking on the gear icon in the top right corner of the web ui. From there, you can create a new connection by providing the endpoints for the AAS Registry, Submodel Registry, AAS Repository, Submodel Repository and Concept Description Repository as well as the optional endpoint for the AAS Discovery Service.

```{seealso}
For more details on how to connect to an AAS infrastructure, please refer to the [Configuration & Environment](./features/configuration.md) page.
```

```{figure} ./images/connect_to_aas_infrastructure.png
---
width: 80%
alt: Connect to AAS Infrastructure
name: connect_to_aas_infrastructure
---
```

```{seealso}
You can find a complete example on how to setup BaSyx in the [Quick Start](../../../introduction/quickstart) section.

To find setups for dedicated use cases, please refer to the [UI examples on GitHub](https://github.com/eclipse-basyx/basyx-aas-web-ui/tree/main/examples).
```

## Interacting with AAS

After connecting to an AAS infrastructure, you can start interacting with the Asset Administration Shells that are available in the connected AAS infrastructure.

### AAS List Navigation Drawer

```{figure} ./images/aas_list.png
---
width: 40%
alt: AAS List Sidebar
name: aas_list
---
AAS List Sidebar
```

The **AAS List** shows all Asset Administration Shells that are registered in the AAS Registry. If no registries are used, the AAS List will directly visualize shells coming from the configured AAS Repository. The list can be filtered by entering a search term in the search bar. THis could either be the `idShort` or the `displayName` of the AAS.

Selecting an AAS from the list will open a details pane below to show more information about the selected AAS, such as the `globalAsset`, `AdministrativeInformation` and a QR code representing the assets unique identifier.

From the AAS List, users can **download** and **delete** Asset Administration Shells by clicking on the respective icons on the right side of each AAS entry. When switching to the `AAS Editor` via the main menu, users can also **create** new Asset Administration Shells by clicking on the three dot icon in the top right corner of the AAS List and selecting `Create AAS` from the context menu. They can also **edit** existing AAS by clicking on `Edit AAS` in the context menu of each individual AAS entry.

### AAS Treeview

```{figure} ./images/aas_treeview.png
---
width: 50%
alt: AAS Treeview
name: aas_treeview
---
AAS Treeview
```

The AAS Treeview shows the Submodels from the selected AAS in a tree structure. The tree can be expanded by clicking on the expand icon on the left side of each Submodel/SubmodelElementCollection. Clicking directly on a Submodel/SubmodelElement will show the Submodel/SubmodelElement in the Element Details Page further to the right.

If a SubmodelElement is selected you are able to copy its path to the clipboard by clicking on the **copy** icon on the right side of the SubmodelElement. IF you are in the `AAS Editor`, you can also **add**, **edit** and **delete** Submodels and SubmodelElements by clicking on the three dot icon on the right side of each Submodel/SubmodelElement and selecting the respective action from the context menu.

The AAS Treeview also contains a search bar that can be used to filter Submodels and SubmodelElements by their `idShort` or `displayName`.

```{hint}
Using the `+` and `-` buttons next to the search bar, you can expand or collapse all nodes in the tree.
```

### Element Details

```{figure} ./images/element_details.png
---
width: 60%
alt: Element Details
name: element_details
---
Element Details
```

The Element Details tab shows the content of the selected SubmodelElement. This includes the following information:

* `idShort` - The short id of the SubmodelElement
* `displayName` - The display name of the SubmodelElement
* `modelType` - The type of the SubmodelElement (e.g. Property, File, Blob, etc.)
* `semanticId` - The semantic id of the SubmodelElement
* `qualifiers` - The qualifiers of the SubmodelElement
* `description` - The description of the SubmodelElement
* `value` - The value of the SubmodelElement (if applicable)
* `ConceptDescription` - ConceptDescription separately fetched from the Concept Description Repository (if applicable)

The implemented SubmodelElements follow the specification for the AAS in Metamodel Version 3. Currently, the following SubmodelElements have their own visualization:

* `SubmodelElementCollection`
* `SubmodelElementList`
* `Property`
* `MultiLanguageProperty`
* `File`
* `Blob`
* `Operation`
* `ReferenceElement`
* `Range`
* `Entity`
* `RelationshipElement`
* `AnnotatedRelationshipElement`

```{note}
The `Capability` and `BasicEvent` SubmodelElements are not yet implemented in the AAS Web UI.
```

### Visualization Panel

The Visualization tab shows the Submodel/SubmodelElement in a graphical representation. There are different criteria which enable a specific visualization for a Submodel/SubmodelElement.

1. The AAS Web UI checks for the presence of a SemanticId in the Submodel/SubmodelElement. If a SemanticId is present, the AAS Web UI will try to find a visualization for the SemanticId from the List of Submodel/SubmodelElement Plugins.

  ```{figure} ./images/ui_visualization.png
  ---
  width: 60%
  alt: Visualization Panel
  name: ui_visualization
  ---
  ```

2. The File and Blob SubmodelElements have a special visualization. If the SubmodelElement contains an image, a PDF or a CAD file (.stl/.glTF/.obj), the AAS Web UI displays the file contents in the visualization tab.

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

## AAS Submodel Viewer

The AAS Submodel Viewer is a separate page that can be used to visualize the content of an Asset Administration Shell in a user friendly manner. It can be accessed via the main menu by clicking on the **AAS Submodel Viewer** button.
Like in the normal view, the AAS Submodel Viewer requires the selection of an AAS from the AAS List Sidebar.
After selecting an AAS, the user can navigate through a list of Submodels for the selected AAS.
In contrast to the normal view, the AAS Submodel Viewer does not show the SubmodelElements in a tree structure but only visualizes the top level Submodels.

The AAS Submodel Viewer shows the visualization of Submodels using the same criteria as the **Visualization Panel** in the normal view.
This means that primarily the SemanticId of the Submodel is used to find a suitable visualization using dedicated Submodel Plugins.
If no fitting Plugin is found, the AAS Submodel Viewer will try to display the Submodel in a generic way.

```{figure} ./images/aas_submodel_viewer.png
---
width: 100%
alt: AAS Submodel Viewer
name: aas_submodel_viewer
---
AAS Submodel Viewer Page
```

## Submodel Viewer & Editor

## Extension Modules

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
