# Authorization
This feature enables authorized access to the AAS Environment.

```{note}
Only Role Based Access Control (RBAC) in combination with Keycloak as a JWT token provider is supported as authorization type as of now.
```

To learn more about the RBAC, please refer [Authorization Services Guide](https://www.keycloak.org/docs/latest/authorization_services/index.html)

To learn more about the Keycloak server administration, please refer [Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/#keycloak-features-and-concepts)

An example valid configuration:

```properties
basyx.feature.authorization.enabled = true
basyx.feature.authorization.type = rbac
basyx.feature.authorization.jwtBearerTokenProvider = keycloak
basyx.feature.authorization.rbac.file = classpath:rbac_rules.json
spring.security.oauth2.resourceserver.jwt.issuer-uri= http://localhost:9096/realms/BaSyx
```

## RBAC rule configuration

The rbac rules should be configured inside a json file, the rules are defined as below:

```
[
  {
    "role": "basyx-reader-serialization",
    "action": "READ",
    "targetInformation": {
      "@type": "aas-environment",
      "aasIds": ["shell001", "shell002"],
      "submodelIds": ["7A7104BDAB57E184", "AC69B1CB44F07935"]
    }
  },
  {
    "role": "admin",
    "action": ["CREATE", "READ", "UPDATE", "DELETE"],
    "targetInformation": {
      "@type": "aas-environment",
      "aasIds": "*",
      "submodelIds": "*"
    }
  },
  {
    "role": "basyx-reader-serialization-two",
    "action": "READ",
    "targetInformation": {
      "@type": "aas-environment",
      "aasIds": ["shell001", "shell002"],
      "submodelIds": ["7A7104BDAB57E184"]
    }
  }
 ]
```

A `role` specifies which actions are permitted to be performed by said users of that role. The role is as per the configuration of identity providers or based on the organization. Action could be CREATE, READ, UPDATE, DELETE, and EXECUTE, there could be a single action or multiple actions as a list (cf. admin configuration above).

The targetInformation defines coarse-grained control over the resource, you may define the aasIds and submodelIds with a wildcard (\*), it means the defined role x with action y can perform operations on all the AASs and Submodels. You can also define specific aasIds and submodelIds in place of the wildcard (\*), then the role x with action y could be performed only on that particular AASs and Submodels. Please note that filtering options are not currently supported. Therefore, for serialization requests, specifying certain aasIds or submodelIds will result in the request being rejected. This happens if there are other AAS or submodels in the environment that are not configured in the rules. A similar rule applies to upload requests.

```{note}
- The actions are static as of now and limited to `CREATE`, `READ`, `UPDATE`, `DELETE`, and `EXECUTE`
    - (Later, a user-configurable mapping of these actions will be provided)
- For serialization-related requests, it's essential to have defined rules for accessing AAS, Submodels, and Concept Descriptions, since serialization requires access to all these elements. If a role configured for serialization targets the AAS Environment but lacks the corresponding read permissions for AAS, Submodels, or Concept Descriptions, the request will be denied.
- For upload-related requests, defined rules for reading, creating, and updating AASs, Submodels, and Concept Descriptions are necessary. This is because upload requests involve creation, update, and retrieval operations on the AASs, Submodels, and Concept Descriptions contained in the uploaded files. Therefore, appropriate rules should be configured for the subjects under consideration.
- Each rule should be unique in combination of role + action + target information
```

## Action table for RBAC

Below is a reference table that shows which actions are used in what endpoints of the AAS Environment:

| Action  | Endpoint           |
|---------|--------------------|
| READ    | GET /serialization |
| CREATE  | POST /upload       |
| UPDATE  | -                  |
| DELETE  | -                  |
| EXECUTE | -                  |

