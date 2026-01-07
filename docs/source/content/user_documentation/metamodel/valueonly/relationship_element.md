# Relationship Element Value Only

A Relationship Element is serialized as a named JSON object, where the property name is the element's `${RelationshipElement/idShort}`.

The JSON object contains two properties:

- **first**: Contains the value from `${RelationshipElement/first}`
- **second**: Contains the value from `${RelationshipElement/second}`

Both values are serialized using the same format as a ReferenceElement.

## Example
Consider a Relationship Element that defines a relationship between two assets:

```json
{
    "idShort": "AssetRelationship",
    "modelType": "RelationshipElement",
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
    "description": {
        "en": "A relationship between two assets"
    },
    "displayName": {
        "en": "Asset Relationship"
    }
}
```

Its corresponding Value Only representation would be:

```json
{
    "AssetRelationship": {
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
        }
    }
}
```