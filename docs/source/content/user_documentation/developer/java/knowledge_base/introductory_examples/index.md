# Setting up a digital production with Eclipse BaSyx
The introductory examples provide a starting point for getting started with the Eclipse BaSyx Java SDK. The overall rationale of Eclipse BaSyx is to enable digital manufacturing processes. Digital manufacturing processes are fully digitized, i.e. they have digital representatives for assets, for the process itself, and for the products. Digital representatives cover all relevant aspects of their real-world counterpart. Eclipse BaSyx realizes these digital representatives with the Asset Administration Shell (AAS). The AAS is therefore a digital substitute for an entity that is relevant for a production process. The following examples introduce Eclipse BaSyx and illustrate the use of our middleware to create a digital representative of a manufacturing process.

In the following, for each SDK there are introductory examples provided, showcasing the different concepts in the respective SDK.

## Hello World via Docker
**[Disclaimer: development branch]** To get a first impression of the look and feel of the BaSyx infrastructure, within the examples a docker compose file is provided. It lets you build a basic BaSys infrastructure, consisting of a registry server, an AAS server and an AAS Web GUI. Setting it up is as simple as

1. checkout basyx-java-examples
> $ git clone https://github.com/eclipse-basyx/basyx-java-examples
2. navigate to basyx-java-examples
> $ cd basyx-java-examples
 * switch to development branch
> git checkout development
3. navigate to basyx.docker/simple-deployment-with-gui
> $ cd basyx.docker/simple-deployment-with-gui
4. run $ docker compose up

This deploys

* A registry server at http://localhost:4000/registry
* An AAS server at http://localhost:4001/aasServer
* An AAS Web GUI at http://localhost:3000/
To setup the AAS Web GUI with the registry, visit http://localhost:3000/ and paste the url http://localhost:4000/registry into the appropriate input field inside the main menu of the application.

More details can be found at Introductory Examples/Java/Step 5

## Java
The goal of the following examples is to introduce core concepts and the respective infrastructure components of the Eclipse BaSyx Java SDK in 8 steps. In these steps we will illustrate:

* [Virtual Automation Bus](../user_documentation/vab/index.md)
* [Asset Administration Shell](../user_documentation/aas.md)
* [Control Components](../user_documentation/controlcomponent.md)

The Virtual Automation Bus enables end-to-end connectivity. The Asset Administration Shell is the digital representative of a device. If the AAS only provides access to sensor data then it will be a digital shadow. If it also enables controlling of the real device, it is a digital twin. The control component can be implemented in a PLC controller, and provides a unified device interface.

**Precondition**: The example requires a successful installation of the [SDK](../download/java_setup.md) and the [components](../download/components_setup.md).

The following example illustrates Eclipse BaSyx by creating a digital twin for one device. The device is an oven that consists of a temperature sensor and of a heater. An application will display the current state of the oven and control its operation. The following links lead to a set of classes that we will be using for simulating the behavior of the oven and its devices to enable the self-contained execution of this example:

* [Oven](./java/oven_stub.md)
* [Heater](./java/heater_stub.md)
* [Temperature sensor](./java/temperature_sensor_stub.md)

**Basic Example**: There are currently 6 steps that illustrate the use of Eclipse BaSyx, each building upon the previous one. In the end, there will be a digitized oven with the ability to access its current state and to control its operation using Asset Administration Shells and Control Components.

* [Step 1](./java/step1.md) - Creating the digital manufacturing concept
* [Step 2](./java/step2.md) - Setting up the Eclipse BaSyx infrastructure
* [Step 3](./java/step3.md) - Creating (and testing) the oven Submodel
* [Step 4](./java/step4.md) - Providing the Submodel in the network via HTTP
* [Step 5](./java/step5.md) - Assembling the oven Asset Administration Shell and deploying it on the AAS server
* [Step 6](./java/step6.md) - Creating an application to connect to the oven through its AAS
* [Step 7](./java/step7.md) - Eventing via MQTT
* [Step 8](./java/step8.md) - Protect the Server from unauthorized access

**Additional steps**: The following steps illustrate additional activities and capabilities of the Eclipse BaSyx Java SDK in context of the oven example.

* [Step 1](./java/example1.md) - Creating and accessing an oven model with local VAB access
* [Step 2](./java/example2.md) - Providing the model via HTTP/REST and accessing the model remotely
    * [Step 2a](./java/example2a.md) - Providing the model via [BaSyxTCP](../user_documentation/vab/tcp_mapping.md)
    * [Step 2b](./java/example2b.md) - Providing the model via [BaSyxTCP](../user_documentation/vab/tcp_mapping.md) and connecting via a [gateway](../user_documentation/gateway.md)
* [Step 3](./java/example3.md) - Using a Control Component for unified service interfacing
* [Step 4](./java/example4.md) - Creating the AAS, registering it and exploring the HTTP-REST interface
* [Step 5](./java/example5.md) - Accessing the remote AAS through the SDK
* [Step 6](./java/example6.md) - Using the Off-the-Shelf-Components