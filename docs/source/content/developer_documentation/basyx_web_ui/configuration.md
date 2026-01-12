# Configuration & Environment

This section explains how the **BaSyx AAS Web UI** is configured in development and production environments. It describes the different configuration layers, their precedence, and how they interact at runtime.

Understanding this configuration model is essential when running the UI in complex infrastructures, multi-environment setups, or secured deployments.

## Configuration Layers and Precedence

The Web UI supports multiple configuration mechanisms that are intentionally layered to maintain backward compatibility and runtime flexibility.

The effective precedence (highest first) is:

1. Infrastructure configuration stored in `localStorage`
(only if `ENDPOINT_CONFIG_AVAILABLE=true`)
2. Legacy infrastructure environment variables
(kept for backward compatibility)
3. Environment variables
    * env.development in development mode
    * Docker-injected environment variables in production
4. `public/config/basyx-infra.yml`
5. Application defaults

```{note}
Legacy infrastructure-related environment variables intentionally have higher precedence than the YAML configuration to avoid breaking existing deployments.
```

## Infrastructure Configuration

The primary and recommended way to configure backend infrastructures is the YAML file:

```bash
public/config/basyx-infra.yml
```

This file defines:

* One or more AAS infrastructures
* Component endpoints (registry, repository, discovery, etc.)
* Authentication configuration per infrastructure

### Characteristics

* The file name is currently fixed and cannot be changed
* It is loaded at runtime, not build time
* It supports multi-infrastructure setups

```{warning}
Changes made via the UI infrastructure editor are stored in `localStorage` only and are **not written back** to `basyx-infra.yml`.
```

## Environment Variables

Environment variables are used for **build-agnostic configuration** such as branding, feature flags, authentication toggles, and (for legacy reasons) infrastructure endpoints.

### Development Mode

In development mode:

* Configuration is read from `env.development`
* Variables must be prefixed with `VITE_`
* Values are injected by Vite at runtime

### Production Mode

In production:

* Environment variables are injected via Docker
* Variables are **not prefixed** with `VITE_`
* The `entrypoint.sh` script replaces placeholders at container startup

```{hint}
The same configuration keys are used in development and production. Only the prefix handling differs.
```

## Supported Environment Variables

### General

* `BASE` – application base path (runtime replaced) (**only available in dev mode!**, use `BASE_PATH` in production)
* `VITE_LOGO_LIGHT_PATH`
* `VITE_LOGO_DARK_PATH`
* `VITE_PRIMARY_LIGHT_COLOR`
* `VITE_PRIMARY_DARK_COLOR`

### Infrastructure (Legacy – Deprecated)

The following variables are deprecated in favor of `basyx-infra.yml`, but still supported:

* `VITE_AAS_DISCOVERY_PATH`
* `VITE_AAS_REGISTRY_PATH`
* `VITE_SUBMODEL_REGISTRY_PATH`
* `VITE_AAS_REPO_PATH`
* `VITE_SUBMODEL_REPO_PATH`
* `VITE_CD_REPO_PATH`

```{warning}
These variables remain available to avoid breaking existing deployments but should not be used for new setups.
```

### Authentication & Security

* `VITE_KEYCLOAK_ACTIVE` (**deprecated**; automatically set in production if Keycloak variables are present)
* `VITE_KEYCLOAK_URL` (**deprecated**; use `basyx-infra.yml` instead)
* `VITE_KEYCLOAK_REALM` (**deprecated**; use `basyx-infra.yml` instead)
* `VITE_KEYCLOAK_CLIENT_ID` (**deprecated**; use `basyx-infra.yml` instead)
* `VITE_KEYCLOAK_FEATURE_CONTROL`
* `VITE_KEYCLOAK_FEATURE_CONTROL_ROLE_PREFIX`
* `VITE_OIDC_ACTIVE` (**deprecated**; automatically set in production if OIDC variables are present)
* `VITE_OIDC_URL` (**deprecated**; use `basyx-infra.yml` instead)
* `VITE_OIDC_SCOPE` (**deprecated**; use `basyx-infra.yml` instead)
* `VITE_OIDC_CLIENT_ID` (**deprecated**; use `basyx-infra.yml` instead)
* `VITE_PRECONFIGURED_AUTH` (**deprecated**; use `basyx-infra.yml` instead with `client_Credentials` flow)
* `VITE_PRECONFIGURED_AUTH_CLIENT_SECRET` (**deprecated**; use `basyx-infra.yml` instead with `client_Credentials` flow)
* `VITE_BASIC_AUTH_ACTIVE` (**deprecated**; automatically set in production if basic auth variables are present)
* `VITE_BASIC_AUTH_USERNAME` (**deprecated**; use `basyx-infra.yml` instead)
* `VITE_BASIC_AUTH_PASSWORD` (**deprecated**; use `basyx-infra.yml` instead)
* `VITE_AUTHORIZATION_HEADER_PREFIX` (**deprecated**; use `basyx-infra.yml` instead)
* `VITE_AUTHORIZATION_HEADER_DESCRIPTION_ENDPOINT_EXEMPTION`

```{danger}
Never commit OAuth client secrets or credentials into version control. Frontend applications expose configuration to end users and secrets can be extracted easily.
```

### Feature Flags & Behavior

* `VITE_ENDPOINT_CONFIG_AVAILABLE`
* `VITE_SINGLE_AAS`
* `VITE_SINGLE_AAS_REDIRECT`
* `VITE_SM_VIEWER_EDITOR`
* `VITE_ALLOW_EDITING`
* `VITE_ALLOW_UPLOADING`
* `VITE_ALLOW_LOGOUT`

### Miscellaneous

* `VITE_INFLUXDB_TOKEN`
* `VITE_EDITOR_ID_PREFIX`

## Base Path Configuration

The Web UI supports deployment under a custom base path (e.g. `/basyx-ui/`).

* Controlled via the `BASE` environment variable
* Replaced at runtime by `entrypoint.sh` in production (`BASE_PATH`)

This affects:

* Routing
* Static asset resolution
* Mounted configuration files (e.g. `basyx-infra.yml`, logos)

```{hint}
When deploying under a non-root base path, all mounted static files must be available under the same base path.
```

## Infrastructure Editing via UI

If enabled, the Web UI allows users to edit infrastructure configurations directly.

* Controlled by `ENDPOINT_CONFIG_AVAILABLE=true`
* Enabled by default in development and production

Edits:

* Are stored in `localStorage`
* Override YAML and environment configuration
* Are local to the browser instance

```{note}
Infrastructure editing does not modify backend configuration or YAML files.
```

## Docker and Runtime Injection

In containerized deployments:

* Configuration is injected via environment variables
* `entrypoint.sh` performs:
  * Base path replacement
  * Environment variable injection into Pinia stores
  * Configuration file placement

This allows the same image to be reused across environments without rebuilding.

## Development vs Production Summary

| **Aspect** | **Development** | **Production** |
|------------|-----------------|----------------|
| Env vars | `env.development` (`VITE_*`) | Docker env vars |
| Infra config | `basyx-infra.yml` | `basyx-infra.yml` |
| Overrides | localStorage | localStorage |
| Base path | runtime | runtime |

## Common Pitfalls

* Committing local changes to `basyx-infra.yml`
* Assuming UI-edited infrastructure is persisted globally
* Using OAuth client secrets in frontend configuration
* Forgetting to adjust mounted paths when changing `BASE`/`BASE_PATH`

## Introducing new Environment Variables

When introducing new environment variables, the following files need to be updated accordingly:

* `env.development` – for development mode (including dev defaults)
* `entrypoint.sh` – for production mode (including prod defaults)
* `src/store/EnvironmentStore.ts` – to define placeholders that will be replaced at runtime (including application defaults)

## Next Steps

* [Design Guidelines](design_guidelines.md)
* [Creating Submodel Plugins](creating_submodel_plugins.md)
* [Developing Custom Modules](developing_custom_modules.md)
