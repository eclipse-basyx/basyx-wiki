# Configuration & Environment

> **As a** BaSyx AAS Web UI user  
> **I want to** configure the Web UI to connect to my AAS infrastructure  
> **so that** I can access and interact with my Asset Administration Shells.

## Feature Overview

The BaSyx AAS Web UI provides flexible configuration options to connect to different AAS infrastructures and customize the application behavior. Configuration can be done through multiple mechanisms, depending on your deployment scenario.

## Configuring Backend Connections

To connect the Web UI to your AAS infrastructure, you need to configure the endpoints for the various BaSyx components.

### Using the UI Settings Panel

The easiest way to configure backend connections is through the Web UI itself:

1. Click on the **gear icon** in the top right corner of the Web UI
2. In the settings panel, select the **Infrastructure** tab
3. Either:
   - Select an existing infrastructure configuration from the dropdown, or
   - Click **Add Infrastructure** to create a new connection
4. Provide the endpoints for the following components:
   - **AAS Registry** (required for discovering AAS)
   - **Submodel Registry** (required for discovering Submodels)
   - **AAS Repository** (required for accessing AAS data)
   - **Submodel Repository** (required for accessing Submodel data)
   - **Concept Description Repository** (required for semantic information)
   - **AAS Discovery Service** (optional, for discovering AAS by asset IDs)

```{figure} ./images/connect_to_aas_infrastructure.png
---
width: 80%
alt: Connect to AAS Infrastructure
name: infrastructure_config
---
Configuring Infrastructure Connections
```

```{note}
Changes made through the UI settings are stored in your browser's local storage and will persist across sessions on the same device.
```

### Using Configuration Files

For production deployments or when you want to pre-configure the Web UI for multiple users, you can use the YAML configuration file:

**Location:** `public/config/basyx-infra.yml`

This file allows you to:
- Define multiple infrastructure configurations
- Set default connections
- Configure authentication settings per infrastructure

```{hint}
Changes made via the UI infrastructure editor are **not** written back to the YAML file. The YAML file serves as the initial/default configuration.
```

### Using Docker Environment Variables

When running the Web UI in a Docker container, you can configure it using environment variables. This is particularly useful for automated deployments and CI/CD pipelines.

```{seealso}
For details on Docker-specific configuration options, see the [Docker Configuration](./docker_config.md) page.
```

## Configuration Precedence

The Web UI supports multiple configuration sources with the following precedence (highest first):

1. **Browser Local Storage** (configurations made through the UI settings panel)
2. **Docker Environment Variables** (when running in a container)
3. **Configuration File** (`basyx-infra.yml`)
4. **Application Defaults**

This layered approach allows you to provide default configurations while still enabling users to customize their settings as needed.

## Advanced Configuration Options

Beyond basic backend connections, the Web UI supports various advanced configuration options:

- **Authentication and Authorization**: Configure OAuth, RBAC, and other security settings
- **Feature Flags**: Enable or disable specific features based on your requirements
- **Corporate Design**: Customize colors, logos, and branding elements
- **Performance Tuning**: Adjust data fetching intervals and cache settings

```{seealso}
For comprehensive technical details on all configuration options, including advanced scenarios and multi-environment setups, refer to the [Configuration & Environment](../../../../developer_documentation/basyx_web_ui/configuration.md) page in the developer documentation.
```

## Connecting to Different Environments

The flexible configuration system makes it easy to switch between different environments:

- **Development**: Connect to local BaSyx instances running on your development machine
- **Testing**: Connect to shared test infrastructure
- **Production**: Connect to production AAS repositories and registries

You can save multiple infrastructure configurations and quickly switch between them using the infrastructure dropdown in the settings panel.

## Troubleshooting Connection Issues

If you're having trouble connecting to your AAS infrastructure:

1. **Verify Endpoints**: Ensure all URLs are correct and accessible from your browser
2. **Check CORS Settings**: Make sure the backend services allow requests from the Web UI's origin
3. **Review Authentication**: Verify that authentication tokens or credentials are properly configured
4. **Inspect Browser Console**: Check for error messages that might indicate connection problems

```{seealso}
For status monitoring and error notifications, see the [Status Check and Error Notifications](./statuscheck.md) feature page.
```
