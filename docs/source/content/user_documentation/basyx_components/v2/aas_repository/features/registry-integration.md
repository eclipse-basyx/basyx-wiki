# Registry Integration
This feature automatically integrates the Descriptor with the Registry while creation of the Shell at Repository. <br>
It also automatically removes the Descriptor from the Registry when the Shell is removed from the Repository. 

This feature is enabled when both of the below defined properties are set, i.e., no additional enabled/disabled property is required.

An example valid configuration:

```
basyx.aasrepository.feature.registryintegration = http://localhost:8050
basyx.externalurl = http://localhost:8081
```

## AAS Repository Integration with Authorized AAS Registry
If the target AAS Registry has authorization enabled, then the following properties needs to be configured in order to successfully integrate the Descriptor:

```
basyx.aasrepository.feature.registryintegration.authorization.enabled=true
basyx.aasrepository.feature.registryintegration.authorization.token-endpoint=http://localhost:9096/realms/BaSyx/protocol/openid-connect/token
basyx.aasrepository.feature.registryintegration.authorization.grant-type = <CLIENT_CREDENTIALS> or <PASSWORD>
basyx.aasrepository.feature.registryintegration.authorization.client-id = <client-id>
basyx.aasrepository.feature.registryintegration.authorization.client-secret = <client-secret>
basyx.aasrepository.feature.registryintegration.authorization.username=test
basyx.aasrepository.feature.registryintegration.authorization.password=test
basyx.aasrepository.feature.registryintegration.authorization.scopes=[]
```

An example authorized integration would be:
```
basyx.aasrepository.feature.registryintegration.authorization.token-endpoint = http://localhost:9096/realms/BaSyx/protocol/openid-connect/token
basyx.aasrepository.feature.registryintegration.authorization.grant-type = CLIENT_CREDENTIALS
basyx.aasrepository.feature.registryintegration.authorization.client-id = workstation-1
basyx.aasrepository.feature.registryintegration.authorization.client-secret = nY0mjyECF60DGzNmQUjL81XurSl8etom
```