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