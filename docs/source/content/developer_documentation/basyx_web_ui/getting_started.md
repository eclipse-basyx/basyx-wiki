# Getting Started with Development

This section describes how to set up a local development environment for the **BaSyx AAS Web UI**, run the application in development mode, and connect it to a BaSyx backend infrastructure.

The instructions below are intended for contributors and extension developers. If you only want to use the Web UI, please refer to the user-facing documentation instead.

## Prerequisites

### Required

* **Node.js**: version **20 LTS or newer**
  * Node.js **24 (current LTS)** is recommended
* **Yarn** package manager (lockfile-based installation is required)
* **Git**

The repository commits lockfiles. Please do not switch package managers.

## Repository Setup

### Fork and Clone

The BaSyx AAS Web UI is an Eclipse project. Contributions require:

* Forking the repository
* Signing the Eclipse Contributor Agreement (ECA)

Please refer to the official contribution guide before starting:

* [Contributing Guide](../../introduction/contributing.md)

Clone your fork locally:

```bash
git clone https://github.com/eclipse-basyx/basyx-aas-web-ui.git
cd basyx-aas-web-ui
```

## Bootstrap Script (Recommended)

The recommended way to start development is using the provided bootstrap script from the repository root:

```bash
. ./bootstrap.sh
```

The script interactively guides you through optional steps such as:

* Installing dependencies
* Starting the development server
* Building a Docker image

For most developers, this is preferred over manually navigating into `aas-web-ui/` and running Yarn commands.

## Manual Setup (Alternative)

If you prefer a manual setup, you can work directly in the application directory:

```bash
cd aas-web-ui
yarn
yarn dev
```

This starts the Vite development server with hot module replacement enabled.

## Development Scripts

The following scripts are defined in `aas-web-ui/package.json`:

* `yarn dev` – start development server
* `yarn build` – production build
* `yarn preview` – preview production build locally
* `yarn lint:check` – run ESLint checks
* `yarn lint:fix` – fix linting and formatting issues
* `yarn test` – run unit tests
* `yarn test:watch` – run tests in watch mode
* `yarn test:coverage` – generate test coverage
* `yarn test:ui` – run Vitest UI

Before a production build, the following checks are executed automatically:

* ESLint
* Unit tests
* TypeScript type checking (vue-tsc)

The same checks are enforced in CI.

```{hint}
It is strongly recommended to run `yarn lint:fix` before opening a pull request. The lint configuration includes Prettier and helps catch issues locally before CI runs.
```

## Configuration in Development Mode

### Infrastructure Configuration (YAML)

In development mode, the Web UI is configured using:

* `public/config/basyx-infra.yml`

This file:

* Defines one or more BaSyx infrastructures
* Configures component endpoints
* Specifies authentication methods

The file name is currently fixed and must not be changed.

Changes to this file should not be committed when working on local setups.

### Environment Configuration

Additional development configuration is done via:

* `env.development`

Environment variables are used for aspects not covered by the infrastructure YAML, for example:

* UI branding / corporate design
* Feature flags
* Build-time behavior

Legacy environment variables for infrastructure configuration are still supported, but **YAML-based configuration is recommended** for new setups.

### Local Overrides

During development, configuration can be adjusted via:

* Editing `basyx-infra.yml`
* Editing `env.development`
* Modifying infrastructure entries via the UI (stored in localStorage)

This allows experimentation without rebuilding the application.0

## Backend Infrastructure Requirements

For a fully functional development setup, it is recommended to have the following BaSyx components running:

* AAS Registry
* Submodel Registry
* AAS Repository
* Submodel Repository
* Concept Description Repository
* AAS Discovery Service

A complete setup can be obtained via the BaSyx Starter Kit:

* [https://basyx.org/](https://basyx.org/)

### Example Infrastructures

The repository contains ready-to-use examples:

* `examples/MultiInfrastructure/`

  Starts two BaSyx infrastructures in parallel (e.g. with and without authentication). This setup is particularly useful for testing multi-infrastructure handling and authentication features.

## Authentication During Development

Most development scenarios use **no authentication** for simplicity.

However, when working on:

* Authentication features
* Infrastructure handling
* Security-related UI behavior

it is recommended to enable OAuth2 in the backend and configure it in `basyx-infra.yml`.

## CORS Considerations

The Web UI is a browser-based application and requires proper **CORS configuration** on backend services.

The recommended approach is:

* Configure CORS directly on BaSyx backend components

If backend configuration is not possible (e.g. in restricted environments), alternatives include:

* Using a reverse proxy
* Using a development proxy via Vite

```{note}
Please note that these approaches are workarounds and should not be used in production environments.
```

## IDE Recommendations

For Visual Studio Code, the following extensions are recommended:

* ESLint
* Vue (Official)
* Prettier
* Prettier ESLint
* Jest (for test support)

The project is configured to take advantage of these tools.

## Docker-Based Development

The Web UI can also be built and run using Docker.

### Build Image

```bash
docker build -t basyx-aas-web-ui ./aas-web-ui
```

### Run Container

```bash
docker run -p 8080:80 \
  -v $(pwd)/aas-web-ui/public/config/basyx-infra.yml:/usr/share/nginx/html/config/basyx-infra.yml \
  basyx-aas-web-ui
```

The container-based setup closely mirrors production deployments and is useful for validating configuration and runtime behavior.

## Next Steps

After setting up your development environment, continue with:

* [Design Guidelines](design_guidelines.md)
* [Creating Submodel Plugins](creating_submodel_plugins.md)
* [Developing Custom Modules](developing_custom_modules.md)
