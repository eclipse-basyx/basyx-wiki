# Authorization

## <span style="color:red">The whole document targets the Java-version of the SDK and components only.</span>

You can add authorization requirements to the actions of BaSyx components that would be subject to the AssetAdministrationShell, Registry and Submodel APIs.

[BaSyx Asset Administration Shell Repository HTTP REST-API](https://app.swaggerhub.com/apis-docs/BaSyx/basyx_asset_administration_shell_repository_http_rest_api/v1#/)

[BaSyx Registry HTTP REST-API](https://app.swaggerhub.com/apis-docs/BaSyx/BaSyx_Registry_API/v1#/)

[BaSyx Submodel HTTP REST-API](https://app.swaggerhub.com/apis-docs/BaSyx/basyx_submodel_http_rest_api/v1)


## <span style="color:red"> For an introduction, also take a look at the [Examples](https://github.com/eclipse-basyx/basyx-java-examples/tree/main/basyx.examples/src/main/java/org/eclipse/basyx/examples/scenarios/authorization/combined).</span>


As BaSyx is meant to support various architectures as a foundational technology, the authorization capabilities are designed accordingly in a somewhat generic way to make it adaptable. At the same time, to reduce the effort, there are implemented standard strategies shipped with BaSyx.

# Provided Authorization Strategies
## GrantedAuthority
The name comes from the GrantedAuthority interface of Spring Security.

As a default, a list of such GrantedAuthority objects can be obtained from a Spring Security Authentication object, which in turn can be attached to the Spring Security Context associated to individual requests the BaSyx server receives. For this to work, we need to indicate that the Authentication object should be taken from the JWT Bearer Token included in the Authorization field of an HTTP request and that token should also be validated and checked against the authorization server. The granted authorities are specified by specific claims inside the JWT. See the table below to for what scopes are required for what actions.

The claims for the allowed actions in the JWT used for the default Keycloak JWT parser look like this (either in realm_access or resource_access):
```yaml
{
  ...,
  "realm_access": {
    "roles": [
        "urn:org.eclipse.basyx:scope:aas-aggregator:read",
        "urn:org.eclipse.basyx:scope:aas-aggregator:write",
        "urn:org.eclipse.basyx:scope:aas-api:read",
        "urn:org.eclipse.basyx:scope:aas-api:write",
        "urn:org.eclipse.basyx:scope:sm-aggregator:read",
        "urn:org.eclipse.basyx:scope:sm-aggregator:write",
        "urn:org.eclipse.basyx:scope:sm-api:read",
        "urn:org.eclipse.basyx:scope:sm-api:write",
        "urn:org.eclipse.basyx:scope:aas-registry:read",
        "urn:org.eclipse.basyx:scope:aas-registry:write",
    ]
  },
  "resource_access": {
    "account": {
      "roles": [
        "urn:org.eclipse.basyx:scope:aas-aggregator:read",
        "urn:org.eclipse.basyx:scope:aas-aggregator:write",
        "urn:org.eclipse.basyx:scope:aas-api:read",
        "urn:org.eclipse.basyx:scope:aas-api:write",
        "urn:org.eclipse.basyx:scope:sm-aggregator:read",
        "urn:org.eclipse.basyx:scope:sm-aggregator:write",
        "urn:org.eclipse.basyx:scope:sm-api:read",
        "urn:org.eclipse.basyx:scope:sm-api:write",
        "urn:org.eclipse.basyx:scope:aas-registry:read",
        "urn:org.eclipse.basyx:scope:aas-registry:write",
      ]
    }
  }
}
```
This strategy can further be customized by specifying how the granted authorities are to be obtained (implementing the ISubjectInformationProvider and IGrantedAuthorityAuthenticator interfaces).

For more information on how GrantedAuthority can be used, see "Using Authorization -> Off-the-Shelf components" and "Using Authorization -> SDK" respectively.

## SimpleRbac
The SimpleRbac strategy is a bit more flexible than GrantedAuthority in that there are further indirections.

As a default, instead of having the permissions directly held in the JWT, the (normally Keycloak-formatted)-JWT only indicates roles of the requester and, from another data source, there are rules specified consisting of role, action and resource tuples that decide whether the role is allowed to do the action on the resource.

When using the default role authenticator implementation, the Jwt should look like this:
```
{
  ...,
  "realm_access": {
    "roles": [
        "roleA",
        "roleB",
        "roleC"
    ]
  }
}
```
This strategy can be further customized by specifying how the roles are obtained (implementing the ISubjectInformationProvider and IRoleAuthenticator interfaces).

The rules can also be provided in different ways (implementing the IRbacRuleChecker interface).

# Using Authorization
## Off-the-Shelf Components
For the Off-the-Shelf components (AASServer and Registry), the creation of the component is already handled for you. The authorization for those can be configured via the `security.properties` files and the main switches for turning on/off authorization as a feature are in the `aas.properties` and `registry.properties` file, respectively.

* AAS-Server Security Properties: [[security.properties]](https://github.com/eclipse-basyx/basyx-java-components/blob/main/basyx.components/basyx.components.docker/basyx.components.AASServer/src/main/resources/security.properties)
* AAS-Server Main Properties: [[aas.properties]](https://github.com/eclipse-basyx/basyx-java-components/blob/main/basyx.components/basyx.components.docker/basyx.components.AASServer/src/main/resources/security.properties)
* Registry Security Properties [[security.properties]](https://github.com/eclipse-basyx/basyx-java-components/blob/main/basyx.components/basyx.components.docker/basyx.components.registry/src/main/resources/security.properties)
* Registry Main Properties: [[registry.properties]](https://github.com/eclipse-basyx/basyx-java-components/blob/main/basyx.components/basyx.components.docker/basyx.components.registry/src/main/resources/security.properties)

The authorization key-value pairs inside the files look like this:

For AAS-Server:

aas.properties:
```yaml
aas.authorization=Enabled
The security.properties looks like this for both components:

# ######################
# Authorization
# ######################
authorization.strategy=GrantedAuthority
# authorization.strategy=SimpleRbac
# authorization.strategy=Custom
authorization.strategy.jwtBearerTokenAuthenticationConfigurationProvider=org.eclipse.basyx.components.security.authorization.internal.KeycloakJwtBearerTokenAuthenticationConfigurationProvider
authorization.strategy.jwtBearerTokenAuthenticationConfigurationProvider.keycloak.serverUrl=http://localhost:9005
authorization.strategy.jwtBearerTokenAuthenticationConfigurationProvider.keycloak.realm=basyx-demo
authorization.strategy.jwtBearerTokenAuthenticationConfigurationProvider.audience=aas-server
authorization.strategy.simpleRbac.rulesFilePath=/rbac_rules.json
authorization.strategy.simpleRbac.subjectInformationProvider=org.eclipse.basyx.extensions.shared.authorization.internal.JWTAuthenticationContextProvider
authorization.strategy.simpleRbac.roleAuthenticator=org.eclipse.basyx.extensions.shared.authorization.internal.KeycloakRoleAuthenticator
authorization.strategy.grantedAuthority.subjectInformationProvider=org.eclipse.basyx.extensions.shared.authorization.internal.AuthenticationContextProvider
authorization.strategy.grantedAuthority.grantedAuthorityAuthenticator=org.eclipse.basyx.extensions.shared.authorization.internal.AuthenticationGrantedAuthorityAuthenticator
authorization.strategy.custom.authorizersProvider=
authorization.strategy.custom.subjectInformationProvider=
```
It is analogous for the registry, apart from the main switch being prefixed by `registry` instead of aas:
`registry.authorization=Enabled`
.
<span style="color:red">Keep in mind that that when using environment variables, there are further prefixes denoting the group of properties:</span>

|         File        |     Prefix     |
|:-------------------:|:--------------:|
| aas.properties      | BaSyxAAS_      |
| registry.properties | BaSyxRegistry_ |
| security.properties | BaSyxSecurity_ |

So for example instead of

`aas.authorization=Enabled`
one would write

`basyxaas_aas_authorization=Enabled`
or instead of

`authorization.strategy=SimpleRbac`
one would write

`basyxsecurity_authorization_strategy=SimpleRbac`
.

Here are the relevant security properties in full form with their meaning:

<span style="color:grey"> BaSyx Asset Administration Shell Repository HTTP REST-API </span>
|                                                  Property                                                 |         Possible values        |                                                                                           Description                                                                                           |                                               Default value                                              |
|:---------------------------------------------------------------------------------------------------------:|:------------------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------:|
| basyxaas.aas.authorization                                                                                | Disabled, Enabled              | main switch for authorization features (of AAS-Server), when disabled, all the other fields won't be effective                                                                                  | Disabled                                                                                                 |
| basyxregistry.registry.authorization                                                                      | Disabled, Enabled              | main switch for authorization features (of AAS-Registry), when disabled, all the other fields won't be effective                                                                                | Disabled                                                                                                 |
| basyxsecurity.authorization.strategy                                                                      | GrantedAuthority, SimpleRbac   | The basic authorization strategy, see section "Provided Authorization Strategies"                                                                                                               | GrantedAuthority                                                                                         |
| basyxsecurity.authorization.strategy.jwtBearerTokenAuthenticationConfigurationProvider                    | <class>                        | The class responsible for providing a jwt bearer token authentication configuration, has to implement the IJwtBearerTokenAuthenticationConfigurationProvider interface                          | org.eclipse.basyx.components.aas.authorization.KeycloakJwtBearerTokenAuthenticationConfigurationProvider |
| basyxsecurity.authorization.strategy.jwtBearerTokenAuthenticationConfigurationProvider.keycloak.serverUrl | <url>                          | base url for the keycloak                                                                                                                                                                       | null                                                                                                     |
| basyxsecurity.authorization.strategy.jwtBearerTokenAuthenticationConfigurationProvider.keycloak.realm     | basyx-demo                     | realm in the keycloak                                                                                                                                                                           | null                                                                                                     |
| basyxsecurity.authorization.strategy.jwtBearerTokenAuthenticationConfigurationProvider.keycloak.audience  | demo-client                    | optional audience the token is for                                                                                                                                                              | null                                                                                                     |
| basyxsecurity.authorization.strategy.simpleRbac.rulesFilePath                                             | <file path> (json, see schema) | relative path to rbac rules for SimpleRbac strategy                                                                                                                                             | /rbac_rules.json                                                                                         |
| basyxsecurity.authorization.strategy.simpleRbac.subjectInformationProvider                                | <class>                        | class that provides the Authentication object for SimpleRbac strategy, has to implemented ISubjectInformationProvider                                                                           | org.eclipse.basyx.extensions.shared.authorization.JWTAuthenticationContextProvider                       |
| basyxsecurity.authorization.strategy.simpleRbac.roleAuthenticator                                         | <class>                        | class that extracts the roles from the Authentication object for SimpleRbac strategy, has to implement IRoleAuthenticator                                                                       | org.eclipse.basyx.extensions.shared.authorization.KeycloakRoleAuthenticator                              |
| basyxsecurity.authorization.strategy.grantedAuthority.subjectInformationProvider                          | <class>                        | class that fetches the Authentication object for GrantedAuthority strategy, hsa to implement ISubjectInformationProvider                                                                        | org.eclipse.basyx.extensions.shared.authorization.AuthenticationContextProvider                          |
| basyxsecurity.authorization.strategy.grantedAuthority.grantedAuthorityAuthenticator                       | <class>                        | class that extracts the granted authorities from Authentication object for GrantedAuthority strategy, has to implement IGrantedAuthorityAuthenticator                                           | org.eclipse.basyx.extensions.shared.authorization.AuthenticationGrantedAuthorityAuthenticator            |
| basyxsecurity.authorization.strategy.custom.authorizersProvider                                           | <class>                        | class that provides the authorizers for AAS-Server/Registry respectively for custom strategy, must implement IAuthorizersProvider, thus 3rd party authorization logic can be dynamically loaded |                                                                                                          |
| basyxsecurity.authorization.strategy.custom.subjectInformationProvider                                    | <class>                        | class that provides the subject information retrieval logic to go with the custom authorizers, must implement ISubjectInformationProvider                                                       |                                                                                                          |

## SimpleRbac in the Components
The components use a json file (named rbac_rules.json on default) containing the rules that allow access when using the SimpleRbac strategy.

Its schema looks like this:
```yaml
[
  {
    "role": "admin",
    "action": "urn:org.eclipse.basyx:scope:aas-registry:read",
    "targetInformation": {
      "@type": "basyx",
      "aasId": "*",
      "smId": "*",
      "smSemanticId": "*",
      "smElIdShortPath": "*"
    }
  },
  {
    "role": "admin",
    "action": "urn:org.eclipse.basyx:scope:aas-registry:write",
    "targetInformation": {
      "@type": "basyx",
      "aasId": "*",
      "smId": "*",
      "smSemanticId": "*",
      "smElIdShortPath": "*"
    }
  },
  {
    "role": "user",
    "action": "urn:org.eclipse.basyx:scope:aas-registry:read",
    "targetInformation": {
      "@type": "basyx",
      "aasId": "*",
      "smId": "*",
      "smSemanticId": "*",
      "smElIdShortPath": "*"
    }
  }
]
```
This is a whitelist approach, each object in the outer array makes one RbacRule. If the combination of the role of the subject making some request, the action type and the attributes of the target resource handled in some operation is found within this list, it will be allowed, otherwise rejected.

That format currently supports using the aas id, submodel id, semantic id of the submodel and the id of the submodel element for target attributes. At the moment, you can only state one role per tuple that requester must possess but the action can be written as an array more tersely like:

   ` "action": ["urn:org.eclipse.basyx:scope:aas-registry:read", "urn:org.eclipse.basyx:scope:aas-registry:write"],`
This effectively translates to two tuples, one whose action is *"urn:org.eclipse.basyx:scope:aas-registry:read"* and another whose action is *"urn:org.eclipse.basyx:scope:aas-registry:write"* while the rest of the attributes is the same.

For the tag-based operations in the registry and tagged directory, there is another targetInformation type "tag":
```yaml
[
  {
    "role": "user",
    "action": "urn:org.eclipse.basyx:scope:aas-registry:read",
    "targetInformation": {
      "@type": "tag",
      "tag": "mytag"
    }
  }
]
```
If the request has an access token (Jwt), the token will be validated and subject information extracted from it for the downstream access controls. A failed validation will result in a 401 response. If, however, there is no access token (anonymous access), this initial validation step will be skipped and the request forwarded to the downstream access controls. On default, the SimpleRbac strategy uses *org.eclipse.basyx.extensions.shared.authorization.KeycloakRoleAuthenticator* for extracting role information from a potential access token. If there is no access token or the expected claims to be read for the roles could not be extracted, then this role extractor will return the special role `anonymous`, which can be used in the rbac_rules.json like other roles but to grant permissions to requests without authentication.

The AAS-Server in particular has another functionality where you can download files from the server. Thus, the access control is extended there and you can allow the download of files like this:
```yaml
[
  {
    "role": "user",
    "action": "urn:org.eclipse.basyx:scope:files:read",
    "targetInformation": {
      "@type": "path",
      "path": "secret.pdf"
    }
  }
]
```
where path is the path to the file.

# SDK
When using the SDK directly, you have to mount the desired servlets yourself onto the BaSyx server and create for example a submodel API that should be served on some endpoint. The main types of resources the BaSyx SDK supplies are specified with the following interfaces:

* IAASAggregator
* IAASAPI
* IAASRegistry
* ISubmodelAggregator
* ISubmodelAPI

and for each of those, there are common implementations available. In order to add authorization functionalities to those, we employ a decorator pattern, wrapping the actual resource providers in authorized decorations, which implement the interface, too, are therefore usable in the same places where common implementations would be allowed.

So instead of
```java
context.addServletMapping("/*", new VABHTTPInterface<>(
  new SubmodelProvider(
    new VABSubmodelAPI(
      new SubmodelProvider(
        new Submodel()
      )
    )
  )
));
```
you would write
```java
context.addServletMapping("/*", new VABHTTPInterface<>(
  new SubmodelProvider(
    new AuthorizedSubmodelAPI<>(
      new VABSubmodelAPI(
        new SubmodelProvider(
          new Submodel()
        )
      )
    )
  )
));
```
This overload of the AuthorizedSubmodelAPI constructor is deprecated and would use the GrantedAuthority authorization strategy as a legacy mechanism. The current, more explicit variant would be:
```java
context.addServletMapping("/*", new VABHTTPInterface<>(
  new SubmodelProvider(
    new AuthorizedSubmodelAPI<>(
      new VABSubmodelAPI(
        new SubmodelProvider(
          new Submodel()
        )
      ),
      new GrantedAuthoritySubmodelAPIAuthorizer<>(
        new AuthenticationGrantedAuthorityAuthenticator()
      ),
      new AuthenticationContextProvider()
    )
  )
));
```
the signature of the AuthorizedSubmodelAPI constructor being
``(ISubmodelAPI decoratedSubmodelAPI, ISubmodelAPIAuthorizer<SubjectInformationType> submodelAPIAuthorizer, ISubjectInformationProvider<SubjectInformationType> subjectInformationProvider)``
.
The available authorized variants of the aforementioned interfaces are:

* AuthorizedAASAggregator
* AuthorizedAASAPI
* AuthorizedAASRegistry
* AuthorizedSubmodelAggregator
* AuthorizedSubmodelAPI

with a similar pattern.

The decocator does not automatically work transitively. Even if you authorize the AAS-Aggregator, the AAS-APIs mounted therein are not authorized. There are however overloads for the factories of AAS-API you can pass to the AAS-Aggregator constructor, so you can make it create an authorized version of the AAS-API.
```java
ISubjectInformationProvider<Authentication> subjectInformationProvider = new AuthenticationContextProvider();
IGrantedAuthorityAuthenticator<Authentication> grantedAuthorityAuthenticator = new AuthenticationGrantedAuthorityAuthenticator();
context.addServletMapping("/*", new VABHTTPInterface<>(
  new AASAggregatorProvider(
    new AuthorizedAASAggregator<>(
      new AASAggregator(
        aas -> new AuthorizedAASAPI<>(
          new VABAASAPIFactory().getAASApi(aas),
          new GrantedAuthorityAASAPIAuthorizer<>(
            grantedAuthorityAuthenticator
          ),
          subjectInformationProvider
        ),
        submodel -> new AuthorizedSubmodelAPI<>(
          new VABSubmodelAPIFactory().getSubmodelAPI(submodel),
          new GrantedAuthoritySubmodelAPIAuthorizer<>(
            grantedAuthorityAuthenticator
          ),
          subjectInformationProvider
        ),
        new AuthorizedAASRegistryProxy(REGISTRY_URL, keycloakService::getTokenAsBearer)
      ),
      new GrantedAuthorityAASAggregatorAuthorizer<>(
        grantedAuthorityAuthenticator
      ),
      subjectInformationProvider
    )
  )
));
```
It's analogous for the submodel aggregator. The registry doesn't have that issue.

In order to support reading a JWT from the HTTP Authorization header and validating the token, we need to further install a JwtBearerTokenAuthenticationConfiguration on the context:
```java
String KEYCLOAK_SERVER_URL = "http://localhost:9005/auth"; // base auth path of the Keycloak
String KEYCLOAK_REALM = "basyx-demo"; // realm of the Keycloak which the token belongs to
KeycloakService keycloakService = new KeycloakService(KEYCLOAK_SERVER_URL, KEYCLOAK_REALM);
...
// context is a BaSyxContext
context.setJwtBearerTokenAuthenticationConfiguration(
  keycloakService.createJwtBearerTokenAuthenticationConfiguration()
);
```
The required JwtBearerTokenAuthenticationConfiguration object can also be created directly via its own factory method:

``JwtBearerTokenAuthenticationConfiguration.of(issuerUri, jwkSetUri, optionalRequiredAudience)``
## Customziation
By implementing ISubmodelAPIAuthorizer or similar plus ISubjectInformationProvider, you can add own authorization logic. The ISubmodelAPIAuthorizer interface for example declares methods which mirror the operations of the ISubmodelAPI interface to deliver an authorization decision for each of those operations.

The next snippet shows the GrantedAuthority implementation of a method making a decision about getting the list of submodel elements of the submodel API:
```java
@Override
public Collection<ISubmodelElement> enforceGetSubmodelElements(final SubjectInformationType subjectInformation, final IIdentifier aasId, final IIdentifier smId, final Supplier<Collection<ISubmodelElement>> smElListSupplier) throws InhibitException {
  if (grantedAuthorityAuthenticator.getAuthorities(subjectInformation).stream()
  .map(GrantedAuthority::getAuthority)
  .noneMatch(authority -> authority.equals(AuthorizedSubmodelAPI.READ_AUTHORITY))) {
    throw new InhibitException();
  }
  return smElListSupplier.get();
}
```

If you want to inhibit an operation, you should throw an InhibitException, which gets translated into a 403 HTTP response status code later on, otherwise just return from the method execution normally. Some operations like the one shown above have a return value, thus you can also modify what value gets returned when the operation is allowed. For example, in this case, it can be used to filter some elements from the list or it could be used to pseudonymize returned data.

The ISubjectInformationProvider supplies the subject information considered by the authorizer. For example, you can read the JWT from a Spring Security Authentication object from the Spring Security Context. Its generic parameter has to match the generic parameter of the associated ISubmodelAPIAuthorizer.

Further utility and facilities for authorization can be found at [https://github.com/eclipse-basyx/basyx-java-sdk/tree/main/src/main/java/org/eclipse/basyx/extensions/shared/internal/authorization].

Among that is the KeycloakService class, which has some methods to interact with a Keycloak server. The BaSyx SDK also has the [[Keycloak Admin REST Client Java library]](https://mvnrepository.com/artifact/org.keycloak/keycloak-admin-client) as a dependency.

# Scope tables for GrantedAuthority and SimpleRbac
Below are reference tables that show which action scopes are used in what endpoints of the Off-the-Shelf components and analogously for the component servlets that you would add with the SDK. The permissions and authorization decisions are not directly matching the endpoints but rather target the individual service operations backing them. For example, in order to write to an AAS-API on an AASServer, it would first ask the AAS-Aggregator to provide the AAS-API, which requires reading permission for the AAS-Aggregator, before trying to write to the AAS-API, which would additionally need writing permissions for the AAS-API.

<span style="color:grey"> BaSyx Asset Administration Shell Repository HTTP REST-API</span>

| Action                                           |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  Used in                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|--------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| urn:org.eclipse.basyx:scope:aas-aggregator:read  | GET /shells<br>GET /shells/{aasId}<br>PUT /shells/{aasId}<br>DELETE /shells/{aasId}<br>GET /shells/{aasId}/aas<br>GET /shells<br>GET /shells/{aasId}/aas/submodels<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/values<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodelElements<br>PUT /shells/{aasId}/aas/submodels/{submodelIdShort}/submodelElements/{seIdShortPath}<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodelElements/{seIdShortPath}<br>DELETE /shells/{aasId}/aas/submodels/{submodelIdShort}/submodelElements/{seIdShortPath}<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodelElements/{seIdShortPath}/value<br>PUT /shells/{aasId}/aas/submodels/{submodelIdShort}/submodelElements/{seIdShortPath}/value<br>POST /shells/{aasId}/aas/submodels/{submodelIdShort}/submodelElements/{idShortPathToOperation}/invoke<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodelElements/{idShortPathToOperation}/invocationList |
| urn:org.eclipse.basyx:scope:aas-aggregator:write | PUT /shells/{aasId}<br>DELETE /shells/{aasId}<br>PUT /shells/{aasId}/aas/submodels/{submodelIdShort}<br>DELETE /shells/{aasId}/aas/submodels/{submodelIdShort}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| urn:org.eclipse.basyx:scope:aas-api:read         | GET /shells/{aasId}<br>GET /shells/{aasId}/aas<br>GET /shells/{aasId}/aas/submodels<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| urn:org.eclipse.basyx:scope:aas-api:write        | PUT /shells/{aasId}/aas/submodels/{submodelIdShort}<br>DELETE /shells/{aasId}/aas/submodels/{submodelIdShort}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| urn:org.eclipse.basyx:scope:aas-registry:write   | GET /api/v1/registry<br>GET /api/v1/registry/{aasId}<br>GET /api/v1/registry/{aasId}/submodels/{submodelId}<br>GET /api/v1/registry/{aasId}/submodels                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| urn:org.eclipse.basyx:scope:aas-registry:write   | PUT /api/v1/registry/{aasId}<br>DELETE /api/v1/registry/{aasId}<br>PUT /api/v1/registry/{aasId}/submodels/{submodelId}<br>DELETE /api/v1/registry/{aasId}/submodels/{submodelId}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| urn:org.eclipse.basyx:scope:sm-aggregator:read   | GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/values<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{seIdShortPath}<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{seIdShortPath}/value<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{idShortPathToOperation}/invocationList<br>PUT /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{seIdShortPath}<br>DELETE /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{seIdShortPath}<br>PUT /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{seIdShortPath}/value<br>POST /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{idShortPathToOperation}/invoke                                                                                                                                                      |
| urn:org.eclipse.basyx:scope:sm-aggregator:write  | GET /shells/{aasId}/aas/submodels<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel<br>PUT /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel<br>DELETE /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| urn:org.eclipse.basyx:scope:sm-api:read          | GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/values<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{seIdShortPath}<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{seIdShortPath}/value<br>GET /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{idShortPathToOperation}/invocationList                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| urn:org.eclipse.basyx:scope:sm-api:write         | PUT /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{seIdShortPath}<br>DELETE /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{seIdShortPath}<br>PUT /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{seIdShortPath}/value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| urn:org.eclipse.basyx:scope:sm-api:execute       | POST /shells/{aasId}/aas/submodels/{submodelIdShort}/submodel/submodelElements/{idShortPathToOperation}/invoke                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |


<span style="color:grey"> BaSyx Submodel HTTP REST-API </span>

|                     Action                     	|                                                                                      Used in                                                                                     	|
|:----------------------------------------------:	|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:	|
| urn:org.eclipse.basyx:scope:aas-registry:read  	| GET /api/v1/registry<br>GET /api/v1/registry/{aasId}<br>GET /api/v1/registry/{aasId}/submodels/{submodelId}<br>GET /api/v1/registry/{aasId}/submodels                            	|
| urn:org.eclipse.basyx:scope:aas-registry:write 	| PUT /api/v1/registry/{aasId}<br>DELETE /api/v1/registry/{aasId}<br>PUT /api/v1/registry/{aasId}/submodels/{submodelId}<br>DELETE /api/v1/registry/{aasId}/submodels/{submodelId} 	|


<span style="color:grey"> BaSyx Submodel HTTP REST-API </span>

|                   Action                   	|                                                                                                                           Used in                                                                                                                           	|
|:------------------------------------------:	|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:	|
| urn:org.eclipse.basyx:scope:sm-api:read    	| GET /submodel<br>GET /submodel/values<br>GET /submodel/submodelElements<br>GET /submodel/submodelElements/{seIdShortPath}<br>GET /submodel/submodelElements/{seIdShortPath}/value<br>GET /submodel/submodelElements/{idShortPathToOperation}/invocationList 	|
| urn:org.eclipse.basyx:scope:sm-api:write   	| PUT /submodel/submodelElements/{seIdShortPath}<br>DELETE /submodel/submodelElements/{seIdShortPath}<br>PUT /submodel/submodelElements/{seIdShortPath}/value                                                                                                 	|
| urn:org.eclipse.basyx:scope:sm-api:execute 	| POST /submodel/submodelElements/{idShortPathToOperation}/invoke                                                                                                                                                                                             	|