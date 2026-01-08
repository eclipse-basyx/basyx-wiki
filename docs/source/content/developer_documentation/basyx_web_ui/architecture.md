# Architecture Overview

This document describes the architectural structure of the **BaSyx AAS Web UI**, explains how its main building blocks interact, and maps the conceptual ideas introduced in the [*Core Concepts*](core_concepts.md) section to concrete implementation layers.

The goal of this page is not to document every file in the repository, but to provide developers with a **clear mental model** of how the Web UI is structured, how data flows through the system, and where extensions should be integrated.

## Architectural Style

The BaSyx AAS Web UI is implemented as a single-page application (SPA) using Vue 3. Architecturally, it follows a layered and modular approach:

* **Presentation layer** built from Vue components
* **Application layer** composed of modules, routing, and state management
* **Domain and integration layer** for AAS-specific logic and backend communication
* **Configuration and infrastructure layer** enabling runtime adaptability

This structure supports long-term evolution, extensibility, and parallel development of core features and domain-specific extensions.

## Technology Stack

### Core Technologies

* **Vue 3** with Composition API for component-based UI development
* **TypeScript** for strong typing and API safety
* **Vuetify 3** as the UI component framework
* **Vite** for fast development builds and optimized production output
* **Pinia** for centralized, reactive state management
* **Vue Router** for declarative routing and navigation

### AAS-Specific Libraries

* **@aas-core-works/aas-core3.0-typescript** for AAS meta-model types and validation
* **js-yaml** for parsing infrastructure configuration
* **ApexCharts** for time-series and analytical visualizations
* **web-ifc** for IFC-based 3D model visualization

## High-Level Project Structure

At a high level, the repository is structured into:

* **Application source code** (`aas-web-ui/src/`)
* **Static assets and runtime configuration** (`public/`)
* **Documentation and examples** (`Docs/`, `examples/`)
* **Build, test, and deployment tooling** (Docker, Vite, CI workflows)

The `src/` directory is the primary focus for developers extending or maintaining the UI.

## Application Layers

### Pages and Modules

Pages define the top-level views of the application and are directly connected to routing. Core pages (located in `src/pages/`) handle generic AAS and submodel interaction, such as viewing or editing shells and submodels.

Extension modules are located under `src/pages/modules/` and are automatically registered as routes. A module typically:

* Represents a self-contained functional area
* Contributes one or more routes (always one base route)
* Reuses shared components, stores, and composables

Modules are the preferred extension mechanism for larger, application-level features.

### Component Layer

The component layer provides reusable UI building blocks. All components in the `src/components/` directory are globally registered and don't have to be imported individually when used. The component layer is divided into:

* **Generic UI components** (navigation, layout, widgets)
* **AAS-aware components** (submodel trees, element visualizations)
* **Editor components** for modifying AAS and submodel data

Submodel element renderers are organized by AAS element type, ensuring that the UI structure mirrors the AAS meta-model.

### Plugins

Plugins encapsulate domain-specific visualizations for particular submodel semantics. Plugins are located in the `src/components/plugins/` directory and divided by type (Submodel-, SubmodelElement-Plugins). They:

* Are bound to one or more semantic IDs
* Are selected automatically at runtime
* Operate within the context of existing pages and modules

This plugin mechanism allows domain experts to extend the UI without modifying core components or application logic.

### Composables (Business and Integration Logic)

Reusable logic is implemented using Vue composables and grouped by responsibility:

* **AAS composables**: handling shells, submodels, and submodel elements
* **Client composables**: typed access to BaSyx backend components
* **Infrastructure composables**: configuration loading, persistence, and authentication

Composables form the main abstraction layer between UI components and backend services.

### Utils (Helper Functions)

Utility functions provide low-level helpers for common tasks such as data formatting, validation, and transformation. They are stateless and can be used across all layers of the application.

### State Management

Global and shared state is managed using Pinia stores. Stores:

* Hold selected AAS and submodel data
* Manage infrastructure connections and authentication state
* Persist UI preferences and environment settings

Components and composables interact with stores reactively, ensuring consistent state propagation across the application.

## Data Flow

### Infrastructure Configuration Flow

At startup, the application loads its infrastructure configuration:

1. Static configuration is fetched from `public/config/`
2. YAML configuration is parsed and validated
3. Stored user configuration is merged from `localStorage`
4. The resulting configuration is exposed via the Infrastructure Store

This enables multi-infrastructure setups and runtime reconfiguration without rebuilding the UI.

### AAS Data Flow

A typical AAS interaction follows this pattern:

1. User interaction in a page or component
2. Invocation of an AAS-related composable
3. Delegation to a client composable for HTTP communication
4. Storage of results in a Pinia store
5. Reactive UI updates based on store state

This flow enforces a clear separation between UI rendering and backend integration logic.

## Routing and Navigation

Routing is configured centrally and consists of:

* **Static routes** for core pages
* **Dynamically generated routes** for modules
* **Route guards** for authentication and data preloading

Route parameters and query parameters are used to preserve application state and enable deep linking.

## Build and Deployment Architecture

The Web UI is built as a static web application:

* Development builds use Vite with hot module replacement
* Production builds generate optimized static assets
* Docker images serve the UI via NGINX

Runtime configuration is injected via configuration files and environment variables during container startup, keeping builds environment-agnostic.

## Security Architecture

Security concerns are handled centrally:

* Authentication is infrastructure-specific and configurable (OAuth2, Basic, Bearer, none)
* Tokens are managed by the Infrastructure Store
* API requests automatically attach authentication headers

```{warning}
The UI relies on proper CORS configuration of backend services to enable browser-based communication.
```

```{danger}
OAuth2 authentication also allows for the usage of the client credentials flow for machine-to-machine communication scenarios. This should only be used in trusted environments, as the client secret must be stored in the frontend application. It is exposed to end users and can be easily extracted from the local storage or the infrastructure configuration.
```

## Extensibility Summary

From an architectural perspective, the Web UI supports extensibility at multiple levels:

* **Configuration**: runtime infrastructure and authentication setup
* **Plugins**: submodel-specific visualization and interaction
* **Modules**: application-level features and workflows

This layered extensibility is a key design goal and underpins the long-term maintainability of the BaSyx AAS Web UI.
