# Value Only

In many scenarios, applications working with Asset Administration Shell (AAS) data already know the structure and meaning of a Submodel. Since attributes, structure, and semantics usually remain unchanged, transferring complete model information with every request is unnecessary. Metadata can still be requested separately using the Content modifier set to Metadata (see [IDTA-01002](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.1.1/index.html)).

The Value Only format is supported for the following types:

* [Submodel](submodel.md)
* [Submodel Element Collection](collection.md)
* [Submodel Element List](list.md)
* [Property](property.md)
* [Range](range.md)
* [File](file.md)
* [Blob](blob.md)
* [Reference Element](reference_element.md)
* [Relationship Element](relationship_element.md)
* [Annotated Relationship Element](annotated_relationship_element.md)

## Benefits

**Reduced Data Transfer**: Applications are typically interested only in current values. Sending just the values reduces transferred data and improves efficiency—especially important for devices with limited processing power or network bandwidth.

**Separation of Concerns**: Semantics and structure can be provided by one system (e.g., a database optimized for querying model information), while actual data values are delivered by another system (e.g., a device providing live runtime data).

**Efficient UI Updates**: By using separate requests for metadata and values, applications can build user interfaces efficiently and update displayed values quickly without repeatedly transferring static information.

```{hint}
For a more in-depth explanation see [IDTA Part 1: Metamodel v3.1.1](https://industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.1.1/mappings/mappings.html#value-only-serialization-in-json)
```

```{toctree}
:maxdepth: 1

submodel
collection
list
property
range
file
blob
reference_element
relationship_element
annotated_relationship_element

```
