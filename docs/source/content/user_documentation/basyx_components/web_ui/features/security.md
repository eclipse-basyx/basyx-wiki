# Security

> **As a** BaSyx AAS Web UI user  
> **I want to** securely access data from Asset Administration Shells  
> **so that** I can control who has access to what data and ensure proper authentication.

## Feature Overview

The BaSyx AAS Web UI supports comprehensive security mechanisms for authenticating users and controlling access to AAS data. The Web UI can integrate with various authentication methods and identity providers, ensuring secure access to your digital twin infrastructure.

Security in the AAS ecosystem is based on the standardized [AAS Security Specification (IDTA-01004)](https://industrialdigitaltwin.io/aas-specifications/IDTA-01004/v3.0.1/index.html), which defines authentication, authorization, and access control mechanisms for Asset Administration Shells. The Web UI implements these security concepts, supporting both **Role-Based Access Control (RBAC)** and **Attribute-Based Access Control (ABAC)** as defined in the AAS Part 4 specification.

```{note}
From the Web UI perspective, it doesn't matter whether your backend implements RBAC or ABAC—both are supported transparently through standard OAuth2/OIDC token-based authentication. The backend services determine which access control model is applied.
```

## Supported Authentication Methods

The BaSyx AAS Web UI supports multiple authentication methods that can be configured per infrastructure:

### 1. No Authentication

For development environments or publicly accessible AAS data, you can connect without authentication.

**Use Cases:**

- Local development and testing
- Public demo systems
- Read-only AAS viewers with no sensitive data

**Configuration:**
Simply set the security type to "None" when configuring an infrastructure.

```{warning}
Never use "No Authentication" for production systems containing sensitive or proprietary data.
```

### 2. OAuth2 / OpenID Connect (OIDC)

OAuth2 with OIDC is the recommended authentication method for production deployments. The Web UI supports **any OAuth2-compatible identity provider** (IDP), including:

- **Keycloak** (open-source IDP)
- **Azure Active Directory / Microsoft Entra ID**
- **Auth0**
- **Okta**
- **Google Identity Platform**
- **Amazon Cognito**
- **Any custom OAuth2/OIDC compliant identity provider**

```{important}
The key requirement is that your identity provider must be **OAuth2 and OIDC compatible**. As long as your IDP supports the OAuth2 Authorization Code Flow and provides OIDC discovery endpoints, it will work with the BaSyx AAS Web UI.
```

**Supported OAuth2 Flows:**

1. **Authorization Code Flow** (Recommended):
   - User-based authentication with browser redirect to IDP
   - Most secure for browser-based applications
   - Users log in with their credentials at the identity provider
   - Recommended for all production deployments

2. **Client Credentials Flow** (Use with Caution):
   - Machine-to-machine authentication
   - Application authenticates directly with IDP using client ID and secret
   - **Security Warning**: Client secrets are exposed in browser applications

```{danger}
**Client Credentials Flow Security Warning**

Client Credentials Flow is inherently insecure for browser-based applications because:
- Client secrets must be visible to the browser
- Secrets can be extracted from browser developer tools
- Any user with access to the application can obtain the secret

**Only use Client Credentials Flow for:**
- Internal development/testing environments
- Trusted network environments with no external access
- Demo/showcase scenarios with non-production credentials

**For production, always use Authorization Code Flow** with proper user authentication.
```

#### Configuring OAuth2

When configuring OAuth2 authentication for an infrastructure:

1. Open the infrastructure configuration in the UI
2. Select "OAuth2" as the security type
3. Provide the following information:
   - **Issuer URL**: The base URL of your OAuth2/OIDC provider (e.g., `https://keycloak.example.com/auth/realms/BaSyx`)
   - **Client ID**: Your application's client identifier registered with the IDP
   - **Scope** (optional): OAuth2 scopes to request (e.g., `openid profile email`)
   - **Flow**: Choose Authorization Code Flow (recommended) or Client Credentials Flow

```{figure} ./images/oauth2_config.png
---
width: 80%
alt: OAuth2 Configuration
name: oauth2_config
---
Configuring OAuth2 authentication for an infrastructure
```

**Important OAuth2 Configuration Notes:**

- **Discovery Endpoint**: Most OAuth2/OIDC providers support automatic discovery. The Web UI will use the issuer URL to discover the authorization endpoint, token endpoint, and other required URLs.

- **Redirect URI**: Make sure to register the Web UI's redirect URI with your identity provider. The redirect URI is typically: `https://your-web-ui-domain.com/` or `https://your-web-ui-domain.com/your-base-path/`

- **CORS Configuration**: Ensure your identity provider allows CORS requests from the Web UI's origin.

- **Token Refresh**: The Web UI automatically refreshes access tokens when they expire, ensuring uninterrupted access to AAS data.

### 3. Basic Authentication

HTTP Basic Authentication can be used for simple username/password authentication.

**Use Cases:**

- Simple authentication for internal systems
- Legacy systems that don't support OAuth2
- Development and testing scenarios

**Configuration:**

1. Select "Basic Authentication" as the security type
2. Provide the username and password

```{warning}
Basic Authentication credentials are Base64-encoded (not encrypted) and visible in browser memory. Use HTTPS to protect credentials in transit, and prefer OAuth2 for production systems.
```

### 4. Bearer Token

Use a pre-configured Bearer token for API access.

**Use Cases:**

- Service accounts with long-lived tokens
- Integration scenarios where OAuth2 flow is not feasible
- API testing and debugging

**Configuration:**

1. Select "Bearer Token" as the security type
2. Provide the bearer token string

```{note}
Bearer tokens do not automatically refresh. Ensure your token has sufficient validity for your use case.
```

## Multi-Infrastructure Security

One of the key features of the BaSyx AAS Web UI is the ability to connect to **multiple infrastructures with different identity providers**. This means:

- **Infrastructure A** can use Keycloak for authentication
- **Infrastructure B** can use Azure AD for authentication
- **Infrastructure C** can use no authentication (for public data)
- **Infrastructure D** can use Basic Auth (for legacy systems)

Each infrastructure maintains its own authentication state, and the Web UI handles token management and authentication flows independently for each infrastructure.

```{hint}
When switching between infrastructures, the Web UI will automatically use the appropriate authentication method and credentials for each infrastructure.
```

```{seealso}
For detailed information on configuring multiple infrastructures, see the [Configuration & Environment](./configuration.md) page.
```

## Access Control: RBAC vs. ABAC

The AAS Security Specification supports two access control models:

### Role-Based Access Control (RBAC)

- Access is granted based on user roles (e.g., "admin", "operator", "viewer")
- Simpler to configure and understand
- Widely supported and well-established
- Suitable for most organizational structures

### Attribute-Based Access Control (ABAC)

- Access is granted based on attributes (user attributes, resource attributes, environmental conditions)
- More flexible and fine-grained than RBAC
- Suitable for complex access control requirements
- Defined in AAS Part 4 v3.1+ specification

```{important}
The Web UI is **agnostic to the access control model** used by your backend. Both RBAC and ABAC work transparently through OAuth2 access tokens. The backend services determine which model is enforced based on the token claims and policies.
```

For more details on access control concepts, refer to the [AAS Security Specification Part 4](https://industrialdigitaltwin.io/aas-specifications/IDTA-01004/v3.0.1/index.html).

## Authentication User Experience

When authentication is configured, the user experience works as follows:

### Initial Access

1. User opens the BaSyx AAS Web UI
2. If OAuth2 is configured and the user is not authenticated:
   - The Web UI redirects to the identity provider's login page
   - User enters credentials at the IDP
   - After successful authentication, the user is redirected back to the Web UI with an access token
3. The access token is used for all subsequent requests to AAS backend services

### Token Management

- **Automatic Refresh**: Access tokens are automatically refreshed before they expire
- **Session Persistence**: Authentication state is maintained across browser sessions (if supported by the IDP)
- **Multi-Tab Support**: Authentication state is shared across multiple browser tabs

### Logout

When authentication is enabled, users can log out from the Web UI:

1. Click on the user profile or logout button in the application bar
2. The Web UI clears the local authentication state
3. Optionally, the user is redirected to the IDP's logout endpoint

```{note}
Logout functionality can be controlled with the `ALLOW_LOGOUT` environment variable. This is useful if you want to prevent users from logging out in certain deployments.
```

## Backend Service Security

The Web UI integrates with the security mechanisms of BaSyx backend components:

```{seealso}
For detailed information on configuring security for BaSyx backend components, refer to their respective documentation:

* [AAS Environment](../../v2/aas_environment/features/authorization.md)
* [AAS Registry](../../v2/aas_registry/features/authorization.md)
* [Submodel Registry](../../v2/submodel_registry/features/authorization.md)
* [AAS Repository](../../v2/aas_repository/features/authorization.md)
* [Submodel Repository](../../v2/submodel_repository/features/authorization.md)
* [Concept Description Repository](../../v2/cd_repository/features/authorization.md)
* [AAS Discovery Service](../../v2/aas_discovery/features/authorization.md)
```

## Configuring Security via Environment Variables (Legacy)

While the recommended approach is to configure security settings per infrastructure using the UI or YAML configuration files, you can also use environment variables for legacy deployments.

```{warning}
Using environment variables for authentication configuration is **deprecated** and maintained only for backward compatibility. New deployments should use the YAML-based infrastructure configuration.
```

**Deprecated Keycloak Environment Variables:**

- `KEYCLOAK_URL`: Keycloak server URL
- `KEYCLOAK_REALM`: Keycloak realm name
- `KEYCLOAK_CLIENT_ID`: Client identifier

**Deprecated Basic Auth Environment Variables:**

- `BASIC_AUTH_USERNAME`: Username for basic authentication
- `BASIC_AUTH_PASSWORD`: Password for basic authentication

```{seealso}
For current configuration approaches, see:
- [Configuration & Environment](./configuration.md) for UI-based and YAML configuration
- [Docker Configuration](./docker_config.md) for Docker environment variables
- [Developer Documentation](../../../../developer_documentation/basyx_web_ui/configuration.md) for YAML file structure and advanced configuration
```

## Security Best Practices

1. **Always use HTTPS** in production to encrypt data in transit
2. **Prefer OAuth2 Authorization Code Flow** for user authentication
3. **Never commit secrets** to version control (client secrets, passwords, tokens)
4. **Use YAML configuration** for system-wide deployment instead of environment variables
5. **Configure CORS properly** on both the Web UI and backend services
6. **Set appropriate token lifetimes** in your identity provider
7. **Enable logout functionality** to allow users to terminate sessions
8. **Monitor authentication failures** and investigate suspicious activity
9. **Use ABAC** for fine-grained access control when needed
10. **Regularly update** the Web UI and backend services to receive security patches

## Troubleshooting Authentication Issues

### Cannot Log In

1. **Verify IDP Configuration**:
   - Ensure the issuer URL is correct and accessible
   - Check that the client ID is registered with the IDP
   - Verify redirect URIs are properly configured

2. **Check CORS Settings**:
   - The IDP must allow requests from the Web UI's origin
   - Check browser console for CORS errors

3. **Review Token Scopes**:
   - Ensure requested scopes are supported by the IDP
   - Verify the user has permissions for the requested scopes

### Unauthorized Access to AAS Data

1. **Check Token Claims**:
   - Open browser developer tools and inspect the access token
   - Verify that required roles or attributes are present

2. **Backend Configuration**:
   - Ensure backend services are configured to accept tokens from your IDP
   - Verify backend RBAC/ABAC policies are correctly configured

3. **Token Expiration**:
   - Check if tokens are refreshing properly
   - Verify token lifetime settings in the IDP

### Authentication Works but Data Access Fails

1. **Verify Backend Security Configuration**:
   - Ensure backend services are using the same IDP configuration
   - Check that the Web UI's access token is being sent to backend services

2. **Check Network Connectivity**:
   - Verify that backend services are accessible from the browser
   - Check for proxy or firewall issues

```{seealso}
For general troubleshooting, see the [Configuration & Environment](./configuration.md#troubleshooting-connection-issues) page.
```
