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
* `VITE_START_PAGE_ROUTE_NAME`

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

## Start Page Configuration

The Web UI supports configuring which page is shown when the application is first loaded.

* Controlled via the `VITE_START_PAGE_ROUTE_NAME` environment variable (`START_PAGE_ROUTE_NAME` in production)
* The value must be a valid **named route** defined in the application router (e.g. `AASViewer`, `AASEditor`, `SubmodelViewer`)
* Validated at startup: the configured route must exist, its associated feature flag must be enabled, and the corresponding module must be visible
* If the value is invalid or the route is not accessible, the application falls back to the default start page
* After authentication, the application automatically redirects to the configured start page

```{note}
The main viewer route has moved from `/` to `/aasviewer`. Navigating to `/` now shows a 404 page unless an explicit start page redirect is configured. The default start page route is `AASViewer`.
```

### Behavior

* On initial load: the root path (`/`) redirects to the resolved start page route
* After authentication: the user is redirected to the configured start page
* Invalid route names: fall back to the application default
* Feature flag gating: if the target route's feature flag is disabled, the fallback is used

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
* Setting `START_PAGE_ROUTE_NAME` to a route whose feature flag is disabled (the app will fall back silently)
* Using a path (e.g. `/aasviewer`) instead of a named route (e.g. `AASViewer`) for `START_PAGE_ROUTE_NAME`

## YAML Infrastructure Configuration

The primary and recommended method for configuring infrastructure connections is through the `basyx-infra.yml` file. This section provides comprehensive technical details for system administrators and developers.

### File Locations

* **Development Mode**: `/aas-web-ui/public/config/basyx-infra.yml`
* **Production Mode (Docker)**: Mount to `/basyx-infra.yml` in the container

The configuration file is copied to the application's config directory at container startup and parsed client-side by the browser using the `js-yaml` library.

### Basic Structure

```yaml
infrastructures:
  default: <default-infra-key>

  <infra-key>:
    name: <infrastructure-name>
    components:
      aasDiscovery:
        baseUrl: "<url>"
      aasRegistry:
        baseUrl: "<url>"
      submodelRegistry:
        baseUrl: "<url>"
      aasRepository:
        baseUrl: "<url>"
      submodelRepository:
        baseUrl: "<url>"
      conceptDescriptionRepository:
        baseUrl: "<url>"
    security:
      type: <auth-type>
      config:
        # Authentication-specific configuration
```

### Configuration Examples

#### No Authentication

```yaml
infrastructures:
  default: local

  local:
    name: Local Development Environment
    components:
      aasRegistry:
        baseUrl: "http://localhost:9082"
      submodelRegistry:
        baseUrl: "http://localhost:9083"
      aasRepository:
        baseUrl: "http://localhost:9081"
      submodelRepository:
        baseUrl: "http://localhost:9081"
      conceptDescriptionRepository:
        baseUrl: "http://localhost:9081"
      aasDiscovery:
        baseUrl: "http://localhost:9084"
    security:
      type: none
```

#### OAuth2 Authorization Code Flow

```yaml
infrastructures:
  default: production

  production:
    name: Production Environment
    components:
      aasRegistry:
        baseUrl: "https://aasreg.basyx.example.com"
      submodelRegistry:
        baseUrl: "https://smreg.basyx.example.com"
      aasRepository:
        baseUrl: "https://aasenv.basyx.example.com"
      submodelRepository:
        baseUrl: "https://aasenv.basyx.example.com"
      conceptDescriptionRepository:
        baseUrl: "https://aasenv.basyx.example.com"
      aasDiscovery:
        baseUrl: "https://discovery.basyx.example.com"
    security:
      type: oauth2
      config:
        flow: auth_code
        issuer: "https://keycloak.example.com/auth/realms/BaSyx"
        clientId: "basyx-web-ui"
        scope: "openid profile email"
```

#### OAuth2 Client Credentials Flow

```{danger}
Client Credentials Flow exposes the client secret in the browser. Only use for internal/trusted environments.
```

```yaml
infrastructures:
  default: service

  service:
    name: Service Account Environment
    components:
      aasRegistry:
        baseUrl: "https://aasreg.internal.basyx.com"
      submodelRegistry:
        baseUrl: "https://smreg.internal.basyx.com"
      aasRepository:
        baseUrl: "https://aasenv.internal.basyx.com"
      submodelRepository:
        baseUrl: "https://aasenv.internal.basyx.com"
      conceptDescriptionRepository:
        baseUrl: "https://aasenv.internal.basyx.com"
    security:
      type: oauth2
      config:
        flow: client_credentials
        issuer: "https://keycloak.internal.basyx.com/auth/realms/BaSyx"
        clientId: "basyx-service-client"
        clientSecret: "your-client-secret-here"
        scope: ""
```

#### Basic Authentication

```yaml
infrastructures:
  default: staging

  staging:
    name: Staging Environment
    components:
      aasRegistry:
        baseUrl: "https://aasreg.staging.basyx.com"
      submodelRegistry:
        baseUrl: "https://smreg.staging.basyx.com"
      aasRepository:
        baseUrl: "https://aasenv.staging.basyx.com"
      submodelRepository:
        baseUrl: "https://aasenv.staging.basyx.com"
      conceptDescriptionRepository:
        baseUrl: "https://aasenv.staging.basyx.com"
    security:
      type: basic
      config:
        username: "admin"
        password: "admin123"
```

#### Bearer Token Authentication

```yaml
infrastructures:
  default: test

  test:
    name: Test Environment
    components:
      aasRegistry:
        baseUrl: "https://aasreg.test.basyx.com"
      submodelRegistry:
        baseUrl: "https://smreg.test.basyx.com"
      aasRepository:
        baseUrl: "https://aasenv.test.basyx.com"
      submodelRepository:
        baseUrl: "https://aasenv.test.basyx.com"
      conceptDescriptionRepository:
        baseUrl: "https://aasenv.test.basyx.com"
    security:
      type: bearer
      config:
        token: "your-bearer-token-here"
```

#### Multiple Infrastructures

```yaml
infrastructures:
  default: production

  production:
    name: Production Environment
    components:
      # ... production components
    security:
      type: oauth2
      config:
        flow: auth_code
        issuer: "https://auth.prod.example.com/realms/basyx"
        clientId: "basyx-web-ui"
        scope: "openid profile email"

  development:
    name: Development Environment
    components:
      # ... development components
    security:
      type: none

  partner-a:
    name: Partner A Infrastructure
    components:
      # ... partner A components
    security:
      type: oauth2
      config:
        flow: auth_code
        issuer: "https://auth.partner-a.com/realms/basyx"
        clientId: "basyx-integration"
        scope: "openid"
```

### Docker Deployment

#### Mounting the Configuration File

```yaml
services:
  aas-web-ui:
    image: eclipsebasyx/aas-gui:latest
    ports:
      - '3000:3000'
    volumes:
      - ./basyx-infra.yml:/basyx-infra.yml:ro
    environment:
      # Control whether users can edit infrastructures
      ENDPOINT_CONFIG_AVAILABLE: "false"  # Locked mode
```

#### Configuration Precedence

Environment variables take precedence over YAML for backward compatibility:

1. **Environment Variables** (highest): If any infrastructure-related env vars are set (e.g., `AAS_REGISTRY_PATH`, `KEYCLOAK_URL`), the YAML file is ignored
2. **YAML Configuration**: Only used when no env vars are configured
3. **User Edits (localStorage)**: User modifications in the UI (if `ENDPOINT_CONFIG_AVAILABLE=true`)

#### Configuration Locking

Control user ability to modify infrastructures with `ENDPOINT_CONFIG_AVAILABLE`:

* **`false`** (Locked Mode):
  - Configuration source (env vars or YAML) takes full precedence
  - Users cannot add or edit infrastructures
  - Recommended for production

* **`true`** (Editable Mode - Default):
  - Configurations from source are loaded as templates
  - Users can edit and create infrastructures
  - Changes stored in browser localStorage
  - Recommended for development

### Security Configuration Reference

#### Authentication Types

The `security.type` field accepts:

* **`none`**: No authentication
* **`oauth2`**: OAuth2/OIDC authentication
* **`basic`**: HTTP Basic authentication
* **`bearer`**: Bearer token authentication

#### OAuth2 Fields

**Common Fields (Both Flows):**

* `flow` (required): `auth_code` or `client_credentials`
* `issuer` (required): OAuth2 authorization server URL
* `clientId` (required): Client identifier
* `scope` (optional): Space-separated OAuth2 scopes (default: `""`)

**Client Credentials Flow Only:**

* `clientSecret` (required): Client secret for authentication

```{warning}
Client secrets in YAML files are visible in the browser. Never use client credentials flow in production environments with external access.
```

#### Basic Authentication Fields

* `username` (required): Username for authentication
* `password` (required): Password for authentication

#### Bearer Token Fields

* `token` (required): Bearer token string

### Implementation Details

#### Infrastructure IDs

* YAML-based: `yaml_<yamlKey>` (stable across reloads)
* User-created: `infra_<timestamp>` (unique per creation)

#### YAML to Internal Format Mapping

* YAML `baseUrl` → Internal `url`
* YAML field names match internal store structure
* Security types map: `none` → `No Authentication`, `oauth2` → `OAuth2`, etc.

#### Loading Process

1. **Container Startup** (`entrypoint.sh`):
   ```bash
   if [ -f "/basyx-infra.yml" ]; then
     cp /basyx-infra.yml /usr/src/app/dist/config/basyx-infra.yml
   fi
   ```

2. **Application Startup** (`useInfrastructureConfigLoader`):
   - Determine base path (dev: `import.meta.env.BASE_URL`, prod: `envStore.getEnvBasePath`)
   - Fetch from `${basePath}/config/basyx-infra.yml`
   - Return null if file doesn't exist (404)

3. **YAML Parsing** (`useInfrastructureYamlParser`):
   - Convert YAML structure to internal format
   - Transform `baseUrl` to `url` for each component
   - Map security types to internal enums
   - Generate infrastructure IDs: `yaml_<yamlKey>`

4. **Configuration Merging** (`useInfrastructureStorage`):
   - Check if environment variables are configured
   - Load YAML file and parse infrastructures
   - Merge with localStorage based on `ENDPOINT_CONFIG_AVAILABLE`
   - Authenticate client credentials flows automatically

#### OAuth2 Client Credentials Auto-Authentication

When `client_credentials` flow is detected:
* Application automatically authenticates on load
* Token refresh handled automatically
* No user interaction required

### Best Practices

1. **Use YAML for Production**: Avoid deprecated environment variables for infrastructure config
2. **Lock Configuration**: Set `ENDPOINT_CONFIG_AVAILABLE=false` in production
3. **Secure Secrets**: Never use client credentials flow with external access
4. **Multiple Infrastructures**: Define all environments in one YAML file
5. **Default Infrastructure**: Always set a sensible `default` key
6. **Version Control**: Commit YAML templates, not files with real credentials
7. **Read-Only Mount**: Mount YAML files as read-only (`:ro`) in Docker

## Introducing new Environment Variables

When introducing new environment variables, the following files need to be updated accordingly:

* `env.development` – for development mode (including dev defaults)
* `entrypoint.sh` – for production mode (including prod defaults)
* `src/store/EnvironmentStore.ts` – to define placeholders that will be replaced at runtime (including application defaults)

## Next Steps

* [Design Guidelines](design_guidelines.md)
* [Creating Submodel Plugins](creating_submodel_plugins.md)
* [Developing Custom Modules](developing_custom_modules.md)
