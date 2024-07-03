# Registry Integration
This feature automatically integrates the Descriptor with the Registry while creation of the Submodel at the Repository. <br>
It also automatically removes the Descriptor from the Registry when the Submodel is removed from the Repository.

To enable this feature, the following two properties should be configured:

```
basyx.submodelrepository.feature.registryintegration = {Submodel-Registry-Base-Url}
basyx.externalurl = {Submodel-Repo-Base-Url}
```

This feature is enabled when both of the above defined properties are configured, i.e., no additional enabled/disabled property is required.
