# Digital Nameplate

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Digital Nameplate Submodels in an expandable panel view  
> **so that** I can easily access and understand nameplate information for assets.

## Semantic IDs

This plugin is activated when a Submodel has one of the following semantic IDs:

- **V2.0**: `https://admin-shell.io/zvei/nameplate/2/0/Nameplate`
- **V3.0**: `https://admin-shell.io/idta/nameplate/3/0/Nameplate`

## Feature Overview

The Digital Nameplate plugin provides a specialized visualization for Digital Nameplate Submodels according to the IDTA specification. It displays nameplate information in an expandable panel view, making it easy to browse through manufacturer information, product details, and other relevant nameplate data.

```{figure} ./images/digital_nameplate.png
---
width: 100%
alt: Digital Nameplate Plugin
name: digital_nameplate_plugin
---
Digital Nameplate Plugin
```

## Key Features

- **Expandable Panel View**: All SubmodelElements are organized in collapsible panels for easy navigation
- **Structured Information Display**: Nameplate data is presented in a logical, hierarchical structure
- **Support for Multiple Versions**: Compatible with both V2.0 and V3.0 of the IDTA Digital Nameplate specification
- **Multi-language Support**: Displays multi-language properties according to the user's language settings

## Usage

1. Navigate to a Submodel with the Digital Nameplate semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The plugin will automatically display the nameplate information in an expandable panel view
4. Click on panel headers to expand or collapse sections
5. View detailed information for each nameplate element

## Supported Submodel Elements

The plugin supports all SubmodelElements defined in the IDTA Digital Nameplate specification, including:

- Manufacturer information
- Product designation and descriptions
- Article numbers and serial numbers
- Physical dimensions and classifications
- Markings and certifications
- Contact information
- And more...

## References

- [IDTA Digital Nameplate V2.0 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2022/10/IDTA-02006-2-0_Submodel_Digital-Nameplate.pdf)
- [IDTA Digital Nameplate V3.0 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2025/10/IDTA-02006-3-0-1_Submodel_Digital-Nameplate.pdf)
