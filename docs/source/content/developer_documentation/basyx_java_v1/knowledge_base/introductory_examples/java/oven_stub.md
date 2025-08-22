# Oven stub
This stub code realizes an interface to an oven and a dummy implementation for the example code that can be executed without any hardware.


The oven interface defines common interface functions to access to oven heater function and the oven temperature sensor function. It illustrates the ability to define generic interfaces for common aspects of assets.
```java
/**
 * Oven containing a heater and a temperature sensor
 */
public interface IOven {
 
	public Heater getHeater();
 
	public TemperatureSensor getSensor();
}
```

The oven stub is used during the example.
```java
/**
 * Oven containing a heater and a temperature sensor
 */
public class Oven implements IOven {
	private Heater heater;
	private TemperatureSensor sensor;
 
 
	public Oven() {
		heater = new Heater();
		sensor = new TemperatureSensor(heater);
	}
 
	public Heater getHeater() {
		return heater;
	}
 
	public TemperatureSensor getSensor() {
		return sensor;
	}
}
```