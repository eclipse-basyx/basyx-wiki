# Submodel Value Only

A Submodel is serialized containing only the values of its Submodel Elements, without any metadata such as descriptions, data types, or semantic information.

This format is particularly useful for scenarios where applications need to frequently update or retrieve the current values while minimizing data transfer overhead.

## Example
Consider a Submodel representing the temperature and humidity of a sensor:
```json
{
  "idShort": "EnvironmentSensor",
  "modelType": "Submodel",
  "id": "urn:example:submodel:environmentsensor",
  "administration": {
    "version": "1.0",
    "revision": "0"
  },
  "description": {
    "en": "A Submodel representing environmental sensor data"
  },
  "displayName": {
    "en": "Environment Sensor"
  },
  "submodelElements": [
    {
      "idShort": "Temperature",
      "value": 22.5
    },
    {
      "idShort": "Humidity",
      "value": 60
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

Note that in the Value Only representation, only the values of the Submodel Elements are included, omitting all other metadata. This allows for efficient data transfer and quick access to the current values of the Submodel.