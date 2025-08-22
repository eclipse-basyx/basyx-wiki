# File System Provider

The FileSystem provider is one of the basic providers in the BaSyx SDK for generic models. Each instance of the provider is based on an abstract FileSystem which is the local file system by default. Here, it is possible to provide own implementations of other types of file system, too. Like the [HashMap provider](hashmap_provider.md) and the [Lambda provider](lambda_provider.md), it is possible to store arbitrary object types in this provider. The key difference between FileSystem providers and other providers is that operations are not supported. Consider the following example:

```yaml
{
	"name" : "MyElement",
	"data" : {
		"type" : "boolean",
		"value" : true
	},
	"description" : {
		"de" : "Dies is ein beliebiges Objekt",
		"en" : "This is an arbitrary object"
	}
}
```

The FileSystem provider serializes the content of each property and stores it in a file that is associated with the corresponding property path. The resulting file structure generated for the object by a FileSystem provider with the local root folder C:/root/ looks like this:

* C:/root/name (file)
* C:/root/data (directory)
    + C:/root/data/type (file)
    + C:/root/data/value (file)
* C:/root/description (directory)
    + C:/root/description/de (file)
    + C:/root/description/en (file)