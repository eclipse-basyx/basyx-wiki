# Handover Documentation

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Handover Documentation Submodels with previews for PDFs, images, and CAD files  
> **so that** I can access and review product documentation efficiently.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- **V1.2**: `0173-1#01-AHF578#001`

## Feature Overview

The Handover Documentation plugin provides a specialized interface for viewing product documentation according to VDI 2770 Blatt 1 standards. It organizes documents in an expandable view based on the VDI 2770 classification system and provides built-in preview capabilities for common file formats, eliminating the need to download files for quick review.

```{figure} ./images/handover_documentation.png
---
width: 100%
alt: Handover Documentation Plugin
name: handover_documentation_plugin
---
Handover Documentation Plugin
```

## Key Features

- **Expandable Document Structure**: Navigate through documents easily
- **Inline File Previews**: View documents directly in the browser without downloading
- **Multi-format Support**:
  - PDF documents
  - Images (PNG, JPG, SVG, etc.)
  - CAD files (STL, glTF, OBJ)
- **Document Metadata**: View document properties, versions, and classifications
- **Download Options**: Download documents

## Usage

1. Navigate to a Submodel with the Handover Documentation semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The plugin displays the document in expansion panels
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

## Document Organization

Documents are organized according to the **VDI 2770 Blatt 1:2020** classification system. This standard defines a comprehensive set of document classes that allows efficient management and retrieval of equipment documentation. Each document class has a unique ClassID and multilingual ClassName.

### VDI 2770 Blatt 1:2020 Document Classes

| ClassID | ClassName (EN) | ClassName (DE) |
| ------- | -------------- | -------------- |
| 01-01 | Identification | Identifikation |
| 02-01 | Technical specification | Technische Spezifikation |
| 02-02 | Drawings, plans | Zeichnungen, Pläne |
| 02-03 | Assemblies | Bauteile |
| 02-04 | Certificates, declarations | Zeugnisse, Zertifikate, Bescheinigungen |
| 03-01 | Commissioning, de-commissioning | Montage, Demontage |
| 03-02 | Operation | Bedienung |
| 03-03 | General safety | Allgemeine Sicherheit |
| 03-04 | Inspection, maintenance, testing | Inspektion, Wartung, Prüfung |
| 03-05 | Repair | Instandsetzung |
| 03-06 | Spare parts | Ersatzteile |
| 04-01 | Contract documents | Vertragsunterlagen |

The plugin automatically organizes documents into these categories based on their DocumentClassification metadata, making it easy to find specific types of documentation.

## References

- [IDTA Handover Documentation V1.2 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2023/03/IDTA-02004-1-2_Submodel_Handover-Documentation.pdf)
