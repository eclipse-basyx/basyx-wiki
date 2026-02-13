# Docker Configuration

> **As a** BaSyx AAS Web UI user  
> **I want to** deploy and configure the AAS Web UI using Docker  
> **so that** I can easily run it in containerized environments with proper configuration.

## Feature Overview

The BaSyx AAS Web UI is distributed as a Docker image that can be easily deployed and configured through environment variables and volume mounts. This page focuses on Docker-specific setup, including how to run the container, configure it through environment variables, and mount custom resources.

## Quick Start with Docker

### Pull the Image

The AAS Web UI can be pulled from [Docker Hub](https://hub.docker.com/r/eclipsebasyx/aas-gui):

```bash
docker pull eclipsebasyx/aas-gui
```

### Run the Container

Start the AAS Web UI with basic configuration:

```bash
docker run -p 3000:3000 --name=aas-web-ui eclipsebasyx/aas-gui
```

The Web UI will be accessible at [http://localhost:3000](http://localhost:3000).

## Configuration Through Environment Variables

Environment variables allow you to configure the Web UI's behavior, appearance, and feature availability at container startup.

### Setting Environment Variables

**Using Docker Run:**

```bash
docker run -p 3000:3000 --name=aas-web-ui \
  -e BASE_PATH="/basyx-ui" \
  -e ALLOW_EDITING="false" \
  -e PRIMARY_LIGHT_COLOR="#0066cc" \
  eclipsebasyx/aas-gui
```

**Using Docker Compose:**

Create a `docker-compose.yml` file:

```yaml
services:
  aas-web-ui:
    image: eclipsebasyx/aas-gui
    container_name: aas-web-ui
    ports:
      - "3000:3000"
    environment:
      BASE_PATH: "/"
      ALLOW_EDITING: "true"
      ALLOW_UPLOADING: "true"
      PRIMARY_LIGHT_COLOR: "#0cb2f0"
      PRIMARY_DARK_COLOR: "#f69222"
```

Then start the container:

```bash
docker-compose up -d
```

### Available Environment Variables

The following environment variables can be used to configure the AAS Web UI:

#### Branding and Appearance

| Variable Name | Description | Default |
|---------------|-------------|---------|
| PRIMARY_COLOR | The primary color of the AAS Web UI (legacy, use theme-specific colors instead) | - |
| PRIMARY_LIGHT_COLOR | The primary color for the light theme | "#0cb2f0" |
| PRIMARY_DARK_COLOR | The primary color for the dark theme | "#f69222" |
| LOGO_PATH | The path to the application logo inside the container `<your-logo.png>` | - |
| LOGO_LIGHT_PATH | The path to the logo for the light theme | "Logo_light.svg" |
| LOGO_DARK_PATH | The path to the logo for the dark theme | "Logo_dark.svg" |

```{seealso}
For more details on customizing branding, see the [Corporate Design](./corporate_design.md) page.
```

#### Application Behavior

| Variable Name | Description | Default |
|---------------|-------------|---------|
| BASE_PATH | The base path where the AAS Web UI is deployed (e.g., "/basyx-ui") | "/" |
| ENDPOINT_CONFIG_AVAILABLE | Allow users to create/edit infrastructure configurations | true |
| SINGLE_AAS | Show only one specific AAS instead of a list | false |
| SINGLE_AAS_REDIRECT | Redirect URL when SINGLE_AAS is true and no `aas` query parameter is present | - |
| SM_VIEWER_EDITOR | Enable/disable the standalone Submodel Viewer and Editor | true |
| ALLOW_EDITING | Enable/disable the AAS Editor | true |
| ALLOW_UPLOADING | Enable/disable uploading AAS environments | true |
| ALLOW_LOGOUT | Enable/disable logout functionality when authentication is active | true |
| EDITOR_ID_PREFIX | Default prefix for AAS IDs and GlobalAssetIDs in the editor | "https://example.com/" |
| START_PAGE_ROUTE_NAME | The named route to use as the application's landing page (e.g. "AASViewer", "AASEditor") | "AASViewer" |

#### Integration Features

| Variable Name | Description | Default |
|---------------|-------------|---------|
| INFLUXDB_TOKEN | Token for accessing time series data from InfluxDB | - |

#### Deprecated Infrastructure Configuration Variables

```{warning}
The following environment variables are **deprecated** and maintained only for backward compatibility. For new deployments, use YAML-based infrastructure configuration or configure infrastructures through the Web UI.
```

| Variable Name | Description | Status |
|---------------|-------------|--------|
| AAS_DISCOVERY_PATH | Path to the AAS Discovery Service | ⚠️ Deprecated |
| AAS_REGISTRY_PATH | Path to the AAS Registry | ⚠️ Deprecated |
| SUBMODEL_REGISTRY_PATH | Path to the Submodel Registry | ⚠️ Deprecated |
| AAS_REPO_PATH | Path to the AAS Repository | ⚠️ Deprecated |
| SUBMODEL_REPO_PATH | Path to the Submodel Repository | ⚠️ Deprecated |
| CD_REPO_PATH | Path to the Concept Description Repository | ⚠️ Deprecated |

```{seealso}
For infrastructure configuration, see the [Configuration & Environment](./configuration.md) page.
```

#### Deprecated Authentication Variables

```{warning}
The following authentication-related environment variables are **deprecated**. Use YAML-based infrastructure configuration with per-infrastructure security settings instead.
```

| Variable Name | Description | Status |
|---------------|-------------|--------|
| KEYCLOAK_URL | URL of the Keycloak server | ⚠️ Deprecated |
| KEYCLOAK_REALM | Keycloak realm name | ⚠️ Deprecated |
| KEYCLOAK_CLIENT_ID | Keycloak client ID | ⚠️ Deprecated |
| PRECONFIGURED_AUTH_USERNAME | Preconfigured username for automatic sign-in | ⚠️ Deprecated |
| PRECONFIGURED_AUTH_PASSWORD | Preconfigured password for automatic sign-in | ⚠️ Deprecated |
| BASIC_AUTH_USERNAME | Username for basic authentication | ⚠️ Deprecated |
| BASIC_AUTH_PASSWORD | Password for basic authentication | ⚠️ Deprecated |

```{seealso}
For authentication and security configuration, see the [Security](./security.md) page.
```

## Mounting Custom Resources

### Custom Logos and Branding

You can mount your own logo files to customize the Web UI's appearance:

**Using Docker Run:**

```bash
docker run -p 3000:3000 --name=aas-web-ui \
  -v /path/to/your/logos:/usr/src/app/dist/Logo \
  -e LOGO_LIGHT_PATH="my-company-logo-light.png" \
  -e LOGO_DARK_PATH="my-company-logo-dark.png" \
  eclipsebasyx/aas-gui
```

**Using Docker Compose:**

```yaml
services:
  aas-web-ui:
    image: eclipsebasyx/aas-gui
    container_name: aas-web-ui
    ports:
      - "3000:3000"
    volumes:
      - ./logos:/usr/src/app/dist/Logo
    environment:
      LOGO_LIGHT_PATH: "my-company-logo-light.png"
      LOGO_DARK_PATH: "my-company-logo-dark.png"
```

```{tip}
Place your logo files (PNG or SVG recommended) in the local directory that you're mounting, and reference them using the `LOGO_LIGHT_PATH` and `LOGO_DARK_PATH` environment variables.
```

### Infrastructure Configuration File

For system administrators who want to pre-configure infrastructure connections, you can mount a YAML configuration file:

**Using Docker Run:**

```bash
docker run -p 3000:3000 --name=aas-web-ui \
  -v /path/to/basyx-infra.yml:/basyx-infra.yml \
  -e ENDPOINT_CONFIG_AVAILABLE="false" \
  eclipsebasyx/aas-gui
```

**Using Docker Compose:**

```yaml
services:
  aas-web-ui:
    image: eclipsebasyx/aas-gui
    container_name: aas-web-ui
    ports:
      - "3000:3000"
    volumes:
      - ./basyx-infra.yml:/basyx-infra.yml
    environment:
      ENDPOINT_CONFIG_AVAILABLE: "false"  # Lock configuration
```

```{seealso}
For detailed information on the YAML configuration file structure and advanced infrastructure setup, see the [Infrastructure Configuration](../../../../developer_documentation/basyx_web_ui/configuration.md#infrastructure-configuration) section in the developer documentation.
```

## Complete Docker Compose Examples

### Basic Deployment

A minimal deployment with default settings:

```yaml
services:
  aas-web-ui:
    image: eclipsebasyx/aas-gui
    container_name: aas-web-ui
    ports:
      - "3000:3000"
    restart: unless-stopped
```

### Customized Deployment with Branding

Deployment with custom branding and feature flags:

```yaml
services:
  aas-web-ui:
    image: eclipsebasyx/aas-gui
    container_name: aas-web-ui
    ports:
      - "3000:3000"
    volumes:
      - ./logos:/usr/src/app/dist/Logo
    environment:
      # Branding
      PRIMARY_LIGHT_COLOR: "#0066cc"
      PRIMARY_DARK_COLOR: "#ff6600"
      LOGO_LIGHT_PATH: "company-logo-light.svg"
      LOGO_DARK_PATH: "company-logo-dark.svg"
      
      # Feature Flags
      ALLOW_EDITING: "true"
      ALLOW_UPLOADING: "true"
      SM_VIEWER_EDITOR: "true"
      
      # Application Behavior
      EDITOR_ID_PREFIX: "https://example.com/ids/"
      START_PAGE_ROUTE_NAME: "AASEditor"
    restart: unless-stopped
```

### Production Deployment with Pre-configured Infrastructure

Deployment with locked infrastructure configuration:

```yaml
services:
  aas-web-ui:
    image: eclipsebasyx/aas-gui
    container_name: aas-web-ui
    ports:
      - "443:3000"  # Use reverse proxy for HTTPS
    volumes:
      - ./basyx-infra.yml:/basyx-infra.yml
      - ./logos:/usr/src/app/dist/Logo
    environment:
      # Lock infrastructure configuration
      ENDPOINT_CONFIG_AVAILABLE: "false"
      
      # Branding
      LOGO_LIGHT_PATH: "company-logo-light.svg"
      LOGO_DARK_PATH: "company-logo-dark.svg"
      PRIMARY_LIGHT_COLOR: "#0066cc"
      PRIMARY_DARK_COLOR: "#ff6600"
      
      # Feature control for production
      ALLOW_EDITING: "false"
      ALLOW_UPLOADING: "false"
    restart: unless-stopped
```

```{note}
In production, it's recommended to:
- Use a reverse proxy (nginx, traefik) for HTTPS termination
- Lock infrastructure configuration with `ENDPOINT_CONFIG_AVAILABLE=false`
- Carefully control editing and upload features based on your security requirements
- Use pre-configured YAML files for infrastructure connections
```

### Multi-Infrastructure Deployment

Example with YAML file for multiple infrastructures:

Create a `basyx-infra.yml` file (see developer documentation for detailed structure):

```yaml
infrastructures:
  default: production

  development:
    name: Development Environment
    components:
      aasRegistry:
        baseUrl: "http://dev-registry:8080"
      # ... other components
    security:
      type: none

  production:
    name: Production Environment
    components:
      aasRegistry:
        baseUrl: "https://prod-registry.example.com"
      # ... other components
    security:
      type: oauth2
      config:
        flow: auth_code
        issuer: "https://auth.example.com/realms/basyx"
        clientId: "basyx-web-ui"
```

Then reference it in your `docker-compose.yml`:

```yaml
services:
  aas-web-ui:
    image: eclipsebasyx/aas-gui
    container_name: aas-web-ui
    ports:
      - "3000:3000"
    volumes:
      - ./basyx-infra.yml:/basyx-infra.yml
    environment:
      ENDPOINT_CONFIG_AVAILABLE: "true"  # Allow switching between infras
    restart: unless-stopped
```

## Building from Source

If you need to build the Docker image yourself:

1. Clone the repository:
```bash
git clone https://github.com/eclipse-basyx/basyx-aas-web-ui.git
cd basyx-aas-web-ui
```

2. Build the Docker image:
```bash
docker build -t my-aas-web-ui .
```

```{note}
If you're behind a proxy, set the `HTTP_PROXY` and `HTTPS_PROXY` environment variables before building. See the [bootstrap.sh](https://github.com/eclipse-basyx/basyx-aas-web-ui/blob/main/bootstrap.sh) script for details.
```

3. Run your custom build:
```bash
docker run -p 3000:3000 --name=aas-web-ui my-aas-web-ui
```

## Troubleshooting Docker Deployments

### Container Won't Start

1. Check container logs:
```bash
docker logs aas-web-ui
```

2. Verify port availability:
```bash
# Check if port 3000 is already in use
netstat -an | grep 3000
```

3. Ensure proper image pull:
```bash
docker pull eclipsebasyx/aas-gui:latest
```

### Configuration Not Applied

1. Verify environment variables are set:
```bash
docker inspect aas-web-ui | grep -A 20 "Env"
```

2. Check mounted volumes:
```bash
docker inspect aas-web-ui | grep -A 10 "Mounts"
```

3. Restart the container after configuration changes:
```bash
docker restart aas-web-ui
```

### Custom Logo Not Showing

1. Verify the volume mount path is correct
2. Check that logo files exist in the mounted directory
3. Ensure `LOGO_LIGHT_PATH` and `LOGO_DARK_PATH` match the actual filenames
4. Check browser console for 404 errors on logo files

## Best Practices

1. **Use Docker Compose** for complex deployments with multiple services
2. **Mount YAML config files** for infrastructure pre-configuration rather than using deprecated environment variables
3. **Lock configuration in production** with `ENDPOINT_CONFIG_AVAILABLE=false`
4. **Use semantic versioning** for production deployments (e.g., `eclipsebasyx/aas-gui:v2-250417` instead of `latest`)
5. **Set restart policies** to ensure the container restarts automatically
6. **Use reverse proxy** for HTTPS in production
7. **Monitor container logs** for errors and warnings
8. **Keep images updated** to receive security patches and new features

## Next Steps

- **[Configuration & Environment](./configuration.md)**: Configure infrastructure connections
- **[Security](./security.md)**: Set up authentication and authorization
- **[Corporate Design](./corporate_design.md)**: Customize appearance and branding
- **[Developer Documentation](../../../../developer_documentation/basyx_web_ui/configuration.md)**: Advanced configuration options and YAML file structure
