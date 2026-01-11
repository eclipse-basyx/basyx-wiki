# Design Guidelines

This section defines the **design, architectural, and code-style guidelines** for developing and extending the **BaSyx AAS Web UI**. Its goal is to ensure consistency, maintainability, and long-term extensibility across core features, plugins, and custom modules.

These guidelines complement automated checks enforced by ESLint, Prettier, and CI, and document conventions that go beyond what tooling alone can express.

## UI & UX Design Principles

### Vuetify Usage and Theming

The Web UI is based on **Vuetify 3**. Global UI behavior is defined in:

```bash
src/plugins/vuetify.ts
```

This file:

* Defines global Vuetify defaults
* Integrates corporate design settings from environment variables
* Centralizes color and theme configuration

Contributors should not hardcode colors or theme values in components. Instead, styling must rely on Vuetify theming and the configured design tokens.

```{note}
Please use the `primary` color as highlight color unless a different semantic meaning is required.
```

### Spacing, Density, and Responsiveness

* Most UI elements use dense spacing by default
* Mobile responsiveness must be considered for:
  * Viewer pages
  * Plugins
  * Custom modules
* Editing workflows are primarily optimized for desktop use cases

Layouts should degrade gracefully on smaller screens even if full editing is not supported.

### Icons

* [Material Design Icons (MDI)](https://pictogrammers.com/library/mdi/) are the default icon set
* Custom icons are allowed for well-defined domain concepts
  * Example: custom AAS icon
  * See `src/assets/Icons/customIcons.ts` for existing custom icons

Custom icons should be added centrally and reused consistently.

### Lists vs Tables

There is no strict preference between lists and tables:

* Choose the representation that best fits the use case
* Mixed approaches are acceptable

Example: the *Technical Data* submodel plugin supports both list and table views, allowing users to switch dynamically.

## Component Design

### Naming and Structure

* Vue components must use PascalCase file names
* Components in `src/components/` are grouped by topic
* Large features should be split into multiple components

Guidelines for component size:

* more than 1000 lines: strongly discouraged
* 200–500 lines: preferred sweet spot

Components should be split when it improves:

* Readability
* Reuse
* Performance

### Global Component Registration

All components in `src/components/` are globally auto-registered.

* Components must not be imported manually
* This behavior is intentional and relied upon throughout the codebase

### Plugins vs User Plugins

* Core plugins belong in `src/components/Plugins/`
* User- or company-specific plugins belong in `src/UserPlugins/`

This separation avoids polluting the core UI with domain- or customer-specific logic.

## Vue & TypeScript Guidelines

### Script Setup

* `<script setup lang="ts">` is **mandatory**
* Composition API usage is validated via ESLint

### Reactive Patterns

The following Vue APIs are allowed and expected:

* `ref`
* `reactive`
* `computed`
* `watch` / `watchEffect`

Usage should follow **Vue best practices**:

* Avoid unnecessary watchers
* Prefer computed properties over imperative updates
* Keep side effects explicit and localized

Business logic should not live in components if it can be expressed via composables or stores.

### Props and Emits Typing

Props and emits must be fully typed using the Composition API helpers:

```ts
const props = defineProps<Props>();

const emit = defineEmits<{
  (event: 'update:modelValue', value: string | null): void;
}>();
```

This pattern is the preferred and expected style across the project.

## State Management & Business Logic

### Stores vs Composables

The recommended separation of concerns is:

* **Pinia stores**
  * State
  * Caching
  * Cross-component data sharing
* **Composables**
  * Orchestration logic
  * AAS-specific workflows
  * Backend interaction

### API Access Rules

* **Direct API calls from components are discouraged**
* **Direct calls to AAS APIs are forbidden**

All AAS-related backend interaction must go through the provided composables:

* `src/composables/AAS/AASHandling`
* `src/composables/AAS/SubmodelHandling`
* `src/composables/AAS/SMEHandling`
* `src/composables/AAS/ConceptDescriptionHandling`
* Related client composables

This ensures consistent behavior, caching, and error handling.

## AAS-Specific UI Guidelines

### Naming and Descriptions

For all Identifiables and Referables:

* Names must be resolved via `nameToDisplay(...)`
* Descriptions must be resolved via `descriptionToDisplay(...)`

These utilities:

* Apply consistent fallback logic
* Respect language preferences
* Are defined in `src/composables/AAS/referableUtils`

```{note}
The default language is English, but a different language can be provided explicitly.
```

### Semantic IDs

* Semantic IDs should be visible in expert views
* They may be hidden in pure viewer modes

### Editing Rules

Editing UI elements must respect feature flags:

* Editing is only allowed if `ALLOW_EDITING=true` (default setting, can be overridden using environment variables)
* UI must not expose editing actions otherwise

## Plugins vs Modules (High-Level Guidance)

A rough rule of thumb:

* **Plugins**
  * Visualization can be chosen solely by `semanticId`
  * Scope is one submodel or submodel element
  * No overarching business logic
* **Modules**
  * Cross-cutting or workflow-oriented use cases
  * Multiple submodels or templates involved
  * Complex logic or large visualizations

Detailed instructions are provided in the dedicated sections:

* [Creating Submodel Plugins](creating_submodel_plugins.md)
* [Developing Custom Modules](developing_custom_modules.md)

## Code Style & Linting

Code style is enforced via ESLint and Prettier.

Key conventions:

* Prettier formatting via ESLint
* Sorted imports (lint-enforced)
* No default exports (Vue SFCs excepted)
* Use the `@/` alias for absolute imports
* Absolute paths must respect the configured base path

```{hint}
Run `yarn lint:fix` before opening a pull request to resolve formatting and style issues locally.
```

## Testing Considerations

Detailed testing guidance is covered in the [Testing & Quality Assurance section](testing.md).

Within design guidelines:

* Utility functions are expected to include tests
* UI and component tests are encouraged but not mandatory here

## Summary

Following these design guidelines ensures that the BaSyx AAS Web UI remains:

* Consistent in look and behavior
* Maintainable as the AAS specification evolves
* Extensible for plugins, modules, and research prototypes

All contributors are expected to follow these conventions when extending or modifying the UI.
