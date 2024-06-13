# AAS Environment Upload Endpoint

AAS packages (XML, JSON, AASX) can be uploaded as multipart/form-data via POST request using the `/upload` endpoint. Please note that the following MIME types are expected for the respective file uploads:
* AASX: application/asset-administration-shell-package
* JSON: application/json
* XML: application/xml
    
The upload follows the same rules as the preconfiguration in terms of handling existing AAS, submodels and concept descriptions. In order for the file to be recognized correctly, please make sure that its MIME type is properly configured.

```{note}
If the size of the AAS environment file (XML, JSON or AASX) exceeds the default limit given below, it is important to set the following two properties in the application.properties file, depending on the size of the file to be uploaded:

	spring.servlet.multipart.max-file-size (default 1 MB)
	spring.servlet.multipart.max-request-size (default 10 MB)
```
