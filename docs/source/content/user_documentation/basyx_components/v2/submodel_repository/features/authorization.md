# Authorization
This feature enables authorized access to the Submodel Repository.

To enable this feature, the following properties should be configured:

```
basyx.feature.authorization.enabled = true
basyx.feature.authorization.type = <The type of authorization to enable>
basyx.feature.authorization.jwtBearerTokenProvider = <The Jwt token provider>
basyx.feature.authorization.rbac.file = <Class path of the Rbac rules file if authorization type is rbac>
spring.security.oauth2.resourceserver.jwt.issuer-uri= <URI of the resource server>
```

```{note}
- Only Role Based Access Control (RBAC) is supported as authorization type as of now, also Keycloak is the only Jwt token provider supported now and it is also a default provider. 
```

To learn more about RBAC, please refer to the [Authorization Services Guide](https://www.keycloak.org/docs/latest/authorization_services/index.html)

To learn more about the Keycloak server administration, please refer [Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/#keycloak-features-and-concepts)

## RBAC rule configuration

To configure the RBAC rules, you need to create a JSON file for them. Rules could like shown below:

```
[
  {
    "role": "basyx-reader",
    "action": "READ",
    "targetInformation": {
      "@type": "submodel",
      "submodelIds": "*",
      "submodelElementIdShortPaths": "*"
    }
  },
  {
    "role": "admin",
    "action": ["CREATE", "READ", "UPDATE", "DELETE", "EXECUTE"],
    "targetInformation": {
      "@type": "submodel",
      "submodelIds": "*",
      "submodelElementIdShortPaths": "*"
    }
  },
  {
    "role": "basyx-reader-two",
    "action": "READ",
    "targetInformation": {
      "@type": "submodel",
      "submodelIds": "specificSubmodelId",
      "submodelElementIdShortPaths": "*"
    }
  },
  {
    "role": "basyx-sme-reader",
    "action": "READ",
    "targetInformation": {
      "@type": "submodel",
      "submodelIds": ["specificSubmodelId", "testSMId1", "testSMId2"],
      "submodelElementIdShortPaths": ["testSMEIdShortPath1","smc2.specificSubmodelElementIdShort","testSMEIdShortPath2"]
    }
  }
 ]
```

A `role` specifies which actions are permitted to be performed by said users of that role. The role is as per the configuration of identity providers or based on the organization. Action could be CREATE, READ, UPDATE, DELETE, and EXECUTE, there could be a single action or multiple actions as a list (cf. admin configuration above).

The targetInformation defines coarse-grained control over the resource, you may define the submodelIds and submodelElementIdShortPaths with a wildcard (\*), it means the defined role x with action y can access any Submodel and any SubmodelElement on the repository.

You can also define a specific Submodel Identifier in place of the wildcard (\*), then the role x with action y could be performed only on that particular Submodel.

Similarly, you can define a specific SubmodelElement IdShort path, then you can only access the SubmodelElement corresponding to that IdShort path.
It means that the whole Submodel GET request would not be possible if the IdShort path for a specific SubmodelElement is provided, because the requestor only has access for a specific SubmodelElement.
There could be a single submodelId/submodelElementIdShortPath or multiple submodelIds/submodelElementIdShortPaths as a list (cf. basyx-sme-reader).

```{note}
- The Actions are static as of now and limited to `CREATE`, `READ`, `UPDATE`, `DELETE`, and `EXECUTE`
    - (Later, a user-configurable mapping of these actions will be provided)
- Each rule should be unique in combination of role + action + target information
```

## Action table for RBAC

Below is a reference table that shows which actions are used in what endpoints of the Submodel Repository:

| Action  | Endpoint                                                                                                                                                                                                            |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| READ    | GET /submodels <br /> GET /submodels/{submodelIdentifier} <br /> GET /submodels/{submodelIdentifier}/$value <br /> GET /submodels/{submodelIdentifier}/$metadata <br /> GET /submodels/{submodelIdentifier}/submodel-elements <br /> GET /submodels/{submodelIdentifier}/submodel-elements/{idShortPath} <br /> GET /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$value <br /> GET /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/attachment  |
| CREATE  | POST /submodels <br />                                                                                                                                                                                                   |
| UPDATE  | PUT /submodels/{submodelIdentifier} <br /> PUT /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/attachment <br /> POST /submodels/{submodelIdentifier}/submodel-elements/{idShortPath} <br /> POST /submodels/{submodelIdentifier}/submodel-elements <br />  PATCH /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$value <br /> PATCH /submodels/{submodelIdentifier}/$value <br /> DELETE /submodels/{submodelIdentifier}/submodel-elements/{idShortPath} <br /> DELETE /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/attachment |
| DELETE  | DELETE /submodels/{submodelIdentifier}  |
| EXECUTE | POST /submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/invoke <br />                                                                                                                                                                                                                |

```{note}
The invoke operation is not supported currently for off-the-shelf component
```