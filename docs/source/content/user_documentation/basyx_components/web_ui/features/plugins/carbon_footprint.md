# Carbon Footprint

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Carbon Footprint Submodels with timelines and comparative charts  
> **so that** I can track and analyze the environmental impact of products over time.

## Semantic IDs

This plugin is activated when a Submodel has one of the following semantic IDs:

- **V0.9**: `https://admin-shell.io/idta/CarbonFootprint/CarbonFootprint/0/9`
- **V1.0**: `https://admin-shell.io/idta/CarbonFootprint/CarbonFootprint/1/0`

## Feature Overview

The Carbon Footprint plugin provides specialized visualizations for Product Carbon Footprint (PCF) data. It displays PCF values in a timeline view, allowing users to track emissions over time and compare different PCF calculations. Version 1.0 adds additional visualization options, including pie charts when PCF values share the same reference value.

```{figure} ./images/carbon_footprint.png
---
width: 100%
alt: Carbon Footprint Plugin
name: carbon_footprint_plugin
---
Carbon Footprint Plugin with Timeline View
```

## Key Features

### Version 0.9 Features
- **Timeline Visualization**: Display PCF values chronologically
- **PCF Metadata**: Show calculation methods, standards, and validity periods
- **Data Export**: Export PCF data for reporting

### Version 1.0 Additional Features
- **Pie Chart Visualization**: Compare PCF values when they share the same reference
- **Enhanced Metadata**: Additional information about calculation boundaries and assumptions
- **Comparison Mode**: Side-by-side comparison of multiple PCF calculations
- **Trend Analysis**: Visualize PCF trends over time

```{figure} ./images/carbon_footprint_pie.png
---
width: 80%
alt: Carbon Footprint Pie Chart
name: carbon_footprint_pie
---
Carbon Footprint Pie Chart (V1.0)
```

## Usage

1. Navigate to a Submodel with the Carbon Footprint semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The plugin displays PCF data in the timeline view by default
4. For V1.0 Submodels with compatible reference values:
   - Switch to pie chart view to see proportional breakdown
   - Compare multiple PCF calculations
5. Click on individual PCF entries to view detailed information:
   - CO2 equivalent values
   - Calculation methodology
   - Reference unit and functional unit
   - Validity period
   - Data quality indicators

```{figure} ./images/carbon_footprint_timeline.png
---
width: 100%
alt: Carbon Footprint Timeline
name: carbon_footprint_timeline
---
Carbon Footprint Timeline View
```

## PCF Information Displayed

### Basic PCF Data
- **PCF Value**: CO2 equivalent emissions (kg CO2e)
- **Reference Unit**: Unit to which the PCF value relates
- **Calculation Date**: When the PCF was calculated
- **Validity Period**: Time period for which the PCF is valid

### Calculation Details
- **Calculation Method**: Standard or methodology used (e.g., ISO 14067, GHG Protocol)
- **System Boundary**: Scope of the calculation (cradle-to-gate, cradle-to-grave, etc.)
- **Allocation Method**: How emissions were allocated to the product
- **Data Quality**: Assessment of input data quality

### Breakdown and Composition
- **Life Cycle Stages**: Emissions by stage (raw materials, production, transport, use phase, end-of-life)
- **Material Composition**: Contribution of different materials to total PCF
- **Process Contributions**: Emissions from specific production processes

### Additional Information
- **Exclusions**: Elements not included in the calculation
- **Assumptions**: Key assumptions made during calculation
- **Uncertainty**: Confidence intervals or uncertainty ranges
- **Verification Status**: Third-party verification information

## Visualization Options

### Timeline View (V0.9 and V1.0)
Shows all PCF calculations in chronological order, ideal for:
- Tracking PCF improvements over time
- Comparing current vs. historical PCF values
- Monitoring the impact of process changes

### Pie Chart View (V1.0 only)
Available when multiple PCF values share the same reference unit:
- Visual breakdown of PCF contributions
- Proportional comparison between components
- Easy identification of major emission sources

## Use Cases

### Product Development
- Track PCF changes throughout product development
- Identify opportunities for emissions reduction
- Compare design alternatives

### Supply Chain Management
- Compare PCF values from different suppliers
- Monitor supplier improvement efforts
- Make informed sourcing decisions

### Sustainability Reporting
- Generate PCF reports for stakeholders
- Track progress toward emissions reduction goals
- Support environmental claims and certifications

## References

- [IDTA Carbon Footprint V0.9 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2024/01/IDTA-2023-0-9-_Submodel_CarbonFootprint.pdf)
- [IDTA Carbon Footprint V1.0 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2025/03/IDTA-02023_Submodel_CarbonFootprint.pdf)
