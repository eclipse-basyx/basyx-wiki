# TCP Mapping

## General Frame Format
Each *BaSyx* Native frame is divided into two fields. These fields define message size and message payload. Due to this, the receiver can create a appropriate sized buffer.

If a message is received with *size > Message Length*, an error is assumed and the message it is discarded.

|                 Length                 |      Field      |
|:--------------------------------------:|:---------------:|
| 4 Byte, LSB first                      | Payload Length  |
| Variable, as defined in Payload Length | Message payload |

## String Encoding
Strings are encoded in the following scheme:

|                 Length                |                   Field                  |
|:-------------------------------------:|:----------------------------------------:|
| 4 Byte, LSB first                     | String Length                            |
| Variable, as defined in String Length | String content, without null termination |

## Object Encoding
Collections/Maps are serialized to a string as defined in the JSON serialization and send as a string as defined above.

## Primitive Mapping
For a detailed description of the primitives, see the VAB [documentation](index.md#technology-independent-vab-element-interface).

## RETRIEVE

### Request

|   Length   |           Field           | Value |
|:----------:|:-------------------------:|:-----:|
| 1 Byte     | Command                   | 0x01  |
| <variable> | Path to element as string |       |

### Response

|   Length   |           Field          |
|:----------:|:------------------------:|
| 1 Byte     | Result                   |
| <variable> | Value serialized as JSON |

Currently, the result will always be *0x00* with exceptions encoded in the returned string.

### Exceptions
If the property specified in the path or one of its parent elements does not exist, a ResourceNotFound Exception will be returned.

If the parent element of the specified property is a list, a ResourceNotFound Exception will be returned.

If another error occurs and the property can't be retrieved, a MalformedRequest Exception will be returned.

## UPDATE

### Request

|   Length   |           Field           | Value |
|:----------:|:-------------------------:|:-----:|
| 1 Byte     | Command                   | 0x02  |
| <variable> | Path to element as string |       |
| <variable> | Value serialized as JSON  |       |

### Response
| Length     | Field                    |
|------------|--------------------------|
| 1 Byte     | Result                   |
| <variable> | Value serialized as JSON |

Currently, the result will always be *0x00* with exceptions encoded in the returned string.

### Exceptions
If the parent element of the property specified in the path is a list, a ResourceNotFound Exception is returned.

If another error occurs while trying to set the property, a MalformedRequest Exception is returned.

## CREATE

### Request

| Length     | Field                     | Value |
|------------|---------------------------|-------|
| 1 Byte     | Command                   | 0x03  |
| <variable> | Path to element as string |       |
| <variable> | Value serialized as JSON  |       |

### Response

| Length     | Field                    |
|------------|--------------------------|
| 1 Byte     | Result                   |
| <variable> | Value serialized as JSON |

Currently, the result will always be 0x00 with exceptions encoded in the returned string.

### Exceptions
If one of the parent elements specified in the path does not exist, a ResourceNotFound exception will be returned.

If the property already exists, a ResourceAlreadyExists exception will be returned.

If the new property could not be created, a MalformedRequest exception will be returned.

## DELETE
There are two variants of delete: Deleting a value from a path and deleting a value from a Collection in a given path. In the latter case, the object to be deleted will be passed as JSON string.

### Request

|   Length   |                             Field                            | Value |
|:----------:|:------------------------------------------------------------:|:-----:|
| 1 Byte     | Command                                                      | 0x04  |
| <variable> | Path to element as string                                    |       |
| <variable> | Optional Object to be deleted from collection as JSON string |       |

### Response

| Length | Field  |
|--------|--------|
| 1 Byte | Result | 

Currently, the result will always be 0x00 with exceptions encoded in the returned string.

### Exceptions
If the property specified in the path or one of its parent elements does not exist, a PropertyNotFound exception is returned.

If the property could not be deleted, a MalformedRequest exception is returned.

## INVOKE

### Request

|   Length   |              Field              | Value |
|:----------:|:-------------------------------:|:-----:|
| 1 Byte     | Command                         | 0x05  |
| <variable> | Path to operations as string    |       |
| <variable> | Return value serialized as JSON |       |

### Response

|   Length   |           Field          |
|:----------:|:------------------------:|
| 1 Byte     | Result                   |
| <variable> | Value serialized as JSON |

Currently, the result will always be *0x00* with exceptions encoded in the returned string.

### Exceptions
If the property specified in the path or one of its parent elements does not exist, a PropertyNotFound exception is returned.

If invoke is called on an object that is not a function, a ProviderException will be returned.