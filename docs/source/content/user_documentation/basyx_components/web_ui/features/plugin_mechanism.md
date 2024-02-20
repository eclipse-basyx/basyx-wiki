# Plugin Mechanism
>As AAS Web UI user
>I want to visualize and interact with Submodels and SubmodelElements in custom ways
>The AAS Web UI provides a feature to integrate your own plugins to visualize and interact with Submodels and SubmodelElements.

## Feature Overview
Plugins can be integrated in the *"Visualization"* view of the UI. The Plugin-Feature checks if the selected Submodel/SubmodelElement includes a **SemanticId** and displays a plugin automatically if one is available for the given SemanticId.

Currently, there are four plugins available:

| List of available plugins 	|                                                     	|                                                                                                                                                                                                                                                                                 	|
|:-------------------------:	|:---------------------------------------------------:	|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:	|
|            Name           	|                      SemanticId                     	|                                                                                                                                   Description                                                                                                                                   	|
| HTWFuehrungskomponente    	|        http://htw-berlin.de/smc_statemachine        	| This plugin visualizes Submodels and SubmodelElementCollections which include properties to interact with PackML state machines. It allows to trigger state transitions as well as changing the operating mode.                                                                 	|
| DigitalNameplate          	| https://admin-shell.io/zvei/nameplate/1/0/Nameplate 	| This Plugin is intented to visualize Digital Nameplate Submodels. It displays the SubmodelElements in an expandable panel view. Structure of the Digital Nameplate: [Digital Nameplate PDF](./datei/IDTA%2002006-2-0_Submodel_Digital%20Nameplate.pdf)                                                                                      	|
| HelloWorldPlugin          	|        http://hello.world.de/plugin_submodel        	| This plugin is a simple example plugin which displays a Submodel in a generic way and allows to edit the SubmodelElements. It is intended to be used as a template for developing your own plugins.                                                                             	|
| JSONArrayProperty         	|       http://iese.fraunhofer.de/prop_jsonarray      	| This plugin can be used to visualize data series from Property values in a chart. It is possible to visualize single or multiple series. Example Values: `[11, 32, 45, 32, 34, 52, 41] or { "series1": [31, 40, 28, 51, 42, 109, 100], "Series2": [11, 32, 45, 32, 34, 52, 41] }` 	|

## Developing your own Plugins
New Plugins have to be written in vue.js 3 (in TypeScript) and are implemented as own .vue File/Component.

Plugins are automatically integrated into the application when they are saved in the *"UserPlugins"*-Folder at `Frontend/aas-web-gui/src/UserPlugins/`

A good starting point is the HelloWorld-Plugin which is already present in the mentioned folder.

## Using external Plugins
It is also possible to use plugins which are not part of the application itself.

To use external plugins, you have to mount a local plugins folder containing .vue plugin-files.

This can either be done in the *docker run* command or in the *docker-compose* file:

**docker run**:

`docker run -p 3000:3000 -v <local_path_to_plugins>:/app/src/UserPlugins eclipsebasyx/aas-gui`

**docker-compose**:
```
 aas-web-gui:
     image: eclipsebasyx/aas-gui
     container_name: aas-web-gui
     ports:
         - "3000:3000"
     volumes:
         - <local_path_to_plugins>:/app/src/UserPlugins
```