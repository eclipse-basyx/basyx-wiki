# Developing Custom Modules

This section explains how to develop custom modules for the **BaSyx AAS Web UI**.

Modules are the right extension mechanism when you want to implement **larger, workflow-oriented features** that go beyond a single Submodel or SubmodelElement visualization. Typical examples include import/export workflows, cross-submodel analytics, dashboards, or domain-specific tools.

## Prerequisites and Related Docs

Before starting, it is strongly recommended to read:

* [Architecture Overview](architecture.md) – how modules fit into the application
* [Configuration & Environment](configuration.md) – feature flags, infrastructure setup
* [Design Guidelines](design_guidelines.md) – UI, code style, and Vue conventions
* [Testing & Quality Assurance](testing.md) – optional testing guidance
* [Creating Submodel Plugins](creating_submodel_plugins.md) – when a plugin might be a better fit

## What Is a Module?

A module is a self-contained application feature that:

* Has its own route under `<web-ui-url>/modules/...`
* Appears as an entry in the Modules tab of the main menu
* Runs inside the standard application shell (app bar, footer)
* Has full control over its internal layout and navigation

Modules are typically used when:

* Multiple submodels or submodel elements are involved
* Business logic spans more than a single visualization panel
* Dedicated workflows, forms, or dashboards are required

## Where Modules Live

All modules are located in:

```
src/pages/modules/
```

### Simple modules

A single Vue file placed directly in this directory automatically becomes a module:

```
src/pages/modules/MyModule.vue
```

This creates:

* Route: `/modules/mymodule`
* Menu entry: MyModule (or a custom title)

### Larger modules

For larger modules, use a dedicated directory and a top-level entry file:

```
src/pages/modules/PcfProcess.vue
src/pages/modules/PcfProcess/
  ├── components/
  ├── composables/
  ├── stores/
  └── utils/
```

Best practices:

* The directory name and top-level `.vue` file should match
* The top-level file acts as the module entry point
* Internal views/components are imported from the module directory

## Automatic Route Generation

Module routes are generated dynamically at startup:

```ts
const moduleFileRecords = import.meta.glob('@/pages/modules/*.vue');
```

For each module file:

* The file name becomes the route name and base path
* The component is lazy-loaded
* Route metadata is derived from `defineOptions`

Example generated route:

```
/modules/pcfprocess
```

```{hint}
No manual router configuration is required.
```

## Module Options

Modules declare metadata using `defineOptions`:

```ts
defineOptions({
  inheritAttrs: false,
  isDesktopModule: true,
  isMobileModule: true,
  isVisibleModule: true,
  isOnlyVisibleWithSelectedAas: false,
  isOnlyVisibleWithSelectedNode: false,
  moduleTitle: 'PCF Process',
});
```

### Option reference

| Option | Description |
| ------ | ----------- |
| `moduleTitle` | Display name in the Modules menu (defaults to file name) |
| `isDesktopModule` | Visible in desktop layout (default: `true`) |
| `isMobileModule` | Visible in mobile layout (default: `false`) |
| `isVisibleModule` | Controls menu visibility (route still accessible) |
| `isOnlyVisibleWithSelectedAas` | Only visible when an AAS is selected |
| `isOnlyVisibleWithSelectedNode` | Only visible when a Submodel or SME is selected |
| `preserveRouteQuery` | Preserve `aas`/`path` query parameters in the route |

```{note}
If `isOnlyVisibleWithSelectedAas` or `isOnlyVisibleWithSelectedNode` is set, `preserveRouteQuery` is enabled automatically.
```

### Hotkeys

Modules can also define their own hotkeys. Hotkeys are a way to provide keyboard shortcuts for actions within the module.

In order to define hotkeys for a module, it is recommended to create a second `<script setup>` block in the module's main Vue file. This block should import and use the type `PageShortcutDefinitions` from the `useRouteShortcuts` composable.

The following example showcases how to define a hotkey that clears an asset ID input field when the user presses `Cmd+Shift+Backspace`:

```ts
<script lang="ts">
    import type { PageShortcutDefinitions } from '@/composables/Shortcuts/useRouteShortcuts';

    // Module shortcuts definition - available when this module is active
    export const shortcuts: PageShortcutDefinitions = () => [
        {
            id: 'my-module-clear-asset-id',
            title: 'Clear Asset ID',
            description: 'Clear the asset ID input field',
            prependIcon: 'mdi-eraser',
            category: 'My Module Shortcuts',
            keys: 'cmd+shift+backspace',
            handler: (event: KeyboardEvent) => {
                event.preventDefault();
                event.stopPropagation();
                const assetIdInput = document.querySelector('#asset-id-input input') as HTMLInputElement;
                if (assetIdInput) {
                    assetIdInput.value = '';
                    assetIdInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
            },
        },
    ];
</script>
```

```{hint}
For more details on defining hotkeys, refer to the [Defining Hotkeys](hotkeys.md) section.
```

## Modules in the Main Menu

The main menu contains three tabs:

* **AAS** - AAS related pages
* **Submodels** - Submodel and SME related pages
* **Modules** - Custom modules

All registered modules appear in the Modules tab.

```{figure} images/module_menu.png
---
name: module_menu
---
Modules tab in the main menu.
```

Menu behavior:

* Modules are filtered based on mobile/desktop mode
* Visibility depends on AAS / node selection
* Modules are sorted alphabetically by name

## Mobile vs Desktop Modules

The application distinguishes between mobile and desktop layouts using responsive breakpoints.

Use `isDesktopModule` and `isMobileModule` to control where a module appears.

Typical patterns:

* Complex workflows: desktop-only
* Viewer-style dashboards: desktop + mobile

## Accessing Context and State

### Selected AAS and Node

Modules should access the current selection via the AAS Store:

```ts
import { useAASStore } from '@/store/AASDataStore';

const aasStore = useAASStore();

const selectedAas = aasStore.getSelectedAAS;
const selectedNode = aasStore.getSelectedNode;
```

If `preserveRouteQuery` is enabled, the following are also available via the router:

* `aas` query parameter
* `path` query parameter

This allows reloading the page without losing context.

### Loading and Modifying AAS Data

Modules should reuse the same composables as core pages and plugins:

* `useAASHandling`
* `useSMHandling`
* Client composables for repositories and registries

```{warning}
Direct API calls to AAS backend services are discouraged.
```

## Routing Inside Modules

Each module has a single base route:

```
/modules/<module-name>
```

Modules may define **nested routes** below this base route for internal navigation.

Implementation choices are flexible:

* Nested Vue Router routes
* Internal tabs
* Navigation drawers
* ...

Deep linking is encouraged but not required.

## Layout Guidelines

Modules are rendered inside the standard application shell:

* App bar and menus are provided by the host application
* The module controls the main content area

Recommended layout pattern:

```html
<v-container fluid>
  <!-- module content -->
</v-container>
```

```{figure} images/module_layout.png
---
name: module_layout
---
Typical module layout inside the application shell.
```

## Feature Flags and Security

Modules must respect global feature flags:

* `ALLOW_EDITING`
* `ALLOW_UPLOADING`
* related environment flags

These flags are available via the Environment Store.

```{warning}
Accessing the Infrastructure Store directly from modules should be avoided unless absolutely necessary.

Some modules (e.g. import/export workflows) may intentionally interact with multiple infrastructures, but this should be done explicitly and with care.
```

## Testing Modules

There is currently no strict testing requirement for modules.

Recommended approach:

* Move complex logic into composables or utils
* Test those units as described in [Testing & Quality Assurance](testing.md)
* Use manual testing for UI-heavy workflows

## Existing Modules as Reference

The following modules demonstrate common patterns:

* **Test** – minimal module structure
* **PcfProcess** – dedicated module directory, AAS & SM handling
* **AasImporter** – infrastructure access and data transfer
* **QueryLanguage** – client composables usage
* **TestPreserveUrlQuery** – route query preservation

```{hint}
Studying existing modules is often the fastest way to understand best practices.
```

## Summary

Modules provide a powerful extension mechanism for the BaSyx AAS Web UI:

* Automatic routing and menu integration
* Full-screen application features
* Access to shared state, composables, and infrastructure
* Clear separation from submodel-level plugins

When a feature grows beyond a single semantic visualization, a **module** is usually the right architectural choice.
