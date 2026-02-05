# Carbon Footprint

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Carbon Footprint Submodels with timelines and comparative charts  
> **so that** I can track and analyze the environmental impact of products over time.

## Semantic IDs

This plugin is activated when a Submodel has one of the following semantic IDs:

- **V0.9**: `https://admin-shell.io/idta/CarbonFootprint/CarbonFootprint/0/9`
- **V1.0**: `https://admin-shell.io/idta/CarbonFootprint/CarbonFootprint/1/0`

## Feature Overview

The Carbon Footprint plugin enables the exchange of an asset's Carbon Footprint (CF) information between partners along the value chain. It aims to increase interoperability between manufacturers, users/consumers, and logistic partners who document, exchange, evaluate, or optimize environmental footprints. The CF data can be part of larger initiatives such as the Digital Product Passport (DPP) or the Product Environmental Footprint.

The plugin provides specialized visualizations for Product Carbon Footprint (PCF) data, supporting **multiple PCF values with different calculation methods and standards**. Each PCF value can use different standards, calculation methods, or assumptions, allowing comprehensive carbon footprint documentation.

```{figure} ./images/carbon_footprint.png
---
width: 100%
alt: Carbon Footprint Plugin
name: carbon_footprint_plugin
---
Carbon Footprint Plugin with Timeline View
```

## Key Features

### Core Capabilities

- **Multiple PCF Values**: Support for unlimited SubmodelElementCollections, each representing different calculation methods, standards, or assumptions
- **Timeline Visualization**: Display PCF values chronologically to track emissions over time
- **PCF Metadata**: Show calculation methods, standards, validity periods, and system boundaries
- **Multiple Standards Support**: Compatible with various calculation standards:
  - ISO 14044 (Life Cycle Assessment)
  - ISO 14067 (Carbon Footprint of Products)
  - ISO 14026 (Documentation requirements)
  - Greenhouse Gas Protocol
  - Product Category Rules (industry-specific)
  - PACT Framework (Pathfinder Framework Version 2.0)

### Version 1.0 Additional Features

- **Pie Chart Visualization**: Compare PCF values when they share the same reference unit

## Usage

1. Navigate to a Submodel with the Carbon Footprint semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The plugin displays PCF data in the timeline view by default, showing all available PCF values
4. View **multiple PCF calculations** using different standards and methods:
   - Each PCF value is represented as a separate SubmodelElementCollection
   - Different calculation methods, standards, and assumptions can be compared
5. For V1.0 Submodels with compatible reference values:
   - See pie chart card that visualizes and compares multiple PCF calculations
6. Access detailed information for each PCF entry:
   - CO2 equivalent values
   - Calculation methodology and standard used
   - Reference unit and functional unit
   - Validity period
   - System boundary (cradle-to-gate, cradle-to-grave, etc.)
   - Data quality indicators

## PCF Information Displayed

### Basic PCF Data

- **PCF Value**: CO2 equivalent emissions (kg CO2e)
- **Reference Unit**: Unit to which the PCF value relates
- **Calculation Date**: When the PCF was calculated
- **Validity Period**: Time period for which the PCF is valid

### Calculation Details

- **Calculation Method**: Standard or methodology used:
  - ISO 14044 (Life Cycle Assessment principles and framework)
  - ISO 14067 (Carbon Footprint of Products)
  - ISO 14026 (Principles and requirements for documentation)
  - Greenhouse Gas Protocol (Product Standard)
  - Product Category Rules (industry-specific guidelines)
  - PACT Framework (Pathfinder Framework Version 2.0)
  - Proprietary methods
- **System Boundary**: Scope of the calculation (cradle-to-gate, cradle-to-grave, gate-to-gate, etc.)
- **Allocation Method**: How emissions were allocated to the product
- **Data Quality**: Assessment of input data quality and uncertainty

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

### Value Chain Communication

- Exchange CF information between value chain partners
- Enable manufacturers, users/consumers, and logistic partners to collaborate
- Support Digital Product Passport (DPP) initiatives
- Contribute to Product Environmental Footprint reporting

### Limited Machine-Readable Communication

- Scan products to view essential Carbon Footprint information
- Access machine-readable metadata about PCF calculations
- Download detailed documentation (ISO 14026 compliant PDFs, certificates)
- Link to websites for comprehensive analysis

### Multi-Standard Comparison

- Compare PCF values calculated using different standards
- Evaluate impact of different calculation methods and assumptions
- Support product category rules for industry-specific calculations
- Assess lifecycle phase contributions (cradle-to-gate vs. cradle-to-grave)

### Product Development

- Track PCF changes throughout product development
- Identify opportunities for emissions reduction
- Compare design alternatives

### Supply Chain Management

- Compare PCF values from different suppliers
- Monitor supplier improvement efforts
- Make informed sourcing decisions based on environmental impact

### Sustainability Reporting

- Generate PCF reports for stakeholders
- Track progress toward emissions reduction goals
- Support environmental claims and certifications
- Meet regulatory requirements (e.g., Battery Passport)

## References

- [IDTA Carbon Footprint V0.9 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2024/01/IDTA-2023-0-9-_Submodel_CarbonFootprint.pdf)
- [IDTA Carbon Footprint V1.0 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2025/03/IDTA-02023_Submodel_CarbonFootprint.pdf)
