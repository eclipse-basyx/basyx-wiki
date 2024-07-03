# Registry Integration
This feature automatically integrates the Descriptor with the Registry while creation of the Shell at Repository. <br>
It also automatically removes the Descriptor from the Registry when the Shell is removed from the Repository. 

This feature is enabled when both of the below defined properties are set, i.e., no additional enabled/disabled property is required.

An example valid configuration:

```
basyx.aasrepository.feature.registryintegration = http://localhost:8050
basyx.externalurl = http://localhost:8081
```
