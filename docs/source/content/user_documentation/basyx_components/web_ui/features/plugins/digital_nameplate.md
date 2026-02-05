# Digital Nameplate

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Digital Nameplate Submodels in an expandable panel view  
> **so that** I can easily access and understand nameplate information for assets.

## Semantic IDs

This plugin is activated when a Submodel has one of the following semantic IDs:

- **V2.0**: `https://admin-shell.io/zvei/nameplate/2/0/Nameplate`
- **V3.0**: `https://admin-shell.io/idta/nameplate/3/0/Nameplate`

## Feature Overview

The Digital Nameplate plugin provides a specialized visualization for Digital Nameplate Submodels according to the IDTA specification. It organizes nameplate information into five distinct cards for easy navigation and comprehension:

1. **Product Info Card**: Displays product designation, descriptions, article numbers, serial numbers, ...
2. **Manufacturer Info Card**: Shows manufacturer details including company name, addresses, and contact information
3. **Address Map Card**: Interactive OpenStreetMap visualization of the company/manufacturer address
4. **Markings Card**: Presents regulatory markings and certifications (e.g., CE marking)
5. **Asset Specific Properties Card**: Generic expansion panel structure for additional asset-specific information

```{figure} ./images/nameplate_product.png
---
width: 100%
alt: Digital Nameplate Plugin - Product Information
name: digital_nameplate_product
---
Digital Nameplate Plugin - Product Information Card
```

```{figure} ./images/nameplate_manufacturer.png
---
width: 100%
alt: Digital Nameplate Plugin - Manufacturer Information and Map
name: digital_nameplate_manufacturer
---
Digital Nameplate Plugin - Manufacturer Information and Address Map Cards
```

## Key Features

- **Card-Based Layout**: Information is organized into five dedicated cards for intuitive navigation
- **Interactive Address Map**: OpenStreetMap integration displays manufacturer/company locations visually
- **vCard Download**: Export manufacturer contact information as a vCard file for easy import into contact management systems

## Usage

1. Navigate to a Submodel with the Digital Nameplate semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The plugin will automatically display the nameplate information organized in five cards:
   - **Product Info**: View product details, descriptions, article numbers, and dimensions
   - **Manufacturer Info**: Access manufacturer details and download contact information as a vCard
   - **Address Map**: Explore the manufacturer's location on an interactive OpenStreetMap
   - **Markings**: Review regulatory markings and certifications
   - **Asset Specific Properties**: Browse additional asset-specific information in expandable panels
4. Use the vCard download button in the Manufacturer Info card to export contact information

## Supported Submodel Elements

The plugin supports all SubmodelElements defined in the IDTA Digital Nameplate specification, organized across the five cards:

### Product Info Card

- Product designation and descriptions
- Article numbers and serial numbers
- Product classifications and categories

### Manufacturer Info Card

- Manufacturer name and identifiers
- Contact information with vCard export functionality
- Company addresses
- Web presence and communication details

### Address Map Card

- Interactive OpenStreetMap visualization
- Geolocation of manufacturer/company address
- Zoom and pan controls for detailed location viewing

### Markings Card

- Regulatory markings (e.g., CE marking)
- Certifications and compliance information
- Safety and quality markings

### Asset Specific Properties Card

- Custom asset properties
- Additional technical specifications
- Application-specific information

## References

- [IDTA Digital Nameplate V2.0 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2022/10/IDTA-02006-2-0_Submodel_Digital-Nameplate.pdf)
- [IDTA Digital Nameplate V3.0 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2025/10/IDTA-02006-3-0-1_Submodel_Digital-Nameplate.pdf)
