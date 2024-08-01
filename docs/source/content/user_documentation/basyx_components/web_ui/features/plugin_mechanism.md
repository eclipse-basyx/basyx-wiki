# Plugin Mechanism

>As AAS Web UI user
>I want to visualize and interact with Submodels and SubmodelElements in custom ways
>The AAS Web UI provides a feature to integrate your own plugins to visualize and interact with Submodels and SubmodelElements.

## Feature Overview

Plugins can be integrated in the *"Visualization"* view of the UI. The Plugin-Feature checks if the selected Submodel/SubmodelElement includes a **SemanticId** and displays a plugin automatically if one is available for the given SemanticId.

Currently, the following plugins available:

| List of available plugins | | |
| :-------------------------: | :-------------------------: | :-------------------------: |
| Name | SemanticId | Description |
| HTWFuehrungskomponente | http://htw-berlin.de/smc_statemachine | This plugin visualizes Submodels and SubmodelElementCollections which include properties to interact with PackML state machines. It allows to trigger state transitions as well as changing the operating mode. |
| DigitalNameplate | https://admin-shell.io/zvei/nameplate/1/0/Nameplate | This Plugin is intented to visualize Digital Nameplate Submodels. It displays the SubmodelElements in an expandable panel view. Structure of the Digital Nameplate: [Digital Nameplate PDF](./datei/IDTA%2002006-2-0_Submodel_Digital%20Nameplate.pdf) |
| TimeSeriesData | https://admin-shell.io/idta/TimeSeries/1/1 | This Plugin is intented to visualize Time Series Data Submodels using different chart types. It displays the time series data coming from either AAS properties, file SubmodelElements or from external time series databases (InfluxDB). Structure of the Time Series Data : [Time Series Data PDF](./datei/IDTA-02008-1-1_Submodel_TimeSeriesData.pdf) |
| Bills of Material | https://admin-shell.io/idta/HierarchicalStructures/1/0/Submodel | This Plugin is intented to visualize Bills of Material Submodels. It displays the Bill of Material in a tree view chart. Structure of the Bill of Material: [Bill of Material PDF](./datei/IDTA-02011-1-0_Submodel_HierarchicalStructuresEnablingBoM.pdf) |
| Handover Documentation | 0173-1#01-AHF578#001 | This Plugin is intented to visualize Handover Documentation Submodels. It displays the Handover Documentation in an extandable view. PDFs, Images and CAD files are previewed. Structure of the Handover Documentation: [Handover Documentation PDF](./datei/IDTA-02004-1-2_Submodel_Handover-Documentation.pdf) |
| Contact Information | https://admin-shell.io/zvei/nameplate/1/0/ContactInformations | This Plugin is intented to visualize Contact Information Submodels. It displays the Contact Information in a table view. Structure of the Contact Information: [Contact Information PDF](./datei/IDTA-02002-1-0_Submodel_ContactInformation.pdf) |
| Technical Data | https://admin-shell.io/ZVEI/TechnicalData/Submodel/1/2 | This Plugin is intented to visualize Technical Data Submodels. It displays the Technical Data in an expandable panel view. Structure of the Technical Data: [Technical Data PDF](./datei/IDTA-02003-1-2_Submodel_TechnicalData.pdf) |
| HelloWorldPlugin | http://hello.world.de/plugin_submodel | This plugin is a simple example plugin which displays a Submodel in a generic way and allows to edit the SubmodelElements. It is intended to be used as a template for developing your own plugins. |
| JSONArrayProperty | http://iese.fraunhofer.de/prop_jsonarray | This plugin can be used to visualize data series from Property values in a chart. It is possible to visualize single or multiple series. Example Values: `[11, 32, 45, 32, 34, 52, 41] or { "series1": [31, 40, 28, 51, 42, 109, 100], "Series2": [11, 32, 45, 32, 34, 52, 41] }` |

## Developing your own Plugins

New Plugins have to be written in vue.js 3 (in TypeScript) and are implemented as own .vue File/Component.

Plugins are automatically integrated into the application when they are saved in the *"UserPlugins"*-Folder at `Frontend/aas-web-gui/src/UserPlugins/`

A good starting point is the HelloWorld-Plugin which is already present in the mentioned folder.
