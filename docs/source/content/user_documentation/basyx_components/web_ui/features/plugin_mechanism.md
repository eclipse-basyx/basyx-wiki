# Plugin Mechanism

> **As a** BaSyx AAS Web UI user  
> **I want to** extend the UI with custom plugins  
> **so that** I can visualize and interact with Submodels and SubmodelElements using user-friendly interfaces.

## Feature Overview

Plugins can be integrated in the *"Visualization"* view of the UI. The Plugin-Feature checks if the selected Submodel/SubmodelElement includes a `SemanticId` and displays a plugin automatically if one is available for the given Semantic ID.

Currently, the following plugins are available:

| List of available plugins | | |
| :-------------------------: | :-------------------------: | :-------------------------: |
| Name | SemanticId | Description |
| [Digital Nameplate V2](https://industrialdigitaltwin.org/wp-content/uploads/2022/10/IDTA-02006-2-0_Submodel_Digital-Nameplate.pdf) | `https://admin-shell.io/zvei/nameplate/2/0/Nameplate` | This Plugin is intented to visualize Digital Nameplate Submodels. It displays the SubmodelElements in an expandable panel view. |
| [Digital Nameplate V3](https://industrialdigitaltwin.org/wp-content/uploads/2025/10/IDTA-02006-3-0-1_Submodel_Digital-Nameplate.pdf) | `https://admin-shell.io/idta/nameplate/3/0/Nameplate` | This Plugin is intented to visualize Digital Nameplate Submodels. It displays the SubmodelElements in an expandable panel view. |
| [Time Series Data V1.1](https://industrialdigitaltwin.org/wp-content/uploads/2023/03/IDTA-02008-1-1_Submodel_TimeSeriesData.pdf) | `https://admin-shell.io/idta/TimeSeries/1/1` | This Plugin is intented to visualize Time Series Data Submodels using different chart types. It displays the time series data coming from either AAS properties, file SubmodelElements or from external time series databases (InfluxDB). |
| [Bills of Material V1](https://industrialdigitaltwin.org/wp-content/uploads/2024/06/IDTA-02011-1-1_Submodel_HierarchicalStructuresEnablingBoM.pdf) | `https://admin-shell.io/idta/HierarchicalStructures/1/0/Submodel` | This Plugin is intented to visualize Bills of Material Submodels. It displays the Bill of Material in a tree view chart. |
| [Handover Documentation V1.2](https://industrialdigitaltwin.org/wp-content/uploads/2023/03/IDTA-02004-1-2_Submodel_Handover-Documentation.pdf) | `0173-1#01-AHF578#001` | This Plugin is intented to visualize Handover Documentation Submodels. It displays the Handover Documentation in an extandable view. PDFs, Images and CAD files are previewed. |
| [Contact Information V1](https://industrialdigitaltwin.org/wp-content/uploads/2022/10/IDTA-02002-1-0_Submodel_ContactInformation.pdf) | `https://admin-shell.io/zvei/nameplate/1/0/ContactInformations` | This Plugin is intented to visualize Contact Information Submodels. It displays the Contact Information in a table view. |
| [Technical Data V1.2](https://industrialdigitaltwin.org/wp-content/uploads/2022/10/IDTA-02003-1-2_Submodel_TechnicalData.pdf) | `https://admin-shell.io/ZVEI/TechnicalData/Submodel/1/2` | This Plugin is intented to visualize Technical Data Submodels. It displays the Technical Data in an expandable panel view. |
| [Carbon Footprint V0.9](https://industrialdigitaltwin.org/wp-content/uploads/2024/01/IDTA-2023-0-9-_Submodel_CarbonFootprint.pdf) | `https://admin-shell.io/idta/CarbonFootprint/CarbonFootprint/0/9` | This Plugin is intented to visualize Carbon Footprint Submodels. It displays a timeline of all PCF values. |
| [Carbon Footprint V1.0](https://industrialdigitaltwin.org/wp-content/uploads/2025/03/IDTA-02023_Submodel_CarbonFootprint.pdf) | `https://admin-shell.io/idta/CarbonFootprint/CarbonFootprint/1/0` | This Plugin is intented to visualize Carbon Footprint Submodels. It displays a timeline of all PCF values and a pie chart if the PCF values share the same reference value. |
| HelloWorldPlugin | `http://hello.world.de/plugin_submodel` | This plugin is a simple example plugin which displays a Submodel in a generic way and allows to edit the SubmodelElements. It is intended to be used as a template for developing your own plugins. |
| JSONArrayProperty | `http://iese.fraunhofer.de/prop_jsonarray` | This plugin can be used to visualize data series from Property values in a chart. It is possible to visualize single or multiple series. Example Values: `[11, 32, 45, 32, 34, 52, 41] or { "series1": [31, 40, 28, 51, 42, 109, 100], "Series2": [11, 32, 45, 32, 34, 52, 41] }` |
| HTWFuehrungskomponente | `http://htw-berlin.de/smc_statemachine` | This plugin visualizes Submodels and SubmodelElementCollections which include properties to interact with PackML state machines. It allows to trigger state transitions as well as changing the operating mode. |

## Developing your own Plugin

If you are interested in developing your own plugin for the BaSyx AAS Web UI, please refer to the [Plugin Development Guide](../../../../developer_documentation/basyx_web_ui/creating_submodel_plugins.md).
