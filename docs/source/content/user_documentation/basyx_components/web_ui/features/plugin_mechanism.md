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
| DigitalNameplate | https://admin-shell.io/zvei/nameplate/1/0/Nameplate | This Plugin is intented to visualize Digital Nameplate Submodels. It displays the SubmodelElements in an expandable panel view. Structure of the Digital Nameplate: [Digital Nameplate PDF](./datei/IDTA%2002006-2-0_Submodel_Digital%20Nameplate.pdf) |
| TimeSeriesData | https://admin-shell.io/idta/TimeSeries/1/1 | This Plugin is intented to visualize Time Series Data Submodels using different chart types. It displays the time series data coming from either AAS properties, file SubmodelElements or from external time series databases (InfluxDB). Structure of the Time Series Data : [Time Series Data PDF](./datei/IDTA-02008-1-1_Submodel_TimeSeriesData.pdf) |
| Bills of Material | https://admin-shell.io/idta/HierarchicalStructures/1/0/Submodel | This Plugin is intented to visualize Bills of Material Submodels. It displays the Bill of Material in a tree view chart. Structure of the Bill of Material: [Bill of Material PDF](./datei/IDTA-02011-1-0_Submodel_HierarchicalStructuresEnablingBoM.pdf) |
| Handover Documentation | 0173-1#01-AHF578#001 | This Plugin is intented to visualize Handover Documentation Submodels. It displays the Handover Documentation in an extandable view. PDFs, Images and CAD files are previewed. Structure of the Handover Documentation: [Handover Documentation PDF](./datei/IDTA-02004-1-2_Submodel_Handover-Documentation.pdf) |
| Contact Information | https://admin-shell.io/zvei/nameplate/1/0/ContactInformations | This Plugin is intented to visualize Contact Information Submodels. It displays the Contact Information in a table view. Structure of the Contact Information: [Contact Information PDF](./datei/IDTA-02002-1-0_Submodel_ContactInformation.pdf) |
| Technical Data | https://admin-shell.io/ZVEI/TechnicalData/Submodel/1/2 | This Plugin is intented to visualize Technical Data Submodels. It displays the Technical Data in an expandable panel view. Structure of the Technical Data: [Technical Data PDF](./datei/IDTA-02003-1-2_Submodel_TechnicalData.pdf) |
| HelloWorldPlugin | http://hello.world.de/plugin_submodel | This plugin is a simple example plugin which displays a Submodel in a generic way and allows to edit the SubmodelElements. It is intended to be used as a template for developing your own plugins. |
| JSONArrayProperty | http://iese.fraunhofer.de/prop_jsonarray | This plugin can be used to visualize data series from Property values in a chart. It is possible to visualize single or multiple series. Example Values: `[11, 32, 45, 32, 34, 52, 41] or { "series1": [31, 40, 28, 51, 42, 109, 100], "Series2": [11, 32, 45, 32, 34, 52, 41] }` |
| HTWFuehrungskomponente | http://htw-berlin.de/smc_statemachine | This plugin visualizes Submodels and SubmodelElementCollections which include properties to interact with PackML state machines. It allows to trigger state transitions as well as changing the operating mode. |

## Developing your own Plugins

You can develop your own plugins for the AAS Web UI. For this you will be writing a Vue.js 3 component in TypeScript.

> [!NOTE]
> To get started with Vue.js 3, you can check out the [Vue.js 3 Documentation](https://vuejs.org/guide/introduction.html).

### Prerequisites

Before you start developing your own plugin, make sure you prepared the following:

- **Node.js** and **npm** should be installed on your machine ([Download Node.js](https://nodejs.org/en/download/))
- A **runnin AAS** including a Submodel with a SemanticId that you want to visualize
  - You can use the [BaSyx Starter Kit](https://basyx.org) to create a minimal setup with a running AAS
  - Example AAS can be found in the [BaSyx Examples](https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/BaSyxMinimal/aas)
  - You can use the [AASX Package Explorer](https://github.com/eclipse-aaspe/package-explorer) to create your own AAS and Submodels

### Getting Started

1. Clone the [BaSyx AAS Web UI Repository](https://github.com/eclipse-basyx/basyx-aas-web-ui)
2. Navigate to the `aas-web-ui` directory
3. Install the dependencies by running `yarn install`
4. Start the development server by running `yarn dev`

### Creating a new Plugin

To create your first plugin, navigate to the `UserPLugins` directory in the `src` folder. Here you can create a new Vue component for your plugin.
Vue component files should have the `.vue` extension.

> [!TIP]
> You can use the `HelloWorldPlugin` as a template for your own plugin.

Every vue component should have the following base structure:

```html
<template>
    <!-- Your plugin content goes here -->
</template>

<script lang="ts" setup>
// Your plugin logic goes here
</script>
```

From there you can start to implement you own logic:

1. **Define the SemanticId**: Define the SemanticId of the Submodel or SubmodelElement you want to visualize. It's also good to provide a name for your plugin as well.

   ```typescript
    <script lang="ts" setup>
        import { defineOptions } from 'vue';
        // Further imports go here

        // Plugin name and SemanticId
        defineOptions({
            name: 'MyFirstPlugin',
            semanticId: 'https://example.com/myFirstPlugin',
        });

        // Your plugin logic goes here
    </script>
   ```

2. **Retrieve the Data of the Submodel**: The Submodel data should be retrieved when the component get's mounted. You can use the `onMounted` lifecycle hook for this.

   ```typescript
    <script lang="ts" setup>
        import { defineOptions, onMounted } from 'vue';
        // Further imports go here

        defineOptions({
            name: 'MyFirstPlugin',
            semanticId: 'https://example.com/myFirstPlugin',
        });

        // Call the initializePlugin function when the component is mounted
        onMounted(() => {
            initializePlugin();
        });

        function initializePlugin() {
            // Logic to retrieve the Submodel data goes here
        }
    </script>
   ```

   The `initializePlugin` function will extract the Submodel data from the prop `submodelElementData` that is passed to the component automatically. First, define the prop in the component:

   ```typescript
    <script lang="ts" setup>
        import { defineOptions, onMounted, ref } from 'vue';
        // Further imports go here

        defineOptions({
            name: 'MyFirstPlugin',
            semanticId: 'https://example.com/myFirstPlugin',
        });

        // Define the prop
        const props = defineProps({
            submodelElementData: {
                type: Object as any,
                default: {} as any,
            },
        });

        // Rest of the logic
    </script>
   ```

   Then use the prop in the `initializePlugin` function:

   ```typescript
    function initializePlugin() {
        // Check ig the prop has been passed
        if (!props.submodelElementData || Object.keys(props.submodelElementData).length === 0) {
            return; // Return if no data is available
        }

        // Extract the Submodel data from the prop and save it in a variable
        const mySubmodelData = props.submodelElementData;

        // You can log the data to the console to see the structure
        console.log(mySubmodelData);
    }
   ```

3. **Save the Submodel data in a variable that can be used in the template**: In order to access the Submodel data in the `template` (visual) part of the vue component you need to save the data in a reactive variable. You can use the `ref` function for this.

   ```typescript
    <script lang="ts" setup>
        import { defineOptions, onMounted, ref } from 'vue';
        // Further imports go here

        // defineOptions and defineProps removed for brevity

        // Define a variable to store the Submodel data
        const mySubmodelData = ref<any>({}); // For simplicity we use any as type in this example

        // onMounted hook removed for brevity

        function initializePlugin() {
            // Check ig the prop has been passed
            if (!props.submodelElementData || Object.keys(props.submodelElementData).length === 0) {
                return; // Return if no data is available
            }

            // Extract the Submodel data from the prop and save it in a variable
            mySubmodelData.value = props.submodelElementData;
        }
    </script>
   ```

4. **Calculate pathes of child elements and retrieve Concept Descriptions of elements**: If you need to know the endpoint pathes of every child element of the Submodel for further operations and/or want to access Concept Descriptions of the contained elements, you can use the `calculateSMEPathes` composable (helper function).

   ```typescript
    <script lang="ts" setup>
        import { computed, defineOptions, onMounted, ref } from 'vue';
        import { useSMHandling } from '@/composables/SMHandling';
        import { useAASStore } from '@/store/AASDataStore';
        // Further imports go here

        // defineOptions and defineProps removed for brevity

        // Initialize the AAS Store
        const aasStore = useAASStore();

        // Initialize the SMHandling composable
        const { calculateSMEPathes } = useSMHandling();

        // Define a variable to store the Submodel data
        const mySubmodelData = ref<any>({}); // For simplicity we use any as type in this example

        // Computed property to get the selected node (in this case the currently selected Submodel) from the AAS Store
        const selectedNode = computed(() => aasStore.getSelectedNode);

        // onMounted hook removed for brevity

        // Function now needs to be async
        async function initializePlugin() {
            // Check ig the prop has been passed
            if (!props.submodelElementData || Object.keys(props.submodelElementData).length === 0) {
                return; // Return if no data is available
            }

            // Extract the Submodel data as a copy from the prop and save it in a local variable
            const copiedSubmodelData = { ...props.submodelElementData };

            // Calculate the pathes of the child elements and save the data in the mySubmodelData variable
            mySubmodelData.value = await calculateSMEPathes(copiedSubmodelData, selectedNode.value.path);
        }
    </script>
   ```

4. **Visualize the Submodel data**: Now you can use the `mySubmodelData` variable in the `template` part of the component to visualize the Submodel data.

   ```html
    <template>
        <div>
            <h1>My First Plugin</h1>
            <p>This is my first plugin to visualize a Submodel.</p>
            <p>Submodel Data:</p>
            <pre>{{ mySubmodelData }}</pre>
        </div>
    </template>
   ```

   > [!TIP]
   > You can use [Vuetify Components](https://vuetifyjs.com/en/components/all/#containment) to create a user-friendly interface for your plugin.
