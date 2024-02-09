# Operation Delegation
## User Story & Use Case
*As AAS Components user*

*I want to delegate operation calls to third-party servers*

*so that I can integrate operations hosted on other servers into the AAS Server component*

This feature can be used for example for integrating Operations implemented in other programming languages into the AAS Server component without the need of implementing the complete Submodel interface.

## Feature Overview
An operation is a specific type of submodel element that is capable of performing server-side functions. However, in certain environments this is not possible. Therefore, the operation can be delegated to an independent destination URL to be executed. The operation invocation request is defined on [swaggerhub](https://app.swaggerhub.com/apis/BaSyx/basyx_submodel_http_rest_api/v1#/Submodel/InvokeOperationByIdShort). The type and the number of the in and output variables is defined within the operation itself. An example request body is given below. The strong and italic formatted attribute(s) `value` is/are the value(s) to be processed by the operation.
```
{
   "requestId": "1",
   "timeout": 60,
   "inputArguments": [{
      "value": {
         "idShort": "in",
         "valueType": "integer",
         "value": 1,
         "modelType": {
            "name": "Property"
         }
      }
   }]
}
```
Alternatively to the full request body above, the raw data can simply be passed as an array of values to be processed by the operation. In this case, the response would also consist of raw data instead of a structured body.

1. To create an operation delegation, an AAS with a Submodel that has a Operation(-SubmodelElement) must be present.
    1. The Operation has neither input, output nor inout variables
    2. To achieve the Delegation functionality, a Qualifier of type "invocationDelegation" is added to the operation.
       - As value, the url to the desired operation must be given.
       - The url follows the pattern
      http://{server}:{port}/{contextPath}/{idShortPathToOperation}/invoke
      resp. it is the url for direct operation invocation.
       - Knowledge about the operation to be delegated to, with regard to the number and type of input and output parameters is assumed.


This achieves that operations can be delegated to endpoints of the same server as well as to external servers. For the frontend it remains completely transparent whether an operation was called directly or delegated.

## Feature Configuration
This feature is enabled by default and does not need any additional configuration.