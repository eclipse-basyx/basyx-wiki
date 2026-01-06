# Property Value Only

A Property is serialized as a simple key-value pair:

- **Key**: The Property's `idShort`
- **Value**: The actual value of the Property

This format is particularly useful for scenarios where applications need to frequently update or retrieve the current value while minimizing data transfer overhead.

## Example
Consider a Property representing the status of a device:
```json
{
    "idShort": "DeviceStatus",
    "modelType": "Property",
    "value": "Operational",
    "valueType": "xs:string",
    "description": {
    "en": "The current status of the device"
    },
    "displayName": {
        "en": "Device Status"
    }
}
```

Its corresponding Value Only representation would be:
```json
{
    "DeviceStatus": "Operational"
}
```