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

* [Configuration & Environment](./features/configuration.md)
* [Data Synchronization](./features/data_sync.md)
* [Docker Configuration](./features/docker_config.md)
* [Role Based Access Control](./features/rbac.md)
* [Corporate Design](./features/corporate_design.md)
* [Mobile Support](./features/mobile_support.md)
* [Plugin Mechanism](./features/plugin_mechanism.md)
* [AAS Editor](./features/aas_editor.md)
* [AAS Routing](./features/routing.md)
* [Application Theme](./features/theme.md)

```{toctree}
:hidden:
:maxdepth: 1

features/configuration
features/data_sync
features/docker_config
features/rbac
features/corporate_design
features/mobile_support
features/plugin_mechanism
features/aas_editor
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

To connect to an AAS infrastructure, open the settings by clicking on the gear icon in the top right corner of the Web UI. From there, you can create a new connection by providing the endpoints for the AAS Registry, Submodel Registry, AAS Repository, Submodel Repository and Concept Description Repository, as well as the optional endpoint for the AAS Discovery Service.

```{seealso}
For more details on configuration options, backend connections, and advanced setup, please refer to the [Configuration & Environment](./features/configuration.md) page.
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

The **AAS List** displays all Asset Administration Shells that are registered in the connected AAS Registry. If no registries are configured, the AAS List will directly visualize shells coming from the configured AAS Repository.

You can filter the list by entering a search term in the search bar, which searches through the `idShort` or `displayName` properties of the AAS.

**Viewing AAS Details:**
Selecting an AAS from the list opens a details pane below, showing additional information such as:

* Global Asset ID
* Administrative Information
* A QR code representing the asset's unique identifier

**AAS Management:**
From the AAS List, you can:

* **Download** and **delete** Asset Administration Shells by clicking on the respective icons on the right side of each AAS entry
* **Create** new Asset Administration Shells when in the AAS Editor view (accessible via the main menu) by clicking the three-dot icon in the top right corner of the AAS List and selecting `Create AAS`
* **Edit** existing AAS when in the AAS Editor view by clicking on `Edit AAS` in the context menu of each individual AAS entry

```{seealso}
For detailed information on creating and editing Asset Administration Shells, see the [AAS Editor](./features/aas_editor.md) documentation.
```

### AAS Treeview

```{figure} ./images/aas_treeview.png
---
width: 50%
alt: AAS Treeview
name: aas_treeview
---
AAS Treeview
```

The **AAS Treeview** displays the Submodels from the selected AAS in a hierarchical tree structure, allowing you to navigate through the nested SubmodelElements.

**Navigation:**

* Expand and collapse branches by clicking on the expand icon on the left side of each Submodel or SubmodelElementCollection
* Click directly on a Submodel or SubmodelElement to display its details in the Element Details panel on the right

**Quick Actions:**

* **Copy Path**: When a SubmodelElement is selected, click the copy icon on the right side to copy its path to the clipboard
* **Search**: Use the search bar to filter Submodels and SubmodelElements by their `idShort` or `displayName`
* **Expand/Collapse All**: Use the `+` and `-` buttons next to the search bar to expand or collapse all nodes in the tree at once

**Editing Capabilities:**
When in the AAS Editor view, you can **add**, **edit**, and **delete** Submodels and SubmodelElements by clicking the three-dot icon on the right side of each element and selecting the respective action from the context menu.

```{seealso}
For detailed information on editing Submodels and SubmodelElements, see the [AAS Editor](./features/aas_editor.md) documentation.
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

The **Visualization Panel** provides domain-specific, user-friendly visualizations for Submodels and SubmodelElements through the use of **Submodel Plugins**.

**What are Submodel Plugins?**

Submodel Plugins are specialized UI extensions that render Submodels and SubmodelElements based on their semantic meaning. Instead of showing raw data in a generic form, plugins provide tailored visualizations optimized for specific domains (e.g., Digital Nameplate, Time Series Data, Carbon Footprint, Bill of Materials).

```{seealso}
For a complete list of available plugins and their semantic IDs, see the [Plugin Mechanism](./features/plugin_mechanism.md) feature page.

Developers interested in creating custom plugins can refer to the [Creating Submodel Plugins](../../../developer_documentation/basyx_web_ui/creating_submodel_plugins.md) guide.
```

**How Plugins are Selected:**

The AAS Web UI automatically determines which visualization to display based on the following criteria:

1. **Semantic ID Matching**: The AAS Web UI checks if the Submodel or SubmodelElement has a `semanticId`. If a matching Submodel Plugin is available for that semantic ID, the plugin's custom visualization is displayed.

  ```{figure} ./images/ui_visualization.png
  ---
  width: 60%
  alt: Visualization Panel
  name: ui_visualization
  ---
  Plugin-based Visualization
  ```

2. **File and Blob Previews**: File and Blob SubmodelElements have built-in preview capabilities. If the SubmodelElement contains an image, PDF, or CAD file (.stl/.glTF/.obj), the AAS Web UI displays the file contents directly in the Visualization Panel.

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

The **AAS Submodel Viewer** is a streamlined, end-user-focused view designed to present Submodels in an intuitive and accessible way. Unlike the standard AAS Viewer, which shows detailed tree structures and technical metadata, the AAS Submodel Viewer focuses on **visual clarity and ease of use**, making it ideal for users who need to quickly access and understand Submodel content without deep AAS expertise.

**Key Characteristics:**

* **AAS-centric approach**: You first select an AAS from the AAS List, then navigate through its Submodels
* **Plugin-based visualization**: Submodels are rendered using Submodel Plugins that provide domain-specific, user-friendly interfaces
* **Simplified navigation**: Only top-level Submodels are shown in a list view—no nested tree structures or technical details
* **Fallback rendering**: If no matching plugin is found for a Submodel's semantic ID, a generic visualization is displayed

**Accessing the AAS Submodel Viewer:**

You can access the AAS Submodel Viewer via the main menu by clicking on the **AAS Submodel Viewer** button. After selecting an AAS from the AAS List Sidebar, you'll see a card-based view of all available Submodels for that AAS.

```{figure} ./images/aas_submodel_viewer.png
---
width: 100%
alt: AAS Submodel Viewer
name: aas_submodel_viewer
---
AAS Submodel Viewer Page
```

```{hint}
The AAS Submodel Viewer is particularly useful for presentations, demos, and scenarios where non-technical users need to interact with AAS data.
```

## Submodel Viewer & Editor

The **Submodel Viewer & Editor** is a dedicated page in the BaSyx AAS Web UI that provides a **submodel-centric** view, as opposed to the AAS-centric views described above. This means you work directly with Submodels as standalone entities, independent of a specific Asset Administration Shell.

**When to Use the Submodel Viewer & Editor:**

This view is particularly useful when:

* You want to focus on a specific Submodel without navigating through an entire AAS structure
* You need to view or edit Submodels that are stored in a Submodel Repository but not yet linked to an AAS
* You're working in a scenario where Submodels are managed independently (e.g., library of reusable Submodel templates)
* You want direct access to Submodel content without the overhead of selecting an AAS first

**Key Features:**

* **Direct Submodel access**: Browse and select Submodels directly from the connected Submodel Repository
* **Plugin-based visualization**: Just like in the Visualization Panel, Submodels are rendered using matching Submodel Plugins based on their semantic IDs
* **Full editing capabilities**: All editing functionalities available in the AAS Editor also apply here, allowing you to create, modify, and delete Submodels and their SubmodelElements

**Accessing the Submodel Viewer & Editor:**

You can access this view via the main menu by selecting the **Submodel Viewer & Editor** option.

```{seealso}
For detailed information on editing capabilities (creating, modifying, and deleting Submodels and SubmodelElements), see the [AAS Editor](./features/aas_editor.md) documentation. The same editing features are available in the Submodel Viewer & Editor.
```

```{note}
The main difference between the **AAS Submodel Viewer** and the **Submodel Viewer & Editor** is the starting point: The AAS Submodel Viewer requires you to select an AAS first and then shows its Submodels, while the Submodel Viewer & Editor gives you direct access to Submodels from the repository without requiring an AAS selection.
```

## Extension Modules

The BaSyx AAS Web UI is built as a **modular platform** that can be extended with **Extension Modules**—self-contained application features that provide specialized functionality beyond the core AAS visualization and navigation capabilities.

**What are Extension Modules?**

Extension Modules are dedicated applications integrated into the Web UI that address specific use cases or workflows. Each module:

* Has its own page accessible via the main menu under the "Modules" section
* Operates within the same Web UI shell (using the same navigation, authentication, and backend connections)
* Can span multiple Submodels, implement custom workflows, or provide analytical capabilities

**Benefits of Extension Modules:**

* **Task-specific interfaces**: Modules provide optimized UIs for specific workflows rather than generic data visualization
* **Integration**: All modules share the same backend infrastructure and authentication, providing a seamless experience
* **Extensibility**: New modules can be added to meet evolving requirements without modifying the core Web UI

**Available Built-in Modules:**

The BaSyx AAS Web UI comes with several pre-built modules, including:

* **PCF Process Module**: Guides users through the Product Carbon Footprint (PCF) calculation workflow, from material selection to generating PCF Submodels for product instances. Learn more about PCF calculation in the [Product Carbon Footprint](../../../concepts/use_cases/pcf_calculation.md) use case documentation.
* **AAS Importer**: Import Asset Administration Shells and Submodels from configured AAS infrastructures into your own AAS infrastructure.
* **AAS Query Language**: Execute complex queries across multiple AAS and Submodels using a dedicated query language. Learn more in the [AAS Query Language](../../../concepts/use_cases/aas_query_language.md) documentation.
* **Company Data Portal**: Centralized portal for managing and visualizing company-specific AAS data.
* **Additional domain-specific modules**: Depending on your deployment, additional modules may be available for specific industries or use cases

**Accessing Extension Modules:**

You can access Extension Modules via the main menu by selecting the **Modules** tab or clicking on a specific module entry in the navigation drawer.

```{seealso}
Developers interested in creating their own Extension Modules can refer to the [Developing Custom Modules](../../../developer_documentation/basyx_web_ui/developing_custom_modules.md) guide in the developer documentation.
```

```{hint}
Extension Modules are designed to be customizable and can be tailored to specific organizational needs, industry requirements, or research scenarios. Contact the BaSyx community if you're interested in developing or sharing modules.
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
