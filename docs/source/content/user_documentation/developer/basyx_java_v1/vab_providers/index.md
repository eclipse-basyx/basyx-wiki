# Java SDK VAB Provider Overview

The low-level providers implements the five [Virtual Automation Bus primitives](../../../concepts%20and%20architecture/vab/index.md) create, delete, get, invoke and set in order to be able to interact with the contained model. Therefore, all providers implement the IModelProvider interface. By mapping the requested path to their internal structure all elements can be directly accessed. For a HashMap and Lambda provider the path is mapped to the hierarchy of HashMaps and other collections. The FileSystem provider on the other hand maps it to the directory and file structure based on the given abstract FileSystem.

![The VABHashMapProvider is an IModelProvider based on HashMaps](../vab_providers/images/VABProviders.png)


* [File System Provider](fileSystem_provider.md)
* [Hashmap Provider](hashmap_provider.md)
* [Lambda Provider](lambda_provider.md)
* [SQL Submodel provider](sql_submodel_provider.md)
* [VAB Providers Implementation](vab_providers_implementation.md)


```{toctree}
:hidden:
:maxdepth: 1 

fileSystem_provider
hashmap_provider
lambda_provider
sql_submodel_provider
vab_providers_implementation

```