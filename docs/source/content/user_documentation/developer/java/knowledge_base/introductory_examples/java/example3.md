# Example 3
Previously, Example 1 and 2 had set up the connection of the oven to the VAB. Through this connection, the oven is controllable regardless of location and protocol.

However, the service invocation is still custom made and may differ from oven to oven. Thus, an abstraction of service interface is needed. This is done by the [Control Component](../../user_documentation/controlcomponent.md).

In this example, a control component for the oven is created by extending the *SimpleControlComponent* class of the Components project.

## Example Code
Again, the code is separated between local and remote code. First, the Control Component is set up. Please note, that in this tutorial it is not registered at the Registry. This is done to showcase how to connect to known entities on the VAB that for one reason or another are not registered.

First, in *startMyControlComponent()* the control component is created and hosted on a TCP server. Next, the code connects to the Control Component via direct address input and controls it via the [Control Component VAB API mapping](../../user_documentation/API/control-components.md).

```java
import org.eclipse.basyx.models.controlcomponent.ControlComponent;
import org.eclipse.basyx.models.controlcomponent.ExecutionState;
import org.eclipse.basyx.vab.coder.json.connector.JSONConnector;
import org.eclipse.basyx.vab.modelprovider.VABElementProxy;
import org.eclipse.basyx.vab.modelprovider.api.IModelProvider;
import org.eclipse.basyx.vab.modelprovider.map.VABMapProvider;
import org.eclipse.basyx.vab.protocol.basyx.connector.BaSyxConnector;
import org.eclipse.basyx.vab.protocol.basyx.server.BaSyxTCPServer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
 
/**
 * The control component provides an additional abstraction for native device handling and has a specified interface.
 * It can also be connected to the virtual automation bus.
 * For more information on control components, see:
 * https://wiki.eclipse.org/BaSyx_/_Documentation_/_API_/_ControlComponent
 * 
 * There, the VAB API is specified:
 * https://wiki.eclipse.org/BaSyx_/_Documentation_/_API_/_ControlComponent#Virtual_Automation_Bus_.28VAB.29_implementation
 * 
 * In this HandsOn, a given control component for the virtual (proprietary) oven is utilized via the VAB.
 * 
 * Expected console output in this HandsOn:
 * - state outputs from the OvenControlComponent
 * - oven is activated and deactivated multiple times (not manually, but automatically using the control component this
 * time)
 * - temperature values at ~30
 * - the oven cooling down after the control component is finished
 */
public class Scenario3 {
	// Initializes a logger for the output
	private static final Logger logger = LoggerFactory.getLogger(Scenario3.class);
 
	public static void main(String[] args) throws Exception {
		// Create the virtual oven specific to this HandsOn
		Oven myOven = new Oven();
 
		// Write a function, that starts a control component for the virtual oven
		startMyControlComponent(myOven);
 
		// Connect to the control component, see service interface here
		// This code also shows how to directly connect to a known location without
		// using the Registry/ConnectionManager.
		// However, this assumes that the address of the Control Component will never
		// change
		VABElementProxy proxy = new VABElementProxy("", new JSONConnector(new BaSyxConnector("localhost", 4002)));
 
		// Select the operation mode for heating
		proxy.setValue("STATUS/OPMODE", OvenControlComponent.OPMODE_HEAT);
 
		// Start the selected operation in the control component
		proxy.invokeOperation("OPERATIONS/START");
		logger.info("Using the control component to start the HEAT operation");
		for (int i = 0; i < 10; i++) {
			Thread.sleep(1000);
			logger.info("CurrentTemperature: " + myOven.getSensor().readTemperature());
			// Return true, if the control component has completed its operation
			String currentState = (String) proxy.getValue("STATUS/EXST");
			if (currentState.equals(ExecutionState.COMPLETE.getValue())) {
				// Reset the control component
				proxy.invokeOperation("OPERATIONS/RESET");
				break;
			}
		}
 
		logger.info("Waiting for oven to cool down...");
		Thread.sleep(2500);
		logger.info("CurrentTemperature: " + myOven.getSensor().readTemperature());
	}
 
	public static void startMyControlComponent(Oven oven) {
		// Given is a local control component that can directly control the virtual oven device
		ControlComponent cc = new OvenControlComponent(oven);
 
		// Like the VAB model created before, the structure of the control component is a Map
		// Map ccModel = (Map) cc;
 
		// Create a server for the Control Component and provide it in the VAB (at port 4002)
		VABMapProvider ccProvider = new VABMapProvider(cc);
		// This time, a BaSyx-specific TCP interface is used.
		// Likewise, it is also possible to wrap the control component using a http servlet as before
		BaSyxTCPServer<IModelProvider> server = new BaSyxTCPServer<>(ccProvider, 4002);
		server.start();
	}
}
```

## Oven Control Component
For this example, a simple control component exposing the *HEAT* opmode is created. The Control Component activates and deactivates the oven depending on the temperature multiple times.

Please note, that the *OvenControlComponent* takes some shortcuts for simplicity's sake in the context of this example. For example, having the control component also be its own ChangeListener may not be viable for a real world application.

```java
import org.eclipse.basyx.models.controlcomponent.ControlComponentChangeListener;
import org.eclipse.basyx.models.controlcomponent.ExecutionMode;
import org.eclipse.basyx.models.controlcomponent.ExecutionState;
import org.eclipse.basyx.models.controlcomponent.OccupationState;
import org.eclipse.basyx.models.controlcomponent.SimpleControlComponent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
 
/**
 * Control Component for controlling the oven. Has an additional operation mode named HEAT.
 * This is a "black-box" example for a control component for the HandsOn.
 */
public class OvenControlComponent extends SimpleControlComponent implements ControlComponentChangeListener {
	private static final long serialVersionUID = 1L;
        private static final Logger logger = LoggerFactory.getLogger(OvenControlComponent.class);
 
	public static final String OPMODE_BASIC = "BSTATE";
	public static final String OPMODE_HEAT = "HEAT";
 
	private Oven oven;
 
	public OvenControlComponent(Oven oven) {
		this.oven = oven;
		addControlComponentChangeListener(this);
	}
 
	@Override
	public void onChangedExecutionState(ExecutionState newExecutionState) {
		logger.info("OvenControlComponent: new execution state: " + newExecutionState);
		if (newExecutionState == ExecutionState.EXECUTE) {
			if (this.getOperationMode().equals(OPMODE_HEAT)) {
				controlHeater();
			} else {
				setExecutionState(ExecutionState.COMPLETE.getValue());
			}
		}
	}
 
	protected void controlHeater() {
		new Thread(() -> {
			for (int i = 0; i < 50; i++) {
				if (oven.getSensor().readTemperature() < 30.0d) {
					oven.getHeater().activate();
				} else {
					oven.getHeater().deactivate();
				}
				try {
					Thread.sleep(100);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
			oven.getHeater().deactivate();
			setExecutionState(ExecutionState.COMPLETE.getValue());
		}).start();
	}
 
	@Override
	public void onVariableChange(String varName, Object newValue) {
	}
 
	@Override
	public void onNewOccupier(String occupierId) {
	}
 
	@Override
	public void onNewOccupationState(OccupationState state) {
	}
 
	@Override
	public void onChangedExecutionMode(ExecutionMode newExecutionMode) {
	}
 
	@Override
	public void onChangedOperationMode(String newOperationMode) {
	}
 
	@Override
	public void onChangedWorkState(String newWorkState) {
	}
 
	@Override
	public void onChangedErrorState(String newWorkState) {
	}
}
```

## Expected Output
The first output will be the info about the execution state of the OvenControlComponent, which will be **EXECUTE**. After this the heater will be deactivated and activated multiple times and log the current temperature at a few intervals. Once the execution state changes to **COMPLETE** the temperature will fall and the state will change to **IDLE** as the temperature falls again.

```
15:50:07.729 [org.eclipse.basyx.vab.protocol.basyx.server.VABBaSyxTCPInterface 1629726607727] INFO  i.OvenControlComponent - OvenControlComponent: new execution state: EXECUTE
Heater: activated
15:50:07.731 [main] INFO  i.Scenario3 - Using the control component to start the HEAT operation
Heater: deactivated
Heater: activated
...
15:50:08.735 [main] INFO  i.Scenario3 - CurrentTemperature: 31.27908533
...
15:50:09.744 [main] INFO  i.Scenario3 - CurrentTemperature: 30.035964578619193
...
15:50:13.160 [Thread-4] INFO  i.OvenControlComponent - OvenControlComponent: new execution state: COMPLETE
15:50:13.781 [main] INFO  i.Scenario3 - CurrentTemperature: 25.93672972478958
15:50:13.784 [org.eclipse.basyx.vab.protocol.basyx.server.VABBaSyxTCPInterface 1629726613784] INFO  i.OvenControlComponent - OvenControlComponent: new execution state: IDLE
15:50:13.785 [main] INFO  i.Scenario3 - Waiting for oven to cool down...
15:50:16.297 [main] INFO  i.Scenario3 - CurrentTemperature: 20.526168681839124
```
