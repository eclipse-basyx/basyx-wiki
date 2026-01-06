# Blob Value Only

A Blob is serialized as a JSON object containing two properties:

- **contentType**: The MIME type of the file
- **value**: The Base64 encoded content of the Blob

## Example
Consider a Blob holding a text:
```json
{
    "idShort": "TextBlob",
    "modelType": "Blob",
    "contentType": "text/plain",
    "value": "QmFTeXggaXMgdGhlIGJlc3QgbWlkZGxld2FyZQ==",
    "description": {
        "en": "A sample text blob"
    },
    "displayName": {
        "en": "Text Blob"
    }
}```

Its corresponding Value Only representation would be:
```json
{
    "contentType": "text/plain",
    "value": "QmFTeXggaXMgdGhlIGJlc3QgbWlkZGxld2FyZQ=="
}
```