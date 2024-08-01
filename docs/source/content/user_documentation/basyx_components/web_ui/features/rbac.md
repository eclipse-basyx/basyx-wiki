# Role Based Access Control (RBAC)

>As AAS Components user
>I want to securely access data from Asset Administration Shells
>using the AAS Web UI so that I can control who has access to what data

The AAS Web UI supports the use of RBAC mechanisms using Keycloak as an identity provider. This allows you to control who has access to what data when using the AAS Web UI.

## Feature Overview

When RBAC is configured for all BaSyx components, the AAS Web UI will use Keycloak to authenticate users. When a user opens the AAS Web UI, they will be redirected to the Keycloak login page. After successful login, the user will be redirected back to the AAS Web UI.

After the login process is complete, the user will be able to access AAS data based on the permissions granted to them by the Keycloak server. This is handled by using access tokens provided by Keycloak that get automatically refreshed when they expire.

The user is also able to log out and see the status of their session in the app bar.

## Feature Configuration

The feature can be configured by using Docker environment variables. The RBAC feature is only enabled in the AAS Web UI when the environment variables `KEYCLOAK_URL`, `KEYCLOAK_REALM`, and `KEYCLOAK_CLIENT_ID` are set.

When using **Docker Run** you can set the environment variables like this:

`docker run -p 3000:3000 -e KEYCLOAK_URL=<keycloak_url> -e KEYCLOAK_REALM=<keycloak_realm> -e KEYCLOAK_CLIENT_ID=<keycloak_client_id> eclipsebasyx/aas-gui`
The same feature can also be adapted for **Docker compose**:

```yaml
aas-web-gui:
   image: eclipsebasyx/aas-gui
   container_name: aas-web-gui
   ports:
       - "3000:3000"
   environment:
      KEYCLOAK_URL: "<keycloak_url>"
      KEYCLOAK_REALM: "<keycloak_realm>"
      KEYCLOAK_CLIENT_ID: "<keycloak_client_id>"
```

```{seealso}
The configuration of RBAC for the other BaSyx components can be found here:
* [AAS Environment](../../v2/aas_environment/features/authorization.md)
* [AAS Registry](../../v2/aas_registry/features/authorization.md)
* [Submodel Registry](../../v2/submodel_registry/features/authorization.md)
* [AAS Repository](../../v2/aas_repository/features/authorization.md)
* [Submodel Repository](../../v2/submodel_repository/features/authorization.md)
* [Concept Description Repository](../../v2/cd_repository/features/authorization.md)
* [AAS Discovery Service](../../v2/aas_discovery/features/authorization.md)
```
