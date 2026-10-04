# Models 3D

> **As a** BaSyx AAS Web UI user  
> **I want to** browse the 3D models of an asset and inspect them directly in the browser  
> **so that** I can check geometry, level of detail and origin of a model without downloading it first.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- `https://admin-shell.io/idta/Models3D/1/0`

## Feature Overview

The Models 3D plugin visualizes Submodels based on the IDTA Submodel Template *Provision of 3D Models*. It embeds an interactive 3D viewer for the model and shows the most important information about it right next to the viewer: status, version, level of detail, intended use and key properties. All remaining metadata is available in a collapsible *Technical details* section.

The plugin adapts to the width of the Visualization pane. In a narrow pane (for example side by side with the AAS Treeview) the information is shown below the viewer, in a wide pane (for example in full screen) next to it.

```{figure} ./images/models_3d.png
---
width: 60%
alt: Models 3D Plugin
name: models_3d_plugin
---
Models 3D Plugin showing a single model
```

## Key Features

- **Interactive 3D viewer**: Rotate, pan and zoom the model; a view cube in the corner snaps the camera to the main axes
- **Automatic framing**: The model is centered and scaled to the viewer, independent of its unit
- **Original materials**: glTF/GLB models keep their own colors and textures
- **Viewer buttons**: *Reset view*, switch between the 3D model and the preview image of the Submodel, and *Download* the 3D file. The format of the file (for example `glTF 2.0 · .glb`) is shown as a badge in the corner of the viewer
- **Status**: The status of the selected version (for example `Released`) is shown next to the title and colored accordingly
- **Level of detail**: The description of the simplification and, if given, the elements that were reduced
- **Intended use**: Purposes the model is suitable for (green, with a check mark) and not suitable for (red, with a cross)
- **Key facts**: Object type, origin, representation, length unit and bounding box
- **Technical details**: File name, format, version, date, providing organization, the applications the model was created with and is used by, and classifications
- **External files**: If a version only references an external file (`ExternalFile`), a link to it is offered instead of the viewer

### Several Models

If the Submodel contains more than one model, a scrollable row of cards with preview image, title, format and object type is shown above the viewer. Select a card to show the model. If only one model exists, the row is not shown.

```{figure} ./images/models_3d_multiple.png
---
width: 100%
alt: Models 3D Plugin with several models
name: models_3d_plugin_multiple
---
Several models in a wide Visualization pane: viewer and summary are shown side by side
```

### Several Versions

If a model has more than one file version, a version menu appears next to the title. It lists the versions of the file, the newest first, with their date and status. The most recent version (by `SetDate`) is selected by default and marked as *Latest*. If a model has only one version, the version is shown as a plain label.

```{figure} ./images/models_3d_versions.png
---
width: 60%
alt: Version menu of the Models 3D Plugin
name: models_3d_plugin_versions
---
Version menu of a model with three versions
```

## Usage

1. Navigate to a Submodel with the Models 3D semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. Rotate the model with the left mouse button, pan with the right mouse button and zoom with the mouse wheel
4. Use the buttons in the upper right corner of the viewer to reset the view, switch to the preview image or download the model
5. If there are several models or versions, select them with the cards above the viewer or the version menu
6. Expand **Technical details** for the remaining metadata

## Supported File Formats

| Format | Content type | Notes |
|--------|--------------|-------|
| glTF 2.0 binary (`.glb`) | `model/gltf-binary` | Original materials and textures are shown |
| glTF 2.0 (`.gltf`) | `model/gltf+json` | Must be self-contained (no external `.bin` or texture files) |
| STL | `model/stl` | Shown with a uniform white material |
| OBJ | `application/obj` | Shown with a uniform white material |

The format is determined from the content type of the `DigitalFile` and, if it is missing or generic (for example `application/octet-stream`), from the file extension. The same viewer is used for File elements outside of this plugin, so GLB files are also previewed when a File element is selected in the AAS Treeview.

```{note}
Compressed glTF files (Draco, KTX2, Meshopt) are not supported yet.
```

## Submodel Structure

The plugin expects the structure defined by the IDTA template. Only the `Model3D` list is required, all other elements are optional and are simply left out of the view if they are missing.

### Model3D

| idShort | Type | Description |
|---------|------|-------------|
| `Model3D` | `SubmodelElementList` | One entry (`SubmodelElementCollection`) per 3D model |
| `File` | `SubmodelElementCollection` | File information of the model |
| `Capability` | `SubmodelElementCollection` | Intended use and level of detail |
| `Geometry` | `SubmodelElementCollection` | Geometric properties |

The entries of the `Model3D` list do not have an idShort and are identified by their position.

### File

| idShort | Type | Description |
|---------|------|-------------|
| `FileId` | `SubmodelElementList` | Identifiers of the file; `IsPrimary` marks the primary model |
| `FileVersion` | `SubmodelElementList` | One entry per version of the file |
| `ConsumingApplication` | `SubmodelElementList` | Applications that use the model |
| `FileClassification` | `SubmodelElementList` | Classification of the model (`ClassId`, `ClassName`, `ClassificationSystem`) |

### FileVersion

| idShort | Type | Description |
|---------|------|-------------|
| `Title` | `MultiLanguageProperty` | Title shown on the model card and above the viewer |
| `FileName` | `Property` | Name of the file; used as title if no `Title` is given |
| `FileVersionId` | `Property` | Version of the file |
| `StatusValue` | `Property` | Status, for example `Released` |
| `SetDate` | `Property (xs:date)` | Date of the version; the latest one is shown by default |
| `PreviewFile` | `File` | Preview image of the model |
| `DigitalFile` | `File` | The 3D file shown in the viewer and offered for download |
| `ExternalFile` | `SubmodelElementList` | External location of the file (`ExternalUrl`) |
| `FileFormat` | `SubmodelElementCollection` | `FormatName`, `FormatVersion` and `FormatQualifier` |
| `SourceApplication` | `SubmodelElementCollection` | Application the model was created with |
| `ProvidingOrganization` | `SubmodelElementCollection` | Organization that provides the model |

### Capability

| idShort | Type | Description |
|---------|------|-------------|
| `Simplification` | `SubmodelElementCollection` | Level of detail: `Description` and `ReducedElements` |
| `PosModelPurpose` / `NegModelPurpose` | `SubmodelElementList` | Purposes the model is (not) suitable for |
| `ObjectType`, `Origin` | `Property` | Type of the modeled object and how the model was created |
| `EmbeddedInfo`, `State` | `SubmodelElementList` | Additional information embedded in the model and the state it shows |

The **Level of detail** shows the description of the `Simplification`; if the model is not marked as simplified, the `Representation` of the `Geometry` is shown instead.

### Geometry

| idShort | Type | Description |
|---------|------|-------------|
| `Representation` | `Property` | Kind of representation, for example `Mesh` |
| `LengthUnit` | `Property` | Unit of the model's coordinates |
| `CartBoundingBox` | `SubmodelElementList` | Bounding boxes with their `CartBoundingVector` |
