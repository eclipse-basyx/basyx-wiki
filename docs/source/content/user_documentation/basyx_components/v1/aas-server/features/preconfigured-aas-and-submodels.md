## Preconfigured AAS & Submodels
# User Story & Use Case
*As AAS Components user*

*I want to preconfigure AAS and Submodels*

*so that that AAS and Submodels are available on component startup and can be delivered together with the component*


By preconfiguring serialized AAS and Submodels, the AAS Server component can be tailored and be delivered alongside a sold asset. Customers then can easily integrate the tailored component in their infrastructure. For example, a resulting AASX file created with the AASX Package Explorer can be preconfigured.

# Feature Overview
The AAS Server component supports preconfiguring (multiple) serialized AAS & Submodels. Right now, AASX, JSON and XML serializations are supported.

# Feature Configuration
```
aas.source=/usr/share/config/myAAS.aasx
```
This loads the file myAAS.aasx into the server as soon as it is started. For input files, the json and xml serializations are supported as well:
```
aas.source=/usr/share/config/myAAS.xml
```
Additionally, it is possible to specify multiple aas sources using a JSON syntax:
```json
aas.source=["json/aas.json","aasx/aas.aasx","xml/aas.xml"]
```