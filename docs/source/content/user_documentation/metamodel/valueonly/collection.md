# Submodel Element Collection Value Only

A Submodel Element Collection is serialized as a JSON object where:

- **Key**: The `idShort` of each Submodel Element within the collection
- **Value**: The actual value of that Submodel Element

## Example
Consider a Submodel Element Collection representing various sensor readings:
```json
{
    "idShort": "SensorReadings",
    "modelType": "SubmodelElementCollection",
    "description": {
        "en": "A collection of sensor readings"
    },
    "displayName": {
        "en": "Sensor Readings"
    },
    "value": [
    {
        "idShort": "Temperature",
        "modelType": "Property",
        "value": 22.5,
        "valueType": "xs:double"
    },
    {
        "idShort": "Humidity",
        "modelType": "Property",
        "value": 60,
        "valueType": "xs:integer"
    }
    ]
}
```

Its corresponding Value Only representation would be:
```json
{
    "Temperature": 22.5,
    "Humidity": 60
}
```

Here you can see that in the Value Only representation, only the values of the Submodel Elements within the collection are included, omitting all other metadata. This allows for efficient data transfer and quick access to the current values of the Submodel Element Collection.
