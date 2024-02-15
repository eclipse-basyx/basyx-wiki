# Timer
The Timer trigger is used to generate message exchanges when a timer fires. It means that the configured route would start processing the message when the configured timer is triggered.

## Configuration
You can specify **"trigger"**: **"timer"** in **routes.json**. Apart from this, you have to specify the timer name as a trigger data inside **routes.json**.

### Sample Route Configuration with Timer
```
[
  {
    "datasource": "httpsource",
    "transformers": ["jsonataA"],
    "datasinks": ["ConnectedSubmodel/ConnectedPropertyB"],
    "trigger": "timer",
    "triggerData" : {
    	"timerName": "timer1"
    }
  }
]
```
When configuring the timer as a trigger, you have to include another configuration file i.e. **timerconsumer.json** (Sample Timer consumer configuration file below). For e.g. As the above sample route configuration shows httpsource as datasource and the trigger is timer, then there will be two consumer configuration files i.e.** httpconsumer.json** and **timerconsumer.json** along with other configuration files.

### Sample Timer Consumer Configuration
```
[
  {
    "uniqueId": "timer1",
    "fixedRate": true,
    "delay": 0,
    "period": 5000
  }
]
```
## Working Example
The integration example with **timer triggered** OPC UA as a data source, with two transformers JSONata and Jackson, and AAS as a data sink is on [GitHub DataBridge Example](https://github.com/eclipse-basyx/basyx-databridge/tree/main/databridge.examples/databridge.examples.opcua-jackson-jsonata-aas).