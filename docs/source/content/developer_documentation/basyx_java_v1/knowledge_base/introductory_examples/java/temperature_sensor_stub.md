# Temperature sensor stub
This stub code realizes an interface to a temperature sensor. It uses the generic sensor interface that provides access to a single value.


The ISensor interface defines common interface functions to access a sensor.
```java
/**
 * The sensor interface enables reading of one sensor value
 */
public interface ISensor {
 
	public double readValue();
 
}
```
The TemperatureSensor stub is used during the example. It implements a very basic simulation model for the oven temperature.
```java
/**
 * A sensor for reading a temperature value that is dependent on a heater
 */
public class TemperatureSensor implements ISensor {
	private final double maxTemperature = 50;
	private final double minTemperature = 20;
	private final double changeRate = 0.1d;
 
	private double currentTemperature = 20.0;
 
	public TemperatureSensor(final Heater heater) {
 
		// Start a new Thread that updates the temperature in every tick
		new Thread(() -> {
			while (true) {
				try {
					Thread.sleep(100);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				double targetTemperature = minTemperature;
				if (heater.isActive()) {
					targetTemperature = maxTemperature;
				}
				currentTemperature = (1 - changeRate) * currentTemperature + changeRate * targetTemperature;
			}
		}).start();
	}
 
	public double readValue() {
		return currentTemperature;
	}
}
```