# Core Concepts

This section introduces the core concepts of the **BaSyx AAS Web UI** that are essential for understanding its architecture, extension points, and development model. The goal is to establish a shared mental model for contributors and extension developers before diving into implementation details.

The BaSyx AAS Web UI is designed as a **frontend platform for Asset Administration Shell–based systems**, not as a fixed or monolithic application. Most architectural decisions, abstractions, and APIs are driven by this platform mindset.

## Platform-Oriented UI

The Web UI acts as a **generic visualization and interaction layer for AAS infrastructures**. It does not encode domain-specific logic directly, but instead provides:

* A stable core for navigation, state handling, authentication, and backend communication
* Well-defined extension points for domain- or submodel-specific functionality
* A clear separation between generic AAS concepts and custom UI behavior

This allows the UI to be reused across different industries, domains, and research contexts while remaining adaptable to evolving requirements.

## Asset Administration Shell–Driven Design

The UI is tightly aligned with the **AAS meta-model and semantics**:

* AAS, Submodels, and Submodel Elements are treated as first-class UI concepts
* UI behavior and structure are derived from AAS metadata rather than hardcoded assumptions
* Semantic identifiers, idShorts, and model structure directly influence rendering and interaction

As a result, the Web UI reflects the structure and meaning of the underlying AAS data instead of abstracting it away. This makes it suitable for both operational use and engineering or research scenarios where transparency is required.

## Modules

Modules are the primary building blocks of the Web UI at the application level. They are used to extend and customize the core functionality of the platform with domain specific features bundled as applications as part of the overall UI.

A module typically:

* Represents a specific use case (e.g., AAS querying, carbon footprint calculation, Digital Product Passport visualization)
* Contributes routes, views, and navigation entries
* Integrates with shared services such as state management, backend APIs, and authentication

Modules are loaded as part of the application build and form the structural backbone of the UI. They are intended for larger, cross-cutting functionality rather than fine-grained customization.

```{hint}
Modules could as well be standalone applications. However, in the context of the BaSyx AAS Web UI, they are designed to be integrated into a common platform to provide a unified user experience across different AAS-related functionalities. This has two main advantages:

* **Consistency**: Users benefit from a consistent look and feel, navigation structure, and shared services across different modules.
* **Extensibility**: New modules can be added to the platform without modifying the core application, allowing for easier maintenance and evolution.
```

## Submodel Plugins

Submodel plugins are specialized UI extensions for rendering and interacting with specific submodels.

Key characteristics:

* Bound to one or more submodel semantics (via semantic IDs)
* Encapsulate domain-specific visualization and interaction logic
* Rendered dynamically at runtime based on the selected submodel

Submodel plugins enable domain experts and integrators to implement tailored user interfaces for their submodels without modifying the core UI or UI building blocks.

```{hint}
The BaSyx AAS Web UI already comes with a set of built-in submodel plugins for commonly used Submodels (excerpt):

* **Digital Nameplate**: Renders identification and classification information.
* **Technical Data**: Displays technical specifications and parameters.
* **Product Carbon Footprint**: Visualizes environmental impact data.
* **Handover Documentation**: Shows documentation and manuals related to the asset.
* **Time Series Data**: Presents historical data in chart form.
* **Bill of Materials**: Displays component hierarchies and relationships.
* **Contact Information**: Renders contact details and responsible parties.
* ... and more.
```

## Runtime vs. Build-Time Extensibility

The Web UI distinguishes between different extension scopes:

* **Build-time extensibility**: Modules and plugins are added during development and included in the application build
* **Runtime configurability**: Behavior, backend connections, corporate design, authentication settings, and feature toggles are configured at runtime

This separation ensures a stable and predictable deployment while still allowing flexible configuration in different environments and infrastructures.

## Separation of Concerns

The architecture follows a strict separation between:

* **UI logic** (components, views, layouts)
* **Application logic** (modules, routing, state management)
* **AAS access logic** (API clients, data mapping, backend abstraction)

This separation improves maintainability, testability, and reuse, and enables contributors to work on isolated aspects of the system without unintended side effects.

## Evolution with the AAS Specification

The Web UI is designed to evolve alongside the Asset Administration Shell specification and the BaSyx middleware:

* Meta-model changes are expected and explicitly accounted for
* New AAS concepts can be integrated without architectural redesign
* Experimental or emerging features can be prototyped via plugins or custom modules

This makes the UI suitable not only for production deployments but also for research, standardization, and exploratory development.

## Summary

In short, the BaSyx AAS Web UI is:

* **A platform**, not just an application
* **AAS-driven** in structure and behavior
* **Modular** at the application level
* **Extensible** through submodel plugins
* **Designed for long-term evolution** with the AAS ecosystem

Understanding these core concepts will make it significantly easier to navigate the architecture and effectively extend the Web UI in the following sections.
