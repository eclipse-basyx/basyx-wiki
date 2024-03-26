# JSON Serialization
Both the TCP and the HTTP mapping use a json serialization for objects send over the VAB. In the following, this json serialization is explained.

## Requirements
There are multiple requirements on the JSON serialization:

* Preserve type information, since JSON only knows a small set of types
* Be compatible to the JSON serialization defined in [Details of the Asset Administration Shell](https://www.zvei.org/en/subjects/industrie-4-0/details-of-the-asset-administration-shell/)
* Be compatible to the C#-SDK since it is not using the VAB

## Type Representation
The following types are taken as is from the JSON type scheme:

* string
* number (integer or double)
* object (i.e. map)
* boolean
* null
 Additionally, these types are introduced:

* ordered lists
* functions

## Functions
Functions are most commonly not serializable. Exception of this are Java functions, that can be represented by their byte code. However, there still needs to be an indication that a value is representing a function. This is done by passing this information in the *_basyxFunctionType* key. The allowed values are:

* lambda
* operation