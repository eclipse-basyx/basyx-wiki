# Heater stub
This stub code realizes an interface to an oven and a dummy implementation for the example code that can be executed without any hardware.


The heater interface defines common interface functions to control the oven.
```java
/**
 * The heater enables controlling of the oven
 */
public interface IHeater {
 
	public void activate();
 
	public void deactivate();
 
	public boolean isActive();
}
```
The heater stub is used during the example.

## Heater Code
```java
/**
 * Simple heater with two states: activated or deactivated
 *
 */
public class Heater implements IHeater {
	private boolean isActive = false;
 
	public void activate() {
		if (!isActive) {
			System.out.println("Heater: activated");
			isActive = true;
		}
	}
 
	public void deactivate() {
		if (isActive) {
			System.out.println("Heater: deactivated");
			isActive = false;
		}
	}
 
	public boolean isActive() {
		return isActive;
	}
}
```