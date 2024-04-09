# Step 3: Creating the oven Submodel
This step will create the oven Submodel and a test application for that Submodel. The AAS and its Submodels can be realized in different ways with Eclipse BaSyx:

* If the Submodel contains static data only, it can be deserialized from an AASX file, or from a JSON file that defines the Submodel structure and data.
* If the Submodel provides also dynamic data, but all dynamic data is pushed from outside the Submodel, e.g. from the device, the Submodel can be deserialized from an AASX file, or from a JSON file.
* If the Submodel also contains active parts, e.g. services or the ability to actively pull data from data sources, e.g. from the device, it can be created using the Eclipse BaSyx SDKs.

Submodels of the same AAS can be created by different means. In this example, we will illustrate the creation of an AAS and of the oven Submodel with the Java SDK. Communication between the oven and the edge device is via an analogues connection that encodes values as current, which must be periodically sampled by the edge device. Commands for controlling the oven are provided via individual digital lines. The edge device therefore needs to periodically sample input values, and set digital output lines to reflect commands to the oven. This device specific interface code is not part of the example. We define a Java interface that enables access to these functions, and that enables us to substitute the real-world edge device with a stub that simulates the device behavior to create a self-contained example.

```java
/**
 * Generic interface for sensors
 */
public interface ISensor {
 
	/**
	 * Read sensor value
	 * 
	 * @return The last sampled sensor value
	 */
	public double readValue();
}
```

The [temperature sensor stub](temperature_sensor_stub.md) that we are using in this example for testing implements this interface and therefore can be accessed through the readValue() function. The user of this interface therefore does not need to know whether he will be communicating with a real-world asset or with a simulated instance.


## Realizing the Submodel
Submodels define all domain and asset specific properties. We will therefore first define a Submodel for the oven. The oven Submodel defines two properties: The ID that identifies this heater, and the temperature that provides access to the current temperature from the temperature sensor. Two operations enable to activate and to deactivate the oven.

The ID of the oven will be a static value. It includes the idShort, a locally unique name, as well as the Identification that has to unique identifier.

```java
Submodel ovenSubmodel = new Submodel("oven", new ModelUrn("heater1"));
```

The temperature property provides access to the current temperature of the oven. As the oven in our case does provide a very simple interface, the Submodel samples the current temperature value whenever a temperature value is requested. This is realized with a function that is invoked whenever the property value is requested. For this reason, it uses the Oven interface [Oven](oven_stub.md).

```
// Create a dynamic property that can resolve its value during runtime
// 1. Create a supplier function that can determine the oven temperature using the sensor
Supplier<Object> lambdaReadFunction = () -> oven.getSensor().readValue();
 
// 2. Create a new empty Property
Property dynamicTemperatureProperty = new Property();
 
// 3. Set the id of the new Property
dynamicTemperatureProperty.setIdShort("temperature");
 
// 4. Use the AASLambdaPropertyHelper to add the Getter to the new Property
// NOTE: A setter function is not required (=> null), because a sensor temperature is "read only"
AASLambdaPropertyHelper.setLambdaValue(dynamicTemperatureProperty, lambdaReadFunction, null)
 
// 5. Add that lambda property to the model
ovenSubmodel.addSubmodelElement(dynamicTemperatureProperty);
```

The temperature is read through a call to the readValue() call of the sensor (obtained via getSensor()). Besides of properties, the Submodel also may export operations.

The Submodel will define two functions: An activate and an deactivate function. Both functions are created as lambda function objects and are placed in the operations map.
```java
// Add a function that activates the oven and implements a functional interface
Function<Object[], Object> activateFunction = (args) -> {
	oven.getHeater().activate();
	return null;
};
 
// Encapsulate the function in an operation
Operation activateOperation = new Operation(activateFunction);
 
// Set the id of the operation
activateOperation.setIdShort("activateOven");
 
// Add an operation that activates the oven and implements a functional interface
ovenSubmodel.addSubmodelElement(activateOperation);
 
 
// Add a function that deactivates the oven and implements a functional interface
Function<Object[], Object> deactivateFunction = (args) -> {
	oven.getHeater().deactivate();
	return null;
};
 
// Encapsulate the function in an operation
Operation deactivateOperation = new Operation(deactivateFunction);
 
// Set the id of the operation
deactivateOperation.setIdShort("deactivateOven");
 
// Add an operation that deactivates the oven and implements a functional interface
ovenSubmodel.addSubmodelElement(deactivateOperation);
```

## Putting everything together
The complete code is provided below:

```java
	public static Submodel createMyOvenModel(Oven oven) {
		// Create an empty Submodel
		Submodel ovenSubmodel = new Submodel();
 
		// Set its idShort
		ovenSubmodel.setIdShort("Oven");
 
		// Set its unique identification
		ovenSubmodel.setIdentification(new ModelUrn("heater1"));
 
		// Now we want to create a dynamic property that can resolve its value during runtime
		// 1. Create a supplier function that can determine the oven temperature using the sensor
		Supplier<Object> lambdaReadFunction = () -> oven.getSensor().readValue();
		// 2. Create a new empty Property
		Property dynamicTemperatureProperty = new Property();
		// 3. Set the id of the new Property
		dynamicTemperatureProperty.setIdShort("temperature");
		// 4. Use the AASLambdaPropertyHelper to add the Getter to the new Property
		// NOTE: A setter function is not required (=> null), because a sensor temperature is "read only"
		AASLambdaPropertyHelper.setLambdaValue(dynamicTemperatureProperty, lambdaReadFunction, null)
		// 5. Add that lambda property to the model
		ovenSubmodel.addSubmodelElement(dynamicTemperatureProperty);
 
		// Add a function that activates the oven and implements a functional interface
		Function<Object[], Object> activateFunction = (args) -> {
			oven.getHeater().activate();
			return null;
		};
		// Encapsulate the function in an operation
		Operation activateOperation = new Operation(activateFunction);
		// Set the id of the operation
		activateOperation.setIdShort("activateOven");
		// Add an operation that activates the oven and implements a functional interface
		ovenSubmodel.addSubmodelElement(activateOperation);
 
 
		// Add a function that deactivates the oven and implements a functional interface
		Function<Object[], Object> deactivateFunction = (args) -> {
			oven.getHeater().deactivate();
			return null;
		};
		// Encapsulate the function in an operation
		Operation deactivateOperation = new Operation(deactivateFunction);
		// Set the id of the operation
		deactivateOperation.setIdShort("deactivateOven");
		// Add an operation that deactivates the oven and implements a functional interface
		ovenSubmodel.addSubmodelElement(deactivateOperation);
 
		// Return the Submodel
		return ovenSubmodel;
	}
```

## Testing the Submodel
It always makes sense to create regression tests that ensure that changes do not have unwanted side effects. Therefore, a Submodel can be tested without an extensive BaSyx deployment. The first step when testing a Submodel is to warp it into a VABLambaProvider that enables access to this Submodel. The code below first creates the Submodel under test and then wraps it into a provider. The model connects to a simulated oven instance using the Oven stub.
``` java
// Create a model for an oven device.
Submodel myOvenModel = createMyOvenModel(new Oven());

Now, the model can be used to read/write values, and to execute lambda functions that e.g. preprocess data or access a simulation model during testing.

// Get the Identification of the Submodel
String id = myOvenModel.getIdentification().getId();
System.out.println("Heater id: " + id);
 
// The operations can be invoked via the model provider like this:
IOperation activateOperation = myOvenModel.getOperations().get("activateOven");
activateOperation.invoke();
```
## Conclusion
This second step did illustrate the creation of a Submodel for the oven. This is not yet a complete Asset Administration Shell but a specific domain model that describes the specific properties and services of the oven. The Submodel defines an interface that may be for all ovens that can be activated and deactivated, and that provide the current temperature. More complex systems will define multiple Submodels for their assets, and keep every Submodel focused on a specific aspect. Depending on the type of the asset, many Submodel types are possible, e.g. the nameplate, spare parts and their availability, sensor data, asset health, or offered services.