# Authorization

This feature enables authorized access to the AAS Discovery Service, allowing fine-grained control over access permissions based on roles.

**Important Notes:**

- Only Role-Based Access Control (RBAC) is supported as an authorization type currently.
- Keycloak is the supported JWT token provider by default.

For more details on setting up and managing RBAC and Keycloak:

- [Authorization Services Guide](https://www.keycloak.org/docs/latest/authorization_services/index.html)
- [Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/#keycloak-features-and-concepts)

An example valid configuration:

```json
{
  "basyx.feature.authorization.enabled": true,
  "basyx.feature.authorization.type": "rbac",
  "basyx.feature.authorization.jwtBearerTokenProvider": "keycloak",
  "basyx.feature.authorization.rbac.file": "classpath:rbac_rules.json",
  "spring.security.oauth2.resourceserver.jwt.issuer-uri": "http://localhost:9096/realms/BaSyx"
}
```

## RBAC Rule Configuration

RBAC rules should be configured in a JSON file as follows:

```json
[
  {
    "role": "basyx-assetid-creator",
    "action": "CREATE",
    "targetInformation": {
      "@type": "aas-discovery-service",
      "aasIds": "*",
      "assetIds": []
    }
  },
  {
    "role": "basyx-assetid-discoverer",
    "action": "READ",
    "targetInformation": {
      "@type": "aas-discovery-service",
      "aasIds": ["AasId1", "AasId2"],
      "assetIds": []
    }
  },
  {
    "role": "basyx-assetid-deleter",
    "action": "DELETE",
    "targetInformation": {
      "@type": "aas-discovery-service",
      "aasIds": "AasId1",
      "assetIds": []
    }
  },
  {
    "role": "basyx-aas-discoverer-all",
    "action": "READ",
    "targetInformation": {
      "@type": "aas-discovery-service",
      "aasIds": null,
      "assetIds": [
        {
          "name": "*",
          "value": "*"
        }
      ]
    }
  },
  {
    "role": "basyx-aas-discoverer-specific",
    "action": "READ",
    "targetInformation": {
      "@type": "aas-discovery-service",
      "aasIds": null,
      "assetIds": [
        {
          "name": "assetName1",
          "value": "assetValue1"
        },
        {
          "name": "assetName2",
          "value": "assetValue2"
        }
      ]
    }
  }
]
```

A `role` specifies which actions are permitted to be performed by said users of that role. The `action` can be CREATE, READ, DELETE, and the `targetInformation` provides coarse-grained control over the resource. You may define the `aasIds` and `assetIds` with a wildcard (*), which means the defined role with action can perform operations on all AASs and Assets. You can also define specific `aasIds` and `assetIds`.

```{note}
- The Actions are static as of now and limited to `CREATE`, `READ`, `UPDATE`, `DELETE`, and `EXECUTE`
    - (Later, a user-configurable mapping of these actions will be provided)
- Each rule should be unique in combination of role + action + target information
```

### Special Configuration Notes

- The wildcard `*` for `assetIds` must be inserted in both the `name` and `value` to indicate non-specific filtering for the `READ` endpoint on `/lookup/shells`.

## Action Table for RBAC

Below is a reference table that illustrates which actions are used at specific endpoints of the AAS Discovery Service:

| Action  | Endpoint                                | Note                           |
|---------|-----------------------------------------|--------------------------------|
| CREATE  | POST /lookup/shells/{aasIdentifier}     | Requires `aasIds`, `assetIds` can be empty. |
| READ    | GET /lookup/shells/{aasIdentifier}      | Requires `aasIds`, `assetIds` can be empty. |
| DELETE  | DELETE /lookup/shells/{aasIdentifier}   | Requires `aasIds`, `assetIds` can be empty. |
| READ    | GET /lookup/shells                      | Requires `assetIds`, `aasIds` can be empty. |
