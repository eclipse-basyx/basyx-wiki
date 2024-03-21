# Lambda provider

The Lambda provider is one of the basic providers in the BaSyx SDK for generic models. It is based on the [HashMap provider](./hashmap_provider.md) and therefore also uses HashMaps for the internal representation of data. In addition to the functionalities of this provider, the Lambda provider also enables dynamic property resolution. Both implement the same interface, so depending on the required functionalities they can be used interchangeably.

### Dynamic Property Resolution

The following sequence illustrates a typical use case for the Lambda provider. The value of a property in a given model is not available locally, but can be retrieved from an external resource like a database or a web server. For any given path the provider resolves each path element separately until the desired value has been returned. So first, the provider retrieves the *"data"* element from the root HashMap and checks, if it is a LambdaProperty. In this case, the property resolves its value by calling a previously specified function that is associated with it. In the given example, it connects to a web server and parses the value from the response. Thus, the result can be returned for further processing.


![An example showing how the VABLambdaProvider can resolve properties using external web resources](./images/VABLambdaValueResolution.png)

Other providers like the [SQL Submodel provider](sql_submodel_provider.md) rely on this functionality to be able to persistently store properties. Apart from HashMaps, multiple sources of data can be supported in this way.