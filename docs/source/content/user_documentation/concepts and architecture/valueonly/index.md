# Value Only
In many scenarios, applications that work with Asset Administration Shell (AAS) data already know the structure and meaning of a Submodel. Its attributes, structure, and semantics usually do not change. Therefore, it is often unnecessary to transfer the complete model information with every request. If required, this metadata can still be requested separately by using the Content modifier set to Metadata (see IDTA-01002).

In most cases, applications are primarily interested in the current values of the modeled data. Sending only these values reduces the amount of transferred data and improves efficiency. This is especially important for devices or systems with limited processing power or limited network bandwidth.

This format also supports a clear separation of responsibilities. Semantics and structure can be provided by one system, such as a database optimized for querying model information. The actual data values can be delivered by another system, for example a device that provides live data at runtime.

By using two separate requests—one for metadata and one for values—applications can efficiently build a user interface and update displayed values quickly without repeatedly transferring static information.

[!] For a more in-depth explanation see [IDTA Part 1: Metamodel v3.1.1](https://industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.1.1/mappings/mappings.html#value-only-serialization-in-json)

# Available Value Only representations
The Value only format is supported for the following types:
- [Submodel](submodel.md)
- [Submodel Element Collection](submodel_element_collection.md)
- [Submodel Element List](submodel_element_list.md)
- [Property](property.md)
- [MultiLanguage Property](multilanguage_property.md)
- [Range](range.md)
- [File](file.md)
- [Blob](blob.md)
- [Reference Element](reference_element.md)
- [Relationship Element](relationship_element.md)
- [Annotated Relationship Element](annotated_relationship_element.md)