# Reference Element Value Only

A Reference Element is serialized as a JSON object:

- **Key**: The Reference Element's `idShort`
- **Value**: The Reference Element's value in the Normal representation

## Example
Consider a Reference Element representing a reference to an external asset:
```json
{
    "idShort": "ExternalAssetReference",
    "modelType": "ReferenceElement",
    "value": {
        "type": "ExternalReference",
        "keys": [
            {
                "type": "Submodel",
                "value": "urn:example:submodel:externalsubmodel"
            }
        ],
        "referredSemanticId": {
            "type": "GlobalReference",
            "keys": [
                {
                    "type": "ConceptDescription",
                    "value": "urn:example:conceptdescription:externalasset"
                }
            ]
        }
    },
    "description": {
        "en": "A reference to an external asset"
    },
    "displayName": {
        "en": "External Asset Reference"
    }
}```

Its corresponding Value Only representation would be:
```json
{
    "ExternalAssetReference": {
        "type": "ExternalReference",
        "keys": [
            {
                "type": "Submodel",
                "value": "urn:example:submodel:externalsubmodel"
            }
        ],
        "referredSemanticId": {
            "type": "GlobalReference",
            "keys": [
                {
                    "type": "ConceptDescription",
                    "value": "urn:example:conceptdescription:externalasset"
                }
            ]
        }
    }
}
```