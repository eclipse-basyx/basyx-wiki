# BaSyx AAS Web UI

This section provides in-depth documentation for the BaSyx AAS Web UI intended for developers and contributors. If your goal is to use the off-the-shelf components as-is, please refer to the [Components Documentation](../../user_documentation/basyx_components/index.md) as well as the [Getting Started Guide](../../introduction/quickstart.md).

The BaSyx AAS Web UI is **not just a standalone frontend application**, but **a modular and extensible frontend platform** for Asset Administration Shell (AAS)–based systems. It is designed to support a wide range of AAS use cases through a plugin-oriented architecture, allowing developers to extend and adapt the UI via custom modules and submodel-specific plugins. The UI is tightly coupled to AAS semantics and the underlying specifications, and is intended to continuously evolve alongside the AAS standard and the BaSyx middleware ecosystem.

The Web UI is part of the **Eclipse BaSyx V2 middleware** and provides a user-friendly yet technically powerful interface for visualizing, editing, and interacting with Asset Administration Shells and their submodels. It is built using **Vue.js 3** and **TypeScript**, with **Vuetify 3** as the UI framework. The following sections document the architectural concepts, development workflows, extension mechanisms, and design principles relevant for extending and maintaining the Web UI.

## Intended Audience

This documentation is aimed at readers who want to **develop**, **extend**, or **integrate** the BaSyx AAS Web UI, including:

* **Core contributors** working on the BaSyx AAS Web UI itself
* **Plugin and module developers** implementing custom submodel visualizations or UI extensions
* **System integrators** embedding or adapting the Web UI within larger AAS infrastructures
* **Researchers and prototypers** building experimental or domain-specific AAS-based tools

```{hint}
If you are primarily interested in using the Web UI rather than developing or extending it, the [user-facing documentation](../../user_documentation/basyx_components/web_ui/index.md) is likely more suitable.
```

## Table of Contents

* [Core Concepts](core_concepts.md)
* [Architecture Overview](architecture.md)
* [Getting Started with Development](getting_started.md)
* [Configuration & Environment](configuration.md)
* [Design Guidelines](design_guidelines.md)
* [Testing & Quality Assurance](testing.md)
* [Creating Submodel Plugins](creating_submodel_plugins.md)
* [Developing Custom Modules](developing_custom_modules.md)
* [Defining Hotkeys](hotkeys.md)

```{toctree}
:hidden:
:maxdepth: 1

core_concepts
architecture
getting_started
configuration
design_guidelines
testing
creating_submodel_plugins
developing_custom_modules
hotkeys
```
