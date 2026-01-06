# Annotated Relationship Element Value Only

An Annotated Relationship Element is serialized using the same format as a Relationship Element, with one additional property:

- **annotations**: Contains the value from `${AnnotatedRelationshipElement/annotations}` (optional)

The annotations property is an array where each item is serialized according to its specific data element type.

## Example
Consider an Annotated Relationship Element that defines a relationship between two assets with annotations:
```json
{
    "idShort": "AnnotatedAssetRelationship",
    "modelType": "AnnotatedRelationshipElement",
    "first": {
        "type": "Asset",
        "keys": [
            {
                "type": "Asset",
                "value": "urn:example:asset:firstasset"
            }
        ]
    },
    "second": {
        "type": "Asset",
        "keys": [
            {
                "type": "Asset",
                "value": "urn:example:asset:secondasset"
            }
        ]
    },
    "annotations": [
        {
            "idShort": "Annotation1",
            "modelType": "Property",
            "value": "This is an important relationship",
            "valueType": "xs:string"
        }
    ],
    "description": {
        "en": "An annotated relationship between two assets"
    },
    "displayName": {
        "en": "Annotated Asset Relationship"
    }
}
```

Its corresponding Value Only representation would be:
```json
{
    "AnnotatedAssetRelationship": {
        "first": {
            "type": "Asset",
            "keys": [
                {
                    "type": "Asset",
                    "value": "urn:example:asset:firstasset"
                }
            ]
        },
        "second": {
            "type": "Asset",
            "keys": [
                {
                    "type": "Asset",
                    "value": "urn:example:asset:secondasset"
                }
            ]
        },
        "annotations": [
            {
                "Annotation1": "This is an important relationship"
            }
        ]
    }
}
```