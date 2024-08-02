# Preconfiguration of AAS Packages
AAS Packages can be preconfigured via the _basyx.environment_ property in the configuration (`application.properties`) file.

The feature supports both preconfiguring explicit files (e.g., file:myDevice.aasx) as well as directories (e.g., file:myDirectory) that will be recursively scanned for serialized environments.

You can specify multiple files and directories by separating them with a comma:
```properties
basyx.environment=file:myDevice.aasx, file:myDirectory, file:myOtherDevice.json, file:myXmlDevice.xml
```

```{warning}
Collision of Submodel and AAS IDs in the preconfigured packages will lead to an error.

For ConceptDescriptions ID collisions will be ignored since they are assumed to be identical. Only the first occurance of a ConceptDescription with the same Id will be uploaded.

Further ConceptDescriptions with the same Id will only lead to a warning in the log. 
```

## Preconfiguration of AAS Packages With Authorization Enabled
If you want to use a preconfigured environment with authorization, you need to set the following options as well:

```
basyx.aasenvironment.authorization.preconfiguration.token-endpoint = <Endpoint to the KeyCloak Server>
basyx.aasenvironment.authorization.preconfiguration.grant-type = <Grant Type>
basyx.aasenvironment.authorization.preconfiguration.client-id = <ClientID>
basyx.aasenvironment.authorization.preconfiguration.client-secret= <Client Secret>
basyx.aasenvironment.authorization.preconfiguration.username = <Username>
basyx.aasenvironment.authorization.preconfiguration.password = <Password>
basyx.aasenvironment.authorization.preconfiguration.scopes = <Scopes>
```

An example authorized preconfiguration would be:
```
basyx.aasenvironment.authorization.preconfiguration.token-endpoint = http://localhost:9096/realms/BaSyx/protocol/openid-connect/token
basyx.aasenvironment.authorization.preconfiguration.grant-type = CLIENT_CREDENTIALS
basyx.aasenvironment.authorization.preconfiguration.client-id = workstation-1
basyx.aasenvironment.authorization.preconfiguration.client-secret = nY0mjyECF60DGzNmQUjL81XurSl8etom
```