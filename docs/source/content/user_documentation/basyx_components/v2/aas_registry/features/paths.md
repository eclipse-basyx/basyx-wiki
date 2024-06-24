# Paths

This project utilizes the [simple-path-generator plugin](../basyx.aasregistry-plugins/README.md) to generate a builder Java class. This class is designed to work with the AAS registry client, enabling it to reference a field in an AssetAdministrationShellDescriptor document.

To use the path builder class, specify this dependency in your POM file with an appropriate version:

```xml
<dependency>
	<groupId>org.eclipse.digitaltwin.basyx</groupId>
	<artifactId>basyx.aasregistry-paths</artifactId>
</dependency>
```

Look at the API client project to see how the usage in source code.