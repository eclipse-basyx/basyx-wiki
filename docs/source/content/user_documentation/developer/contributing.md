# Contributing
For a contribution to Eclipse BaSyx, the Eclipse Contributor Agreement has to be signed.

## Eclipse Contributor Agreement
Eclipse BaSyx is using the Eclipse environment for managing code. Due to this, a valid Eclipse Account with a signed [Eclipse Contributor Agreement](https://www.eclipse.org/legal/ecafaq.php) is needed.

## Signed-Off
Additionally, your commit message does need to contain a "signed of by" message. This can be added by using the -s parameter when creating the commit. Below an example of a commit message containing both a change id and a signed of by is given:
```
 Fixes bug: TCP server threads were never closed
* Adds appropriate unit test
Signed-off-by: Frank Schnicke <frank.schnicke@iese.fraunhofer.de>
```

# Developing new Components
There are multiple ways of implementing BaSys 4.0 conforming components.

### Extending Existing Interfaces
For each component, there exist interfaces that can be implemented to realize e.g. new backends. These interfaces integrate seamless in the REST-API-Provider. Additionally, the already defined test suites for the different component types can easily be reused.

In consequence, this is the easiest and fastest way of introducing new components.

### Conforming to the REST-API
If the interfaces provided by BaSyx can't be used (e.g. because the component is implemented in a programming language currently not supported by BaSyx), it has to be ensured that the component is conforming to the defined REST-API and behavior.

For this, BaSyx provides a Technology Compatibility Kit (TCK). The TCKs for the components can be found in the repository in *components/tck*. For each component, there exists a TCK. Each TCK allows to generate a jar file that tests component functionality of arbitrary http endpoints. Each jar can be called in the following way:
```
java -jar $JAR $HTTP_ENDPOINT
```
where *$JAR* is the name of the component's TCK jar and *$HTTP_ENDPOINT* is the endpoint on which the component's REST API is available.

## Code Formatting
For the Java parts of Eclipse BaSyx, an Eclipse IDE Code Formatter profile is available: [File:BaSyx Formatting.zip](../developer/files/BaSyx_Formatting%20.zip).