# Hashmap Provider 

The HashMap provider is one of the basic providers in the BaSyx SDK for generic models. A HashMap serves as the root element for storing the contained data. By allowing child elements to be HashMaps and Collections, arbitrary hierarchical objects can be represented. Thus, the [Virtual Automation Bus](../../../vab/index.md) does not only support BaSys components but can also handle other data structures. Consider the following example:

```yaml
{
	"name" : "MyElement",
	"operation" : calculateSomething(),
	"data" : {
		"type" : "boolean",
		"value" : true
	} 
}
```

Internally, there is a reference to a single HashMap with three entries: *name, operation and data*. The first two are single elements directly stored in the root HashMap, whereas the last one is an additional HashMap containing two basic data elements.