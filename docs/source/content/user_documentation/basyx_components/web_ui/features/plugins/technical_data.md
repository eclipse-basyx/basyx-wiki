# Technical Data

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Technical Data Submodels in an expandable panel view  
> **so that** I can easily access and understand technical specifications and parameters.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- **V1.2**: `https://admin-shell.io/ZVEI/TechnicalData/Submodel/1/2`

## Feature Overview

The Technical Data plugin provides a specialized visualization for Technical Data Submodels according to the IDTA specification. It displays technical specifications, parameters, and characteristics in an expandable panel view, organizing complex technical information in a logical and accessible manner.

```{figure} ./images/technical_data.png
---
width: 100%
alt: Technical Data Plugin
name: technical_data_plugin
---
Technical Data Plugin
```

## Key Features

- **Expandable Panel View**: Technical parameters organized in collapsible sections
- **Hierarchical Structure**: Properties grouped by categories (General, Electrical, Mechanical, etc.)
- **Units and Values**: Clear display of parameter values with their units
- **Property Metadata**: Shows data types, constraints, and descriptions
- **Multi-language Support**: Technical terms and descriptions in multiple languages
- **Specifications and Ranges**: Display of min/max values, tolerances, and typical values

## Usage

1. Navigate to a Submodel with the Technical Data semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The plugin displays technical information in an expandable panel view
4. Click on panel headers to expand or collapse parameter groups
5. View detailed information for each technical parameter:
   - Parameter name and description
   - Value and unit of measurement
   - Min/max ranges and tolerances
   - Data type and format

```{figure} ./images/technical_data_detail.png
---
width: 80%
alt: Technical Data Detail View
name: technical_data_detail
---
Detailed Technical Parameter View
```

## Common Technical Data Categories

### General Technical Properties
- Product dimensions (length, width, height)
- Weight and mass
- Material specifications
- Manufacturing date and location

### Electrical Properties
- Voltage ratings (min/max/nominal)
- Current ratings
- Power consumption
- Frequency specifications
- Resistance, capacitance, inductance

### Mechanical Properties
- Torque specifications
- Force ratings
- Pressure ratings
- Speed and acceleration limits
- Load capacities

### Environmental Properties
- Operating temperature range
- Storage temperature range
- Humidity specifications
- IP protection ratings
- Altitude limitations

### Performance Characteristics
- Efficiency ratings
- Accuracy and precision
- Response times
- Throughput specifications
- Cycle times

## Data Organization

Technical data is typically organized in a hierarchical structure:

1. **Main Categories**: Top-level groupings (e.g., "Electrical Properties", "Mechanical Properties")
2. **Sub-categories**: More specific groupings (e.g., "Input Voltage", "Output Current")
3. **Individual Parameters**: Specific technical values with units and constraints

## References

- [IDTA Technical Data V1.2 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2022/10/IDTA-02003-1-2_Submodel_TechnicalData.pdf)
