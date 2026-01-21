# Configuration & Environment

> **As a** BaSyx AAS Web UI user  
> **I want to** configure the Web UI to connect to my AAS infrastructure  
> **so that** I can access and interact with my Asset Administration Shells.

## Feature Overview

The BaSyx AAS Web UI provides flexible configuration options to connect to different AAS infrastructures and customize the application behavior. You can configure the Web UI through the user interface itself, using environment variables, or by pre-configuring infrastructure connections for your users.

## Configuring Infrastructure Connections

The Web UI allows you to connect to one or multiple AAS infrastructures, each potentially using different authentication methods and component endpoints.

### Managing Infrastructures Through the UI

The most user-friendly way to configure backend connections is directly through the Web UI:

#### Viewing and Selecting Infrastructures

1. Click on the **gear icon** in the top right corner of the Web UI
2. You'll see a list of available infrastructure configurations to select from

```{figure} ./images/infrastructure_selector.png
---
width: 50%
alt: Infrastructure Selector
name: infrastructure_selector
---
Selecting an infrastructure from the dropdown
```

From this view, you can:

- **Switch between infrastructures** using the dropdown selector
- **View all configured infrastructures** in a list
- **Edit existing infrastructures** by clicking the edit icon
- **Delete infrastructures** you no longer need
- **Add new infrastructures** by clicking the "Add Infrastructure" button

```{figure} ./images/infrastructure_list.png
---
width: 80%
alt: Infrastructure List
name: infrastructure_list
---
List of available infrastructures with management actions
```

#### Creating or Editing an Infrastructure

When creating a new infrastructure or editing an existing one, you'll configure:

**Required Component Endpoints:**

- **AAS Registry**: For discovering Asset Administration Shell endpoints
- **Submodel Registry**: For discovering Submodel endpoints
- **AAS Repository**: For accessing AAS data
- **Submodel Repository**: For accessing Submodel data
- **Concept Description Repository**: For semantic information and concept descriptions

**Optional Component Endpoints:**

- **AAS Discovery Service**: For discovering AAS by asset IDs

**Security Configuration:**
See the [Security](./security.md) page for detailed information on authentication and authorization options.

```{figure} ./images/infrastructure_edit_form.png
---
width: 80%
alt: Infrastructure Configuration Form
name: infrastructure_config_form
---
Form for creating or editing an infrastructure configuration
```

```{note}
Infrastructure configurations created or modified through the UI are stored in your browser's local storage and will persist across sessions on the same device. However, they are not shared across different browsers or devices.
```

### Multiple Infrastructures Support

The BaSyx AAS Web UI supports connecting to **multiple AAS infrastructures** simultaneously. This is particularly useful when:

- Working with development, testing, and production environments
- Connecting to different organizational units with separate AAS infrastructures
- Integrating with partner organizations that use different identity providers
- Testing against multiple backend versions

Each infrastructure can have:

- Its own set of component endpoints (registries, repositories, discovery)
- Different authentication methods (OAuth2, Basic Auth, Bearer Token, or none)
- Different identity providers (Keycloak, Azure AD, Auth0, or any OAuth2-compatible IDP)

```{hint}
You can quickly switch between infrastructures using the selector in the settings panel without needing to reconfigure each time.
```

```{seealso}
For details on authentication and authorization for multiple infrastructures, see the [Security](./security.md) page.
```

## General Application Configuration

Beyond infrastructure connections, the Web UI can be configured through environment variables to customize its appearance and behavior.

### Branding and Corporate Design

- **Logo customization**: Set custom logos for light and dark themes
- **Color scheme**: Configure primary colors for your organization
- **Application theme**: Customize the overall look and feel

```{seealso}
For details on corporate design customization, see the [Corporate Design](./corporate_design.md) page.
```

### Feature Flags

Control which features are available in your deployment:

- **Editor mode**: Enable or disable the AAS Editor (`ALLOW_EDITING`)
- **File uploads**: Control whether users can upload AAS environments (`ALLOW_UPLOADING`)
- **Submodel Viewer**: Enable or disable the standalone Submodel Viewer (`SM_VIEWER_EDITOR`)
- **Logout functionality**: Control logout behavior when authentication is enabled (`ALLOW_LOGOUT`)

### Application Behavior

- **Base path**: Deploy the Web UI under a custom URL path (`BASE_PATH`)
- **Single AAS mode**: Configure the UI to display only one specific AAS (`SINGLE_AAS`)
- **Editor ID prefix**: Set a default prefix for AAS IDs created in the editor (`EDITOR_ID_PREFIX`)

```{seealso}
For a complete list of environment variables and how to set them in Docker, see the [Docker Configuration](./docker_config.md) page.
```

## System Administrator Setup

If you are a **system administrator** deploying the BaSyx AAS Web UI for multiple users, you can pre-configure infrastructure connections using a YAML configuration file. This allows you to:

- Define multiple infrastructures that all users can access
- Configure authentication settings centrally
- Prevent users from creating or modifying infrastructure configurations
- Ensure consistent backend connections across your organization

**Key Benefits:**

- **Centralized management**: Configure once, deploy everywhere
- **Security**: Pre-configure authentication without exposing credentials to end users
- **Consistency**: Ensure all users connect to the correct backends

```{seealso}
For detailed instructions on YAML-based infrastructure preconfiguration, including file structure, authentication options, and Docker deployment, see the [Infrastructure Configuration](../../../../developer_documentation/basyx_web_ui/configuration.md#infrastructure-configuration) section in the developer documentation.
```

## Configuration Precedence

When multiple configuration sources are present, the Web UI follows this precedence order (highest first):

1. **User modifications in browser** (stored in local storage)
2. **Environment variables** (set via Docker or system environment)
3. **YAML configuration file** (`basyx-infra.yml`)
4. **Application defaults**

This layered approach allows system administrators to provide default configurations while still enabling users to customize settings when permitted.

### Configuration Locking

System administrators can control whether users can modify infrastructure configurations:

- **`ENDPOINT_CONFIG_AVAILABLE=true`** (default): Users can create, edit, and delete infrastructures through the UI
- **`ENDPOINT_CONFIG_AVAILABLE=false`**: Infrastructure configuration is locked; users can only select from pre-configured infrastructures

```{hint}
Setting `ENDPOINT_CONFIG_AVAILABLE=false` is recommended for production environments where you want to enforce specific backend connections and prevent users from accidentally misconfiguring the application.
```

## Connecting to Different Environments

The flexible configuration system makes it easy to work with multiple environments:

**Development:**

- Connect to local BaSyx instances running on your development machine
- Quickly switch between different local setups
- Test with or without authentication

**Testing:**

- Connect to shared test infrastructure
- Validate configurations before production deployment
- Test multi-infrastructure scenarios

**Production:**

- Use pre-configured YAML files for consistent connections
- Lock configuration to prevent unauthorized changes
- Enable authentication and access control

## Troubleshooting Connection Issues

If you're having trouble connecting to your AAS infrastructure:

1. **Verify Endpoints**:
   - Ensure all component URLs are correct and accessible from your browser
   - Check that services are running and responding to requests
   - Test endpoint URLs directly in your browser

2. **Check Network Connectivity**:
   - Verify that your browser can reach the backend services
   - Check for firewall rules that might block connections
   - Ensure proper DNS resolution for domain names

3. **Review CORS Settings**:
   - Backend services must allow requests from the Web UI's origin
   - Check CORS headers in the backend service configuration
   - Verify that the Web UI's URL is whitelisted in backend CORS settings

4. **Inspect Authentication**:
   - Verify that authentication tokens or credentials are properly configured
   - Check token expiration and refresh behavior
   - Ensure the identity provider is accessible

5. **Use Browser Developer Tools**:
   - Open the browser console (F12) and check for error messages
   - Look for failed network requests in the Network tab
   - Check for CORS errors or authentication failures

```{seealso}
For authentication and authorization troubleshooting, see the [Security](./security.md) page.

For Docker-specific issues, see the [Docker Configuration](./docker_config.md) page.
```

## Next Steps

- **[Security](./security.md)**: Configure authentication and authorization
- **[Docker Configuration](./docker_config.md)**: Deploy and configure using Docker
- **[Corporate Design](./corporate_design.md)**: Customize branding and appearance
- **[Developer Documentation](../../../../developer_documentation/basyx_web_ui/configuration.md)**: Advanced configuration and YAML setup
