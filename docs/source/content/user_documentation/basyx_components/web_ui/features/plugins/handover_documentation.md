# Handover Documentation

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Handover Documentation Submodels with previews for PDFs, images, and CAD files  
> **so that** I can access and review product documentation efficiently.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- **V1.2**: `0173-1#01-AHF578#001`

## Feature Overview

The Handover Documentation plugin provides a specialized interface for managing and viewing product documentation. It organizes documents in an expandable view and provides built-in preview capabilities for common file formats, eliminating the need to download files for quick review.

```{figure} ./images/handover_documentation.png
---
width: 100%
alt: Handover Documentation Plugin
name: handover_documentation_plugin
---
Handover Documentation Plugin
```

## Key Features

- **Expandable Document Structure**: Navigate through document hierarchies easily
- **Inline File Previews**: View documents directly in the browser without downloading
- **Multi-format Support**:
  - PDF documents
  - Images (PNG, JPG, SVG, etc.)
  - CAD files (STL, glTF, OBJ)
- **Document Metadata**: View document properties, versions, and classifications
- **Download Options**: Download individual documents or entire document collections

## Usage

1. Navigate to a Submodel with the Handover Documentation semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The plugin displays the document structure in an expandable view
4. Click on panel headers to expand or collapse document categories
5. Click on a document to preview it inline:
   - PDFs open in a built-in PDF viewer
   - Images display with zoom and pan capabilities
   - CAD files render in an interactive 3D viewer
6. Use the download button to save documents locally

```{figure} ./images/handover_pdf_preview.png
---
width: 80%
alt: PDF Preview in Handover Documentation
name: handover_pdf_preview
---
PDF Document Preview
```

```{figure} ./images/handover_cad_preview.png
---
width: 80%
alt: CAD Preview in Handover Documentation
name: handover_cad_preview
---
CAD File Preview
```

## Supported Document Types

### PDF Documents
- User manuals
- Technical specifications
- Certificates and compliance documents
- Installation guides

### Images
- Product photos
- Technical drawings
- Diagrams and schematics
- QR codes and labels

### CAD Files
- 3D models (.stl, .glTF, .obj)
- Interactive rotation and zooming
- Dimension visualization

## Document Organization

Documents are typically organized in the following categories:

- **Operating Instructions**: User and operator manuals
- **Technical Documentation**: Specifications, drawings, schematics
- **Certificates**: Compliance, safety, and quality certificates
- **Spare Parts Lists**: Maintenance and replacement part information
- **Safety Information**: Safety data sheets, warnings, regulations

## References

- [IDTA Handover Documentation V1.2 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2023/03/IDTA-02004-1-2_Submodel_Handover-Documentation.pdf)
