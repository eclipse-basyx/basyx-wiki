# BaSyx URI ID Schema

Eclipse BaSyx uses unique IDs (URIs) to identify elements that are connected to the virtual automation bus. Therefore, Asset Administration Shells and sub models are identified by a specific and technology independent ID. The following illustrates the ID format that is proposed by Eclipse BaSyx. It resembles the ID format described by the Platform Industrie 4.0 initiative “Asset Administrative Shell in Detail”. In addition, other, internal ID formats may be used at any time, as long as no duplicate identifiers are used.

A BaSyx ID is defined as following: urn: <legalEntity>:<subUnit>:<subModel>:<version>:<revision>:<elementID>#<elementInstance>

The following example describes a valid ID for an asset administration shell: ``urn:de.FHG:devices.es.iese:aas:1.0:3:x-509#001.`` Its elements are the following:

| Legal entity:     | de.FHG          | This is the entity that is responsible for the element that is identified by the ID                                                      |
|-------------------|-----------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Sub unit:         | devices.es.iese | A sub unit of the entity, e.g. a department, a division. Qualified names are permitted. We propose using dots to separate sub unit names |
| Sub model:        | aas             | Identifies the kind of sub model. Sub model type aas refers to an Asset administration shell.                                            |
| Version:          | 1.0             | Version number of the element                                                                                                            |
| Revision:         | 3               | A revision counter that defines for example how often an element was changed or updated                                                  |
| ElementID:        | x-509           | An additional Element ID                                                                                                                 |
| Element instance: | 001             | The instance of the element that is described by this ID                                                                                 |

[This](../developer/basyx_java_v1/knowledge_base/examples/index.md#urn) BaSyx SDK example illustrates the creation of an URN identifier