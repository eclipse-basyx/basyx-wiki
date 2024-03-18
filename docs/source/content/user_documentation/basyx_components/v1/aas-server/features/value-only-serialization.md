# Value-only Serialization
## User Story & Use Case
*As AAS application developer*

*I want to retrieve the values of a Submodel's SubmodelElements in a key-value-pair format*

*so that I don't have to retrieve the complete Submodel every time I would like to check for updated values*


This feature enables developers to focus on only the Submodel's SubmodelElement values, thus only requiring an initial retrieval of meta-information.

## Feature Overview
The value-only serialization of a Submodel can be requested by a GET */submodel/value* of a submodel.


For each SubmodelElement, a value-only serialization is defined. Typically, this is the value defined in the "value" entry of the SubmodelElement's meta model. For a SubmodelElementCollection, the value-only serialization consists of the value-only serialization of the respective SubmodelElements contained in it.


For example, consider the following value-only serialization:
```
{
	"collection": {
		"valueA" : 5,
		"valueB" : false
	},
	"valueC": 100
}
```
A possible submodel returning this value-only serialization would have a property *valueC* with value *100* and a SubmodelElementCollection *collection* containing two properties, *valueA* with *value 5* and *valueB* with value *false*.

## Feature Configuration
This feature is enabled by default. There is not further need for configuration.