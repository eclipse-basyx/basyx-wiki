# File Explorer

> **As a** BaSyx AAS Web UI user  
> **I want to** manage files and folders in a file management Submodel with an intuitive interface  
> **so that** I can organize, upload, preview, and download files similar to common cloud storage solutions.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- `https://basyx.org/FileSystem/FileSystem/0/1`

## Feature Overview

The File Explorer plugin provides a comprehensive file management interface for Asset Administration Shells. It transforms file-based Submodels into an intuitive, cloud storage-like experience, allowing users to manage documents, images, and other files directly within the AAS Web UI.

The plugin automatically handles folder structures using SubmodelElementCollections, providing a seamless hierarchical organization of files without manual configuration.

```{figure} ./images/file_explorer_gallery.png
---
width: 100%
alt: File Explorer - Gallery View
name: file_explorer_gallery
---
File Explorer Plugin in Gallery View
```

## Key Features

### Multiple View Modes

- **Gallery View**: Visual grid layout with file previews and thumbnails
- **List View**: Compact table layout for efficient browsing of large file collections

### File Upload

- **Drag & Drop Upload**: Simply drag files from your computer into the interface
- **Multi-file Upload**: Upload multiple files simultaneously

### Folder Management

- **Create New Folders**: Organize files into hierarchical folder structures
- **Folder Renaming**: Update folder names as your organization needs change
- **Drag & Drop Organization**: Move files and folders by dragging them to new locations
- **Nested Structures**: Support for multiple levels of folder nesting

### File Operations

- **File Preview**: View images, PDFs, and other supported file types directly in the browser
- **File Download**: Download individual files or multiple files at once
- **Delete Operations**: Remove files or folders individually or through multi-select
- **Multi-select Support**: Select multiple files and folders for batch operations

### User Experience

- **Cloud Storage Interface**: Familiar interface inspired by popular cloud storage solutions
- **Responsive Design**: Works seamlessly based on screen size and device
- **Visual Feedback**: Clear indicators for file types and actions

## Usage

### Accessing the File Explorer

1. Navigate to a Submodel with the File System semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The File Explorer plugin automatically displays the file structure

### Switching Between Views

Toggle between Gallery and List view using the view switcher in the toolbar:

- **Gallery View**: Best for visual browsing, especially with images and documents
- **List View**: Best for large file collections and detailed file information

```{figure} ./images/file_explorer_list.png
---
width: 100%
alt: File Explorer - List View
name: file_explorer_list
---
File Explorer Plugin in List View
```

### Uploading Files

**Drag & Drop Method:**

1. Open the File Explorer in the desired folder
2. Drag files from your computer's file manager
3. Drop them onto the File Explorer interface
4. Wait for the upload to complete

**Button Upload Method:**

1. Click the **New** button in the toolbar
2. Select **File** from the context menu
3. Choose files by clicking on the file selection dialog
4. Click **Upload** to start the upload

### Creating Folders

1. Click the **New** button in the toolbar
2. Select **Folder** from the context menu
3. The folder appears in the current directory
4. Rename the folder as needed

### Organizing Files and Folders

**Moving Items:**

1. Select the file or folder you want to move
2. Drag it to the destination folder
3. Drop it when the folder is highlighted
4. The item moves to the new location

**Renaming:**

1. Right-click on a folder
2. Select **Rename** from the context menu
3. Enter the new name
4. Press Enter to save

### Deleting Files and Folders

**Single Item:**

1. Right-click on the file or folder
2. Select **Delete** from the context menu
3. Confirm the deletion if prompted

**Multiple Items:**

1. Select multiple files/folders using the checkboxes
2. Click on the delete icon in the toolbar
3. Confirm the deletion

### Previewing Files

1. Click on a file in the File Explorer
2. Supported file types (images, PDFs, text files) display in a preview pane
3. Close the preview to return to the file list

### Downloading Files

**Single File:**

1. Right-click on the file
2. Select **Download** from the context menu
3. The file downloads to your default download location

```{hint}
Alternbatively you are also able to download files from the preview pane by clicking the download button.
```

## Submodel Structure

The File Explorer plugin expects a Submodel with the following characteristics:

### Root Level

- **Submodel** with semantic ID `https://basyx.org/FileSystem/FileSystem/0/1`

### Files

Files are represented as **File SubmodelElements**:

```json
{
  "idShort": "document.pdf",
  "modelType": "File",
  "contentType": "application/pdf",
  "value": "/path/to/document.pdf"
}
```

### Folders

Folders are represented as **SubmodelElementCollections**:

```json
{
  "idShort": "Documents",
  "modelType": "SubmodelElementCollection",
  "value": [
    // Nested files and folders
  ]
}
```

The plugin automatically recognizes this structure and renders it as a folder hierarchy.

## Supported File Types

### Preview Support

The following file types can be previewed directly in the File Explorer:

- **Images**: PNG, JPG, JPEG, GIF, SVG, WebP
- **Documents**: PDF
- **Text**: TXT, MD, JSON, XML

### Download Support

All file types can be downloaded, regardless of preview support.

## Use Cases

### Product Documentation Management

- Organize user manuals, technical specifications, and certificates
- Maintain version-controlled document repositories
- Provide easy access to product documentation for customers and service technicians

### Image and Media Libraries

- Store product photos, technical drawings, and marketing materials
- Organize images by product line, version, or category
- Quick visual browsing of image assets

### CAD File Management

- Manage 3D models and technical drawings
- Organize models by assembly, component, or project

### Quality Documentation

- Store inspection reports, test results, and compliance documents
- Organize quality records by batch, date, or product
- Quick access to quality documentation during audits

### Maintenance Documentation

- Maintain repair manuals, spare parts lists, and troubleshooting guides
- Organize by equipment, system, or maintenance schedule
- Field technicians can access documentation directly from the AAS

## Notes

```{note}
The File Explorer plugin is a **custom BaSyx plugin** and not based on an official IDTA Submodel template.
```

```{hint}
Use the File Explorer plugin in combination with the Handover Documentation plugin: File Explorer for general file management, and Handover Documentation for standardized product documentation according to IDTA specifications.
```
