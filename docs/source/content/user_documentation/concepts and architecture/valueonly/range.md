# Range Value Only

A Range is serialized as a JSON object with two properties:

- **min**: The minimum value of the Range
- **max**: The maximum value of the Range

## Example
Consider a Range representing acceptable temperature limits:
```json
{
    "idShort": "TemperatureRange",
    "modelType": "Range",
    "min": 15.0,
    "max": 25.0,
    "valueType": "xs:double",
    "description": {
        "en": "The acceptable temperature range"
    },
    "displayName": {
        "en": "Temperature Range"
    }
}```

Its corresponding Value Only representation would be:
```json
{
    "min": 15.0,
    "max": 25.0
}
```