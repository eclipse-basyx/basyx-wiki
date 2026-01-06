# Submodel Element List Value Only

A Submodel Element List is serialized as a JSON array where each element corresponds to the value of a Submodel Element within the list.

## Example
Consider a Submodel Element List representing a series of temperature readings (Note that List Elements do not have idShorts):
```json
{
    "idShort": "TemperatureReadings",
    "modelType": "SubmodelElementList",
    "description": {
        "en": "A list of temperature readings"
    },
    "displayName": {
        "en": "Temperature Readings"
    },
    "value": [
    {
        "modelType": "Property",
        "value": 22.5,
        "valueType": "xs:double",
    },
    {
        "modelType": "Property",
        "value": 23.0,
        "valueType": "xs:double",
    },
    {
        "modelType": "Property",
        "value": 21.8,
        "valueType": "xs:double",
    }
    ]
}```

Its corresponding Value Only representation would be:
```json
[
    22.5,
    23.0,
    21.8
]
```