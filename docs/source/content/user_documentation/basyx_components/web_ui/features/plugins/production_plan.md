# Production Plan

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Production Plan Submodels with their steps, actions, and statuses  
> **so that** I can monitor the execution progress of a production order at a glance.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- `https://smartfactory.de/semantics/submodel/ProductionPlan#1/0`

## Feature Overview

The Production Plan plugin provides a structured visualization of production plans defined by the **SmartFactory Kaiserslautern (SFKL)** Submodel template. It renders the hierarchical structure of a production order — broken down into steps and their associated actions — and displays the current execution status at every level.

The plugin gives operators and engineers a clear overview of which steps and actions have been completed, are in progress, or are still pending, as well as whether the overall plan has finished.

```{figure} ./images/production_plan.png
---
width: 50%
alt: Production Plan Plugin
name: production_plan_plugin
---
Production Plan Plugin showing steps, actions, and their statuses
```

## Key Features

- **Plan status indicator**: Shows the overall `IsFinished` status of the entire production plan
- **Step-by-step breakdown**: Lists all production steps with their title, station, enterprise, and workcentre assignment
- **Step status**: Displays the current status of each step (e.g. `open`, `executing`, `done`)
- **Action listing**: Expands each step to show its actions with their individual title and status
- **Machine assignment**: Shows the `MachineName` for each action where available

## Usage

1. Navigate to a Submodel with the Production Plan semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The plugin displays the overall plan completion status at the top
4. Each production step is shown with its title and current status
5. Expand a step to inspect its individual actions and their statuses

## Submodel Structure

The plugin expects the following structure, based on the SFKL Production Plan Submodel template:

### Top-level Elements

| idShort | Type | Description |
|---------|------|-------------|
| `IsFinished` | `Property (xs:boolean)` | Overall completion flag for the production plan |
| `Step00`, `Step01`, … | `SubmodelElementCollection` | One or more production steps |

### Step Structure

Each step collection contains:

| idShort | Type | Description |
|---------|------|-------------|
| `StepTitle` | `Property (xs:string)` | Human-readable name of the step |
| `Status` | `Property (xs:string)` | Execution status of the step |
| `Station` | `Property (xs:string)` | Target station for the step |
| `Enterprise` | `Property (xs:string)` | Enterprise responsible for the step |
| `Workcentre` | `Property (xs:string)` | Workcentre assigned to the step |
| `Actions` | `SubmodelElementCollection` | Collection of actions within the step |
| `Scheduling` | `SubmodelElementCollection` | Optional scheduling information |
| `InitialState` | `SubmodelElementCollection` | Optional initial state definition |
| `FinalState` | `SubmodelElementCollection` | Optional final state definition |

#### Scheduling Fields (optional)

| idShort | Type | Description |
|---------|------|-------------|
| `StartDateTime` | `Property (xs:string)` | Planned start date and time |
| `EndDateTime` | `Property (xs:string)` | Planned end date and time |
| `SetupTime` | `Property (xs:string)` | Required setup time |
| `CycleTime` | `Property (xs:string)` | Cycle time for the step |

### Action Structure

Each action inside the `Actions` collection contains:

| idShort | Type | Description |
|---------|------|-------------|
| `ActionTitle` | `Property (xs:string)` | Human-readable name of the action |
| `Status` | `Property (xs:string)` | Execution status of the action |
| `MachineName` | `Property (xs:string)` | Optional machine assigned to the action |
| `InputParameters` | `SubmodelElementCollection` | Optional input parameters |
| `FinalResultData` | `SubmodelElementCollection` | Optional result data after execution |
| `Preconditions` | `SubmodelElementCollection` | Optional preconditions |
| `Effects` | `SubmodelElementCollection` | Optional effects |
| `SkillReference` | `ReferenceElement` | Optional reference to the executing skill |

## Status Values

The `Status` property on both steps and actions uses string values. Typical values defined by the SFKL template are:

- `open` – not yet started
- `executing` – currently being executed
- `done` – successfully completed
- `error` – execution failed
