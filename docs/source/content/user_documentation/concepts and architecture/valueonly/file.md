# File Value Only

A File is serialized as a JSON object containing two properties:

- **contentType**: The MIME type of the file
- **value**: A URI, path, or reference to the file location (may be technology-dependent and non-user readable)

## Example
Consider a File representing a configuration file:
```json
{
    "idShort": "ConfigFile",
    "modelType": "File",
    "contentType": "text/plain",
    "value": "file://config.txt",
    "description": {
        "en": "A sample configuration file"
    },
    "displayName": {
        "en": "Configuration File"
    }
}```

Its corresponding Value Only representation would be:
```json
{
    "contentType": "text/plain",
    "value": "file://config.txt",
}
```