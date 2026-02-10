# Plugins

> **As a** BaSyx AAS Web UI user  
> **I want to** extend the UI with custom plugins  
> **so that** I can visualize and interact with Submodels and SubmodelElements using user-friendly interfaces.

## Feature Overview

Plugins can be integrated in the *"Visualization"* view of the UI. The Plugin-Feature checks if the selected Submodel/SubmodelElement includes a `SemanticId` and displays a plugin automatically if one is available for the given Semantic ID.

## Available Plugins

The BaSyx AAS Web UI includes a growing list of plugins for various IDTA Submodel templates and custom use cases.

```{hint}
**Missing a plugin for your use case?** [Contact us!](mailto:anfrage@iese.fraunhofer.de,frank.schnicke@iese.fraunhofer.de?subject=Commercial%20Support%20Request&body=Hello,%0D%0A%0D%0AWe%20are%20reaching%20out%20to%20inquire%20about%20commercial%20support%20for%20%3CEclipse%20BaSyx%20/%20the%20Asset%20Administration%20Shell%3E.%20We'd%20love%20to%20learn%20more%20about%20your%20offerings.%0D%0A%0D%0AName:%20%3CInsert%20Your%20Name%3E%0D%0ARole:%20%3CInsert%20Your%20Role%3E%0D%0ACompany:%20%3CInsert%20Company%20Name%3E%0D%0AContact:%20%3CInsert%20Your%20Contact%20Info%3E%0D%0A%0D%0A%3CPlease%20add%20any%20additional%20details%20or%20specific%20requests%20here%3E%0D%0A%0D%0ABest%20regards,%0D%0A%3CYour%20Name%3E) to develop a custom plugin tailored to your needs.
```

### IDTA Standard Submodels

**[Digital Nameplate](plugins/digital_nameplate.md)**

- **Semantic IDs**:
  - V2.0: `https://admin-shell.io/zvei/nameplate/2/0/Nameplate`
  - V3.0: `https://admin-shell.io/idta/nameplate/3/0/Nameplate`
- Visualizes Digital Nameplate Submodels in an expandable panel view

**[Time Series Data](plugins/time_series_data.md)**

- **Semantic ID**: `https://admin-shell.io/idta/TimeSeries/1/1`
- Visualizes time series data using different chart types (line, bar, area)
- Supports data from AAS properties, files, and external databases (InfluxDB)

**[Bills of Material](plugins/bom_editor.md)**

- **Semantic ID**: `https://admin-shell.io/idta/HierarchicalStructures/1/0/Submodel`
- Displays Bill of Material Submodels in an interactive tree view chart
- Supports creating and editing hierarchical structures

**[Handover Documentation](plugins/handover_documentation.md)**

- **Semantic ID**:
  - V1.0: `0173-1#01-AHF578#001`
- Displays Handover Documentation in an expandable view
- Provides built-in preview for PDFs, images, and CAD files

**[Contact Information](plugins/contact_information.md)**

- **Semantic ID**: `https://admin-shell.io/zvei/nameplate/1/0/ContactInformations`
- Displays Contact Information Submodels in a table view

**[Technical Data](plugins/technical_data.md)**

- **Semantic ID**:
  - V1.0: `https://admin-shell.io/ZVEI/TechnicalData/Submodel/1/2`
- Displays Technical Data Submodels in a table view
- Provides semantic information for each technical property (e.g., unit, description)

**[Carbon Footprint](plugins/carbon_footprint.md)**

- **Semantic IDs**:
  - V0.9: `https://admin-shell.io/idta/CarbonFootprint/CarbonFootprint/0/9`
  - V1.0: `https://admin-shell.io/idta/CarbonFootprint/CarbonFootprint/1/0`
- Displays timeline of PCF values
- V1.0 adds pie chart visualization when PCF values share the same reference

### Custom & Development Plugins

**[File Explorer](plugins/file_explorer.md)**

- **Semantic ID**: `https://basyx.org/FileSystem/FileSystem/0/1`
- Comprehensive file management interface with cloud storage-like experience
- Supports drag & drop upload, folder management, file preview, and download

**[HelloWorld Plugin](plugins/helloworld_plugin.md)**

- **Semantic ID**: `http://hello.world.de/plugin_submodel`
- Example plugin for learning and development
- Displays Submodels generically with editing capabilities
- Intended as a template for developing your own plugins

**[JSONArray Property](plugins/jsonarray_property.md)**

- **Semantic ID**: `http://iese.fraunhofer.de/prop_jsonarray`
- Visualizes data series from Property values in charts
- Supports single or multiple series visualization

**[HTW Führungskomponente](plugins/htw_fuehrungskomponente.md)**

- **Semantic ID**: `http://htw-berlin.de/smc_statemachine`
- Visualizes and controls PackML state machines
- Allows triggering state transitions and changing operating modes

## Developing your own Plugin

If you are interested in developing your own plugin for the BaSyx AAS Web UI, please refer to the [Plugin Development Guide](../../../../developer_documentation/basyx_web_ui/creating_submodel_plugins.md).

## Detailed Plugin Documentation

For detailed information, screenshots, and usage examples, see the individual plugin pages:

```{toctree}
:maxdepth: 1

plugins/digital_nameplate
plugins/time_series_data
plugins/bom_editor
plugins/handover_documentation
plugins/contact_information
plugins/technical_data
plugins/carbon_footprint
plugins/file_explorer
plugins/helloworld_plugin
plugins/jsonarray_property
plugins/htw_fuehrungskomponente
```
