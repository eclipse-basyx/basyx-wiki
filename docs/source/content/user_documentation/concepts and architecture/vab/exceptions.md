# Exceptions

While accessing certain elements through the Virtual Automation Bus (VAB) using a model provider, exceptions would be generated in error cases. There are in total four types of exceptions that could be generated in error cases while using the five primitives of the VAB to access the data. The message of the exception contains information of message type, text, and code.


The message type defines the type of the exception. The text describes the concrete reason why this exception is thrown. The code is inspired by HTTP codes that indicates the type of the exception. The example below illustrates the message structure in Json:

```yaml
{
  "success": false,
    "messages": [
          {
        "messageType": "Information",
        "text": "Asset Administration Shell not found",
        "code": "404"
          }
    ]
}
```

The following table demonstrates the details and causes of these exceptions.

|            Exception           | Error Code |                                                                                                                     Cause                                                                                                                    |
|:------------------------------:|:----------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| MalformedRequestException      | 400        | Exception is thrown if a request does not fit the current context. For example, if a registry receives an invalid descriptor or if an operation or a given VAB-path is invalid.                                                              |
| ResourceNotFoundException      | 404        | Exception is thrown if the target element (or its parent element) does not exist. For example, reading or updating a non-existing element, invoking a non-existing operation, or creating a new element under a non-existing parent element. |
| ResourceAlreadyExistsException | 422        | Exception is thrown if it is tried to create a resource which already exists.                                                                                                                                                                |
| ProviderException              | 500        | For all other cases that are not covered by the above exceptions, a general provider exception is thrown.                                                                                                                                    |