# Creating Submodel Plugins

This section explains how to create **Submodel Plugins** and **SubmodelElement Plugins** for the **BaSyx AAS Web UI**.

The goal of this page is to enable developers to implement a working plugin end-to-end: from choosing/finding the semantic ID to getting the right data and integrating with the existing UI architecture.

## Prerequisites and Related Docs

Before implementing a plugin, skim these sections:

* [Architecture Overview](architecture.md) – where plugins sit in the overall structure
* [Configuration & Environment](configuration.md) – how infrastructure and feature flags affect plugins
* [Design Guidelines](design_guidelines.md) – UI consistency, code style, and Vue conventions
* [Testing & Quality Assurance](testing.md) – optional testing setup and patterns

External references:

* **<a href="https://smt-repo.admin-shell-io.com/" target="_blank" rel="noopener noreferrer">IDTA Submodel Template Repository</a>** (standardized submodels)
* **<a href="https://industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.1/annex/general.html#matching-strategies-for-semantic-identifiers" target="_blank" rel="noopener noreferrer">Matching strategies for semantic identifiers</a>** (AAS spec annex)
* **<a href="https://github.com/eclipse-basyx/basyx-aas-web-ui/blob/main/aas-web-ui/src/utils/AAS/SemanticIdUtils.ts" target="_blank" rel="noopener noreferrer">BaSyx Web UI semantic ID matching implementation</a>**

## What is a Plugin?

Plugins are Vue components that provide **domain-specific visualization** for a Submodel or SubmodelElement.

Two plugin categories exist:

* **Submodel Plugins** – rendered when a Submodel is selected
* **SubmodelElement Plugins** – rendered when a (nested) SubmodelElement is selected

Both are rendered in the same **visualization panel**.

Plugins are selected and rendered based on the **semanticId** of the currently selected element.

## Where to Place Plugins

### Core plugins (contributed to BaSyx)

Put plugins that should be part of the core Web UI into:

* `src/components/Plugins/Submodels/`
* `src/components/Plugins/SubmodelElements/`

### User / company-specific plugins

If a plugin is intended for a specific deployment (company, demo, research prototype) and should not be merged into the core project, put it into:

* `src/UserPlugins/`

```{hint}
During development, it is common to start in `src/UserPlugins/` and move the plugin into `src/components/Plugins/...` once it is generic and intended for contribution.
```

## Plugin Registration

Plugins are discovered at startup via Vite’s `import.meta.glob(...)` and registered globally:

```ts
async function getVisualizations(app: AppType): Promise<PluginType[]> {
    const pluginFileRecords = {
        ...import.meta.glob('./components/Plugins/Submodels/*.vue'),
        ...import.meta.glob('./components/Plugins/SubmodelElements/*.vue'),
        ...import.meta.glob('./UserPlugins/*.vue'),
    };

    const plugins = [] as Array<PluginType>;

    for (const path in pluginFileRecords) {
        const pluginName = path.split('/').pop()?.replace('.vue', '') || 'UnnamedPlugin';
        const pluginComponent: any = await pluginFileRecords[path]();

        if (pluginComponent.default.semanticId) {
            app.component(pluginName, (pluginComponent.default || pluginComponent));
            plugins.push({ name: pluginName, semanticId: pluginComponent.default.semanticId });
        }
    }

    return plugins;
}
```

✅ Implications:

* Adding a new `.vue` file in these folders is enough (no manual imports)
* New plugin files are picked up automatically by the dev server
* The plugin is only registered if a `semanticId` is provided

## Plugin Matching (Semantic IDs)

### How matching works

Matching is performed **only on the top-level semanticId** of the currently selected Submodel/SubmodelElement.

* Nested elements are not matched automatically
* If you need nested logic, the plugin must handle it internally

Multiple plugins can match and will be rendered **below each other** (this is intended).

### Supported semanticId formats

A plugin may define:#

* a single semanticId as a string
* multiple semanticIds as an array of strings

The UI filters plugins roughly like this:

```ts
if (typeof plugin.semanticId === 'string') {
    return checkSemanticId(submodelElementData.value, plugin.semanticId);
} else if (plugin.semanticId.constructor === Array) {
    for (const pluginSemanticId of plugin.semanticId) {
        if (checkSemanticId(submodelElementData.value, pluginSemanticId)) return true;
    }
}
```

### Matching strategies

The matching logic follows the recommended AAS semantic identifier matching strategies and is implemented in `SemanticIdUtils.ts`:

* [`SemanticIdUtils.ts`](https://github.com/eclipse-basyx/basyx-aas-web-ui/blob/main/aas-web-ui/src/utils/AAS/SemanticIdUtils.ts)

For standardized submodels, use semantic IDs from the IDTA repository:

* [Standardized Submodel Templates](https://smt-repo.admin-shell-io.com/)

```{warning}
When designing a plugin, choose semanticIds that are stable and standardized whenever possible.
```

## How Plugins Are Rendered

Once plugins are loaded and filtered, they are dynamically instantiated:

```html
<component
  :is="plugin.name"
  v-for="(plugin, index) in filteredPlugins"
  :key="index"
  :submodel-element-data="submodelElementData"
>
  {{ plugin.name }}
</component>
```

Fallback behavior when no plugin matches:

* either `GenericDataVisu` is used (when in the Submodel view)
* or a “No available visualization” empty state is shown (when in the AAS view)

## Plugin Contract

### Required: defineOptions and semanticId

A plugin must define `semanticId` in `defineOptions`:

```ts
defineOptions({
  name: 'MyPlugin',
  semanticId: 'https://example.com/semantic-id',
});
```

Multiple semantic IDs:

```ts
defineOptions({
  name: 'MyPlugin',
  semanticId: [
    'https://example.com/semantic-id-1',
    'https://example.com/semantic-id-2',
  ],
});
```

### Required: Prop submodelElementData

All plugins receive the same prop:

```ts
const props = defineProps<{
  submodelElementData: any;
}>();
```

* For Submodel Plugins: this is the selected Submodel
* For SubmodelElement Plugins: this is the selected SubmodelElement

## Recommended Development Flow

1. Pick the semanticId you want to support (prefer standardized IDs)
2. Create the plugin file in the right folder
3. Implement the UI using Vuetify (dense layout, responsive)
4. Reuse existing logic via composables and stores
5. Test manually in both viewer modes:

   * side-by-side (narrow panel ~200px)
   * fullscreen (wide layout)
6. Optionally add a unit test (see [Testing & Quality Assurance](testing.md))

## Reusing Existing Logic (Best Practice)

### Use name/description helpers

Do not implement naming fallbacks manually. Use the composables from the core UI:

* `nameToDisplay(...)`
* `descriptionToDisplay(...)`

See [Design Guidelines](design_guidelines.md) for details.

### Accessing application state

Plugins are expected to use stores and composables rather than reimplementing logic.

Recommended stores:

* `useAASStore()` – primary store (selected node, paths, timestamps)
* `useEnvironmentStore()` – feature flags (e.g. `ALLOW_EDITING`)
* `useNavigationStore()` – optional (e.g. snackbars / notifications)
* `useClipboardStore()` – optional (clipboard support for editing)

```{warning}
Do not access the Infrastructure Store from plugins. Plugins should not depend on infrastructure internals.
```

### Preparing nested data and ConceptDescriptions

If your plugin needs:

* stable `id` fields for nested SMEs
* calculated `path` values
* `timestamp` propagation
* `ConceptDescriptions` resolved and attached

use `useSMHandling().setData(...)`.

What it does (high level):

* assigns unique ids to SMEs
* calculates and assigns paths recursively
* propagates timestamps
* optionally fetches and attaches ConceptDescriptions

Example usage:

```ts
import { computed, onMounted, ref } from 'vue';
import { useSMHandling } from '@/composables/AAS/SMHandling';
import { useAASStore } from '@/store/AASDataStore';

const aasStore = useAASStore();
const { setData } = useSMHandling();

const submodelData = ref<any>({});
const selectedNode = computed(() => aasStore.getSelectedNode);

onMounted(async () => {
  if (!props.submodelElementData || Object.keys(props.submodelElementData).length === 0) return;

  submodelData.value = await setData(
    { ...props.submodelElementData },
    selectedNode.value.path,
    true, // withConceptDescriptions
    selectedNode.value.timestamp
  );
});
```

## Example: Minimal Submodel Plugin

This minimal example demonstrates:

* `semanticId` registration
* using `nameToDisplay(...)`
* using `GenericDataVisu` as a fallback visualization
* preparing nested data via `setData(...)`

```html
<template>
  <v-container fluid class="pa-0">
    <v-card class="mb-3">
      <v-card-title>
        <div class="text-subtitle-1">{{ nameToDisplay(submodelElementData) }}</div>
      </v-card-title>
    </v-card>

    <v-card>
      <v-card-text class="pt-1">
        <GenericDataVisu :submodel-element-data="submodelElementData.submodelElements" />
      </v-card-text>
    </v-card>
  </v-container>
</template>
```

```ts
<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { useReferableUtils } from '@/composables/AAS/ReferableUtils';
import { useSMHandling } from '@/composables/AAS/SMHandling';
import { useAASStore } from '@/store/AASDataStore';

defineOptions({
  name: 'HelloWorldPlugin',
  semanticId: 'http://hello.world.de/plugin_submodel',
});

const props = defineProps<{ submodelElementData: any }>();

const aasStore = useAASStore();
const selectedNode = computed(() => aasStore.getSelectedNode);

const { setData } = useSMHandling();
const { nameToDisplay } = useReferableUtils();

const submodelData = ref<any>({});

onMounted(async () => {
  if (!props.submodelElementData || Object.keys(props.submodelElementData).length === 0) return;

  submodelData.value = await setData(
    { ...props.submodelElementData },
    selectedNode.value.path,
    false,
    selectedNode.value.timestamp
  );
});
</script>
```

## Example: SubmodelElement Plugin (e.g., Chart)

SubmodelElement plugins follow the same contract. They typically:

* read and interpret the selected element value
* update reactively when the prop changes
* integrate with Vuetify theming (dark/light)

Use Vue best practices (e.g., watchers only where needed) and follow [Design Guidelines](design_guidelines.md).

## UI Guidelines for Plugins

Plugins must follow project UI conventions:

* Prefer dense Vuetify components (`density="compact"` where applicable)
* Consider both:
  * narrow visualization panel (~200px)
  * fullscreen viewer mode
* Use Vuetify theming; do not hardcode corporate design colors

```{hint}
If you need a generic fallback visualization for nested structures, `GenericDataVisu` can render complex SME hierarchies via expansion panels.
```

## Editing in Plugins

If your plugin offers editing capabilities, it must respect the global feature flag:

* `ALLOW_EDITING=true`

Check this via the Environment Store and hide/disable editing actions otherwise.

## Testing Plugins (Optional)

Component testing is currently not a major focus in this repository.

If you still want to test your plugin:

* Focus on deterministic transformation logic (move into utils/composables)
* Add unit tests under `src/tests/` as described in:
  * [Testing & Quality Assurance](testing.md)

## Troubleshooting

### Plugin not showing up

Checklist:

* Is the file placed in one of the plugin directories?
* Does it define `semanticId` via `defineOptions`?
* Does the selected Submodel/SubmodelElement have a semanticId?
* Does the semanticId match according to `SemanticIdUtils.ts`?

### Multiple plugins showing

This is expected behavior when multiple plugins match. If you only want one visualization for a semanticId, ensure that only one plugin targets it.

## Next Steps

* [Developing Custom Modules](developing_custom_modules.md)