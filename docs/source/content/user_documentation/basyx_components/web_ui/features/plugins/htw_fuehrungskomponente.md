# HTW Führungskomponente (State Machine Control)

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize and interact with PackML state machines  
> **so that** I can control and monitor industrial automation equipment.

## Semantic ID

This plugin is activated when a Submodel or SubmodelElementCollection has the following semantic ID:

- `http://htw-berlin.de/smc_statemachine`

## Feature Overview

The HTW Führungskomponente (Control Component) plugin provides a specialized interface for interacting with PackML (Packaging Machine Language) state machines. It allows users to visualize the current state of industrial control components, trigger state transitions, and change operating modes, making it ideal for industrial automation scenarios.

```{figure} ./images/htw_fuehrungskomponente.png
---
width: 100%
alt: HTW Führungskomponente Plugin
name: htw_fuehrungskomponente_plugin
---
HTW Führungskomponente Plugin showing PackML State Machine
```

## Key Features

- **PackML State Machine Visualization**: Visual representation of all PackML states
- **State Transition Controls**: Buttons to trigger allowed state transitions
- **Operating Mode Management**: Switch between different operating modes
- **Current State Display**: Real-time indication of the current state
- **Transition History**: Log of recent state changes
- **Error State Handling**: Special handling and visualization of error states

## PackML State Machine

The plugin supports the standard PackML state model with the following states:

### Main States

- **Stopped**: Machine is stopped
- **Starting**: Machine is starting up
- **Idle**: Machine is ready but not executing
- **Execute**: Machine is executing its main function
- **Completing**: Machine is completing the current cycle
- **Complete**: Cycle is complete
- **Resetting**: Machine is resetting to initial state
- **Aborting**: Machine is aborting current operation
- **Aborted**: Operation has been aborted
- **Clearing**: Clearing errors and faults
- **Stopping**: Machine is stopping

### Operating Modes

- **Production**: Normal production operation
- **Maintenance**: Maintenance mode with restricted functionality
- **Manual**: Manual control mode

## Usage

1. Navigate to a Submodel or SubmodelElementCollection with the HTW Führungskomponente semantic ID
2. Open the **Visualization** tab
3. The plugin displays:
   - Current state (highlighted)
   - Available transitions (enabled buttons)
   - Current operating mode

### Triggering State Transitions

1. View the current state in the state diagram
2. Available transitions are shown as enabled buttons
3. Click a transition button to trigger the state change
4. The UI updates to reflect the new state

```{note}
Unavailable transitions are not shown
```

### Changing Operating Modes

1. Locate the operating mode selector
2. Click on the mode you wish to switch to
3. Confirm the mode change if required
4. The state machine behavior adapts to the selected mode

## Submodel Structure

The plugin expects Properties within the Submodel or SubmodelElementCollection that represent:

### State Information

- **CurrentState**: The current state of the state machine (e.g., "Execute", "Idle")
- **StateCode**: Numerical code representing the current state

### Transition Commands

- **Start**: Command to trigger Start transition
- **Stop**: Command to trigger Stop transition
- **Reset**: Command to trigger Reset transition
- **Abort**: Command to trigger Abort transition
- **Clear**: Command to trigger Clear transition
- **Hold**: Command to trigger Hold transition
- **Unhold**: Command to trigger Unhold transition
- **Suspend**: Command to trigger Suspend transition
- **Unsuspend**: Command to trigger Unsuspend transition

### Operating Mode

- **OperatingMode**: Current operating mode (Production, Maintenance, Manual, Setup)
- **ModeCommand**: Command to change operating mode

## Use Cases

### Production Line Control

- Start and stop production equipment
- Monitor current operational state
- Handle emergency stops and error conditions

### Equipment Maintenance

- Switch to maintenance mode
- Safely stop equipment for service
- Reset equipment after maintenance

### System Integration

- Integrate with MES (Manufacturing Execution Systems)
- Coordinate multiple machines in a production line
- Implement automated production workflows

### Testing and Commissioning

- Test state transitions during commissioning
- Verify proper state machine behavior
- Debug automation logic

## Integration with Control Systems

The plugin can interact with real control systems through:

- **AAS Operations**: State transitions implemented as AAS Operations
- **Property Updates**: State changes reflected in Property values
- **Event Subscriptions**: Real-time updates via AAS events
- **OPC UA Integration**: Bridge to OPC UA-based automation systems

## Safety Considerations

```{warning}
When using this plugin to control real industrial equipment:
- Ensure proper access control and authentication
- Implement safety interlocks in the control system
- Provide operator training on state machine operation
- Follow all applicable safety standards and regulations
- Test thoroughly in a safe environment before production use
```

## References

- [PackML Implementation Guide](https://www.omac.org/packml)
- HTW Berlin Control Component Research
