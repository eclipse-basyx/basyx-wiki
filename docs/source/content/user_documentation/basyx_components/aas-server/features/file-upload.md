# File Upload Endpoint
## User Story & Use Case
*As AAS Components user*

*I want to upload files to "File" SubmodelElements via a dedicated HTTP/REST endpoint*

*so that I can exchange files with others via the Submodel interfaces without having to use a third-party file server.*

This feature can be used to upload files to any "File" SubmodelElement in a submodel hosted at the AAS Server Component. When uploading files to a File SubmodelElement, the AAS Server automatically updates the value to point to the new file location.

## Feature Overview
If this feature is enabled, it is possible to use the following endpoint for uploading the file via multipart form upload with an HTTP-POST request:
```
http://<server>:<port>/<contextPath>/shells/<aas-id>/.../<file-idShort>/upload
```
A file has to be included as an entry in the multipart form data upload. The entry **must** have a non-empty name like e.g. "file". The following screenshot shows an example in Postman:

![Sme-file-upload-postman.PNG](./images/Sme-file-upload-postman.png)

Here, we gave the entry the name "file". Make sure that "form-data" is selected!

## Feature Configuration
This feature is enabled by default. There is not further need for configuration.