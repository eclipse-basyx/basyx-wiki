# Technical Data

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Technical Data Submodels in an expandable panel view  
> **so that** I can easily access and understand technical specifications and parameters.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- **V1.2**: `https://admin-shell.io/ZVEI/TechnicalData/Submodel/1/2`

## Feature Overview

The Technical Data plugin provides a specialized visualization for Technical Data Submodels according to the IDTA specification. It organizes information into four main expansion panels and offers two visualization modes for technical properties:

1. **General Information**: Minimal information about the provider and equipment for identification and ordering
2. **Product Classification**: Commercial product classifications (e.g., ECLASS, IEC CDD)
3. **Technical Properties**: Detailed technical data with semantic information from concept descriptions
4. **Further Information**: Additional statements, validity dates, and supplementary details

For Technical Properties, users can toggle between a **table view** and a **generic nested expansion panel view** to suit their preference.

```{figure} ./images/technical_data.png
---
width: 100%
alt: Technical Data Plugin
name: technical_data_plugin
---
Technical Data Plugin
```

## Key Features

- **Four-Panel Structure**: Information organized into General Information, Product Classification, Technical Properties, and Further Information
- **Dual View Mode**: Toggle between table view and nested expansion panel view for Technical Properties
- **Semantic Information**: Rich metadata from concept descriptions including:
  - Units of measurement
  - Data types
  - Definitions and descriptions
  - Value constraints
- **Hierarchical Organization**: Properties can be categorized and nested using SubmodelElementCollections
- **Domain-Specific Structuring**: Support for ECLASS, IEC CDD, and other property dictionaries
- **Multi-language Support**: Technical terms and descriptions in multiple languages
- **Specifications and Ranges**: Display of min/max values, tolerances, and typical values

## Usage

1. Navigate to a Submodel with the Technical Data semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The plugin displays four main expansion panels:
   - **General Information**: Provider and equipment identification
   - **Product Classification**: Product classification codes
   - **Technical Properties**: Detailed technical specifications
   - **Further Information**: Additional details and validity information
4. Click on panel headers to expand or collapse each section
5. In the **Technical Properties** panel, toggle between:
   - **Table View**: Properties displayed in a structured table with columns for name, value, unit, and description
   - **Nested Expansion Panel View**: Hierarchical view showing categorized and nested properties
6. View semantic information for each technical parameter from concept descriptions:
   - Parameter name and definition
   - Value and unit of measurement
   - Data type and format
   - Min/max ranges and tolerances

```{figure} ./images/technical_properties.png
---
width: 80%
alt: Technical Properties Table View
name: technical_properties
---
Technical Properties in Table View with Units, Definitions, and Semantic Information
```

## Four-Panel Structure

### 1. General Information

Provides minimal information about the provider of the industrial equipment and the equipment itself. This section helps determine if the technical data fits the particular asset and enables ordering or re-ordering from the manufacturer or supplier.

**Typical content:**

- Manufacturer identification
- Product designation
- Order codes and part numbers
- Basic product identifiers

### 2. Product Classification

Treats the asset as a commercial product brought to market by the manufacturer. Multiple product classifications can be stated according to standardized classification systems.

**Typical content:**

- ECLASS classification codes
- IEC CDD classifications
- Other domain-specific product classifications
- Classification system identifiers

### 3. Technical Properties

The most comprehensive section containing individual SubmodelElements detailing technical data. Properties can be structured using SubmodelElementCollections and nested as needed. Each property includes semantic information from concept descriptions.

**Organization:**

- Main and subsections for human readability
- Domain-specific structuring (ECLASS, IEC CDD blocks)
- Hierarchical categorization (e.g., Electrical, Mechanical, Environmental)
- Support for properties and file references

**Common property types:**

- Electrical specifications (voltage, current, power, frequency)
- Mechanical specifications (dimensions, weight, torque, force)
- Environmental conditions (temperature, humidity, IP ratings)
- Performance characteristics (efficiency, accuracy, response times)
- Material specifications and certifications

### 4. Further Information

Holds additional information beyond structured technical data.

**Typical content:**

- Textual statements by the manufacturer
- Date of validity
- Additional notes and remarks
- Supplementary documentation references

## Data Organization and Semantic Information

### Hierarchical Structure

Technical properties are organized using **SubmodelElementCollections** that allow categorization and nesting:

1. **Top-level Collections**: Main groupings (e.g., "Electrical Properties", "Mechanical Properties")
2. **Nested Collections**: Sub-categories for more specific groupings (e.g., "Input Specifications", "Output Specifications")
3. **Individual Properties**: Specific technical values with complete semantic information

### Semantic Information via Concept Descriptions

Each technical property is enriched with semantic information provided through **Concept Descriptions**, which include:

- **Unit**: Unit of measurement (e.g., V, A, mm, kg, °C)
- **Data Type**: Value type (e.g., integer, float, string, boolean)
- **Definition**: Detailed description of what the property represents
- **Description**: Additional explanatory text
- **Value Constraints**: Min/max values, allowed ranges, enumerations
- **Preferred Name**: Human-readable property name
- **Short Name**: Abbreviated designation

This semantic information is displayed in both the table view and expansion panel view, providing context and clarity for each technical parameter.

## References

- [IDTA Technical Data V1.2 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2022/10/IDTA-02003-1-2_Submodel_TechnicalData.pdf)
