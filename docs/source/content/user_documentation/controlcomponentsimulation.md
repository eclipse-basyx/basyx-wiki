**This information is work in progress as part of the BaSys 4.2 project. This section is preliminary and subject to change during the project.**

# Process Simulation with Control Components
Depending on the supported profile, a control component may specify an additional [execution mode for process simulation](./API/controlcomponentprofiles.md) (SIMULATE). When a control component is in simulation mode, it is expected to behave towards the controlling production process as if it were in automatic mode. However, requested operation modes from a production process neither have an effect on the physical asset nor on the physical product being build.

The simulation mode can thus be exploited during engineering for the virtual commissioning of a (changed) production process. A mixed operation of real and simulated components is in principle also possible, if one is able to establish the physical post-conditions of a simulated process step by other means, so that a subsequent real process step can be performed as expected.

A control component that does not support simulation can be surrogated by a pure virtual control component that mimic the input/output behavior of the actual component to a neccessary extend.

Depending on the purpose of the simulation, a different simulation depth is required for the internal implementation of the simulation mode in a control component. The deeper the simulation, the more complex the implementation of the simulation is.

If, for example, one wants to successfully advance a simulated process step deterministically, the simulated component or the simulated operation mode of a component only has to report an OK with any static process parameters back to the process control. If one wants to specifically ensure the resilience of the production process against faulty executions of a process step, the component in simulation mode must be able to realistically inject corresponding error situations on demand or randomly. In this context, rules for the alarm management of a component may have to be observed or triggered, and corresponding data streams may have to be simulated. In addition, physical cause-effect relationships can also be modeled.

In the [implementation section](./implementation/controlcomponentsimulation.md), we explain how to implement a simulation mode in 4 different ways and at different simulation depths using the [Java-based SDK for control components](https://github.com/dfkibasys/control-component).