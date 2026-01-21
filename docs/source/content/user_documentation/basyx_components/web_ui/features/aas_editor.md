# AAS Editor

> **As a** BaSyx AAS Web UI user  
> **I want to** create and edit Asset Administration Shells, Submodels, and SubmodelElements  
> **so that** I can build and maintain my digital twin infrastructure.

## Feature Overview

The **AAS Editor** provides comprehensive editing capabilities for creating, modifying, and managing Asset Administration Shells (AAS), Submodels, and SubmodelElements directly within the Web UI. It offers form-based editing with validation, import/export functionality, and support for a wide range of SubmodelElement types.

The editor is designed to be user-friendly while ensuring data integrity through validation against the AAS metamodel specification. All changes are made through intuitive forms, with helpful hints and real-time validation to prevent invalid data entry.

```{seealso}
For technical details on the AAS metamodel and its requirements, refer to the [AAS Metamodel Specification](https://industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.2/index.html).
```

## Accessing the Editor

The BaSyx AAS Web UI provides two editor pages accessible from the main menu:

- **AAS Editor**: For working with Asset Administration Shells in an AAS-centric view
- **SM Editor** (Submodel Editor): For working directly with Submodels in a submodel-centric view

```{figure} ./images/accessing_editor.png
---
width: 50%
alt: Accessing the AAS Editor
name: accessing_editor
---
AAS Editor menu entry in the main navigation
```

```{note}
The editor functionality can be disabled by setting the environment variable `ALLOW_EDITING=false`. This is useful for read-only deployments or when editing should be restricted.
```

```{seealso}
For information on configuring environment variables, see the [Docker Configuration](./docker_config.md) page.
```

## Creating Asset Administration Shells

To create a new Asset Administration Shell:

1. Navigate to the **AAS Editor** page from the main menu
2. In the **AAS List** sidebar, click the **three-dot menu icon** in the header
3. Select **Create AAS** from the context menu
4. Fill in the required fields in the creation form:
   - **ID**: Automatically prefilled with a generated ID (can be modified)
   - **idShort**: The short identifier for the AAS
   - **Asset Information**: Details about the physical or logical asset
   - **Administrative Information** (optional): Version, revision, creator details

```{figure} ./images/create_aas_form.png
---
width: 70%
alt: Create AAS Form
name: create_aas_form
---
Form for creating a new Asset Administration Shell
```

5. Click **Save** to create the AAS

```{hint}
Look for the **question mark (?)** buttons next to input fields for helpful hints about what each field represents and how to fill it correctly.
```

### Editing Existing AAS

To edit an existing Asset Administration Shell:

1. In the **AAS List**, locate the AAS you want to edit
2. Click the **three-dot menu icon** next to the AAS
3. Select **Edit AAS** from the context menu
4. Modify the fields as needed in the edit form
5. Click **Save** to apply your changes, or **Cancel** to discard them

```{figure} ./images/edit_aas_context_menu.png
---
width: 40%
alt: Edit AAS Context Menu
name: edit_aas_menu
---
Context menu for editing an existing AAS
```

## Creating and Managing Submodels

### Adding a New Submodel to an AAS

To add a Submodel to an existing AAS:

1. Select the AAS from the **AAS List**
2. In the **AAS Treeview** header, click the **three-dot menu icon**
3. Select **Add Submodel** from the context menu
4. Fill in the required fields:
   - **ID**: Automatically generated (can be customized)
   - **idShort**: Short identifier for the Submodel
   - **semanticId**: The semantic identifier defining the Submodel's meaning and structure
   - **Description** (optional): Human-readable description of the Submodel

```{figure} ./images/add_submodel_form.png
---
width: 70%
alt: Add Submodel Form
name: add_submodel_form
---
Form for adding a new Submodel to an AAS
```

5. Click **Save** to add the Submodel to the AAS

### Editing a Submodel

To edit an existing Submodel:

1. In the **AAS Treeview**, locate the Submodel you want to edit
2. Click the **three-dot menu icon** next to the Submodel name
3. Select **Edit Submodel** from the context menu
4. Modify the fields in the edit form
5. Click **Save** to apply changes

### Deleting a Submodel

To delete a Submodel:

1. In the **AAS Treeview**, click the **three-dot menu icon** next to the Submodel
2. Select **Delete Submodel** from the context menu
3. Confirm the deletion in the dialog that appears

```{warning}
Deleting a Submodel will also delete all SubmodelElements contained within it. This action cannot be undone.
```

## Adding and Editing SubmodelElements

The AAS Editor supports creating and editing the following SubmodelElement types:

- Property
- MultiLanguageProperty
- Range
- File
- Blob
- SubmodelElementCollection
- SubmodelElementList

### Adding a SubmodelElement

To add a SubmodelElement to a Submodel or SubmodelElementCollection/List:

1. In the **AAS Treeview**, locate the parent element (Submodel, Collection, or List)
2. Click the **three-dot menu icon** next to the parent element
3. Select **Add SubmodelElement** from the context menu
4. Choose the type of SubmodelElement you want to create from the list
5. Fill in the required fields based on the element type (see details below)
6. Click **Save** to add the element

```{figure} ./images/add_submodelelement_menu.png
---
width: 60%
alt: Add SubmodelElement Menu
name: add_sme_menu
---
Context menu for adding SubmodelElements
```

### Property

Properties are used to store single values of a specific data type.

**Required Fields:**

- **idShort**: Short identifier
- **valueType**: Select from available AAS-supported value types (string, int, boolean, etc.)

**Optional Fields:**

- **value**: The actual value of the property
- **semanticId**: Semantic identifier
- **displayName**: Localized display names
- **description**: Localized human-readable description

```{figure} ./images/edit_property_form.png
---
width: 70%
alt: Property Edit Form
name: property_form
---
Form for editing a Property SubmodelElement
```

```{hint}
The UI automatically validates that the entered value matches the selected valueType. For example, if you select "int" as the valueType, you cannot enter letters in the value field.
```

### MultiLanguageProperty

MultiLanguageProperties store text values in multiple languages.

**Required Fields:**

- **idShort**: Short identifier

**Optional Fields:**

- **value**: Language-tagged text entries (can add as many languages as needed)
- **semanticId**: Semantic identifier
- **displayName**: Localized display names
- **description**: Localized human-readable description

**Adding Language Entries:**

1. In the value section, click **Add**
2. Select or enter the language code (e.g., "en", "de", "fr")
3. Enter the text for that language
4. Repeat to add more languages

```{figure} ./images/multilanguage_property_form.png
---
width: 70%
alt: MultiLanguageProperty Form
name: mlp_form
---
Form for editing a MultiLanguageProperty with multiple languages
```

### Range

Range SubmodelElements define a value range with minimum and maximum values.

**Required Fields:**

- **idShort**: Short identifier
- **valueType**: Data type for the range values

**Optional Fields:**

- **min**: Minimum value
- **max**: Maximum value
- **semanticId**: Semantic identifier
- **displayName**: Localized display names
- **description**: Localized human-readable description

```{figure} ./images/range_form.png
---
width: 70%
alt: Range Form
name: range_form
---
Form for editing a Range SubmodelElement
```

### File

File SubmodelElements reference external files.

**Required Fields:**

- **idShort**: Short identifier

**Optional Fields:**

- **contentType**: MIME type of the file (e.g., "application/pdf", "image/png")
- **value**: File path or URL
- **semanticId**: Semantic identifier
- **displayName**: Localized display names
- **description**: Localized human-readable description

**Uploading Files:**
Users can upload files directly through the form. The file will be stored and the path will be automatically set.

```{figure} ./images/file_upload_form.png
---
width: 70%
alt: File Upload Form
name: file_form
---
Form for uploading and editing a File SubmodelElement
```

```{note}
Not all file types have dedicated preview capabilities. Some files may only show their path in the Element Details view.
```

### Blob

Blob SubmodelElements store binary data directly within the AAS.

**Required Fields:**

- **idShort**: Short identifier

**Optional Fields:**

- **contentType**: MIME type of the blob content
- **value**: Base64-encoded binary data (or upload a file)
- **semanticId**: Semantic identifier
- **displayName**: Localized display names
- **description**: Localized human-readable description

**Uploading Blob Content:**
Users can upload files directly, which will be automatically encoded and stored as blob data.

```{figure} ./images/blob_upload_form.png
---
width: 70%
alt: Blob Upload Form
name: blob_form
---
Form for uploading and editing a Blob SubmodelElement
```

### SubmodelElementCollection

SubmodelElementCollections group related SubmodelElements together.

**Required Fields:**

- **idShort**: Short identifier

**Optional Fields:**

- **semanticId**: Semantic identifier
- **displayName**: Localized display names
- **description**: Localized human-readable description

**Adding Elements to a Collection:**
After creating the collection, you can add child SubmodelElements by:

1. Clicking the **three-dot menu icon** next to the collection in the treeview
2. Selecting **Add SubmodelElement**
3. Creating the child element as described above

```{figure} ./images/collection_form.png
---
width: 70%
alt: SubmodelElementCollection Form
name: collection_form
---
Form for editing a SubmodelElementCollection
```

### SubmodelElementList

SubmodelElementLists are ordered collections of SubmodelElements of the same type.

**Required Fields:**

- **idShort**: Short identifier
- **typeValueListElement**: The type of SubmodelElements that can be added to this list

**Optional Fields:**

- **orderRelevant**: Boolean indicating if the order of elements matters
- **semanticId**: Semantic identifier
- **displayName**: Localized display names
- **description**: Localized human-readable description

**Adding Elements to a List:**
Similar to collections, use the context menu on the list element to add child SubmodelElements. All child elements must be of the type specified in `typeValueListElement`. Children of `SubmodelElementLists` are not required to have an `idShort`.

```{figure} ./images/list_form.png
---
width: 70%
alt: SubmodelElementList Form
name: list_form
---
Form for editing a SubmodelElementList
```

### Editing SubmodelElements

To edit any existing SubmodelElement:

1. In the **AAS Treeview**, locate the SubmodelElement
2. Click the **three-dot menu icon** next to the element
3. Select **Edit [ElementType]** (e.g., "Edit Property", "Edit File")
4. Modify the fields in the form
5. Click **Save** to apply changes

### Deleting SubmodelElements

To delete a SubmodelElement:

1. Click the **three-dot menu icon** next to the element in the treeview
2. Select **Delete [ElementType]**
3. Confirm the deletion

## Importing and Exporting

### Importing AAS Environments

The AAS Editor supports importing complete AAS environments from files:

**Supported Formats:**

- **AASX** (AAS Package)
- **JSON** (AAS Environment)
- **XML** (AAS Environment)

**Import Process:**

1. Navigate to the **AAS Editor** page
2. Click the **Import** button in the toolbar
3. Select the file to import (can contain multiple AAS)
4. The imported AAS will be added to your infrastructure

```{figure} ./images/upload_aas_menu.png
---
width: 50%
alt: Context menu for importing AAS
name: upload_aas_menu
---
Context menu for importing AAS environments
```

```{figure} ./images/import_dialog.png
---
width: 50%
alt: Import AAS Dialog
name: import_dialog
---
Dialog for importing AAS environments from files
```

### Importing Submodel Templates

You can import Submodel templates as JSON:

1. Navigate to the Submodel where you want to add elements
2. Click the **Import from JSON** option in the context menu
3. Paste or upload the JSON containing the Submodel template
4. The template structure will be added to your Submodel

### Exporting AAS

To export an Asset Administration Shell:

1. In the **AAS List**, click the **download icon** next to the AAS you want to export
2. Select the Submodel(s) to include in the export
3. The file will be downloaded to your device

```{figure} ./images/export_aas.png
---
width: 40%
alt: Export AAS
name: export_aas
---
Exporting an AAS as an AASX file
```

### Copy and Paste Functionality

The editor provides clipboard functionality for Submodels and SubmodelElements:

**Copy to Clipboard:**

1. Right-click on a Submodel or SubmodelElement in the treeview
2. Select **Copy [Element] as JSON** to copy to the system clipboard, or
3. Select **Copy [Element]** to copy to the application's internal clipboard

**Paste from Clipboard:**

1. Navigate to where you want to paste the element
2. Right-click and select **Paste from JSON** (for system clipboard) or **Paste [Element]** (for internal clipboard)
3. The element will be inserted at the selected location

```{hint}
Using the internal clipboard allows you to easily duplicate elements within the same AAS or copy them to different AAS without leaving the Web UI.
```

## Validation and Error Handling

The AAS Editor includes comprehensive validation to ensure data integrity:

### Real-Time Validation

- **Required Fields**: Input fields for required attributes show an error state if left empty
- **Data Types**: Value inputs are validated against their specified valueType (e.g., you cannot enter text in an integer field)
- **Save Button**: The Save button is disabled when the form contains validation errors

### Error States

When validation fails, the affected input field:

- Displays a red border or error indicator
- Shows a descriptive error message below the field
- Prevents saving until the error is resolved

```{figure} ./images/validation_error.png
---
width: 70%
alt: Validation Error
name: validation_error
---
Example of a validation error in the edit form
```

### Helpful Hints

Throughout the editor forms, you'll find **question mark (?)** buttons that provide:

- Descriptions of what each field represents
- Examples of valid values
- Links to relevant sections of the AAS specification

## Best Practices and Tips

### Starting with an Empty Setup

When building an AAS infrastructure from scratch, follow this order:

1. **Create the AAS** first with basic information
2. **Add Submodels** to the AAS with appropriate semanticIds
3. **Add SubmodelElements** to each Submodel to populate the structure
4. **Test and validate** by viewing the AAS in the standard viewer

### Working with Registries and Repositories

```{important}
When using separate registries and repositories in your AAS infrastructure, they must be kept in sync to avoid unexpected behavior.

BaSyx handles this automatically through the **automatic registry integration feature**. If you're using a different infrastructure, ensure that:
- Creating an AAS in the repository also registers it in the registry
- Deleting an AAS removes it from both repository and registry
- Updates to AAS metadata are reflected in the registry
```

### File Handling

- Not all file types have dedicated preview capabilities in the Element Details view
- For files without preview support, only the file path is displayed
- Always specify the correct `contentType` (MIME type) for files and blobs
- Consider file size when using Blobs versus Files (Blobs store data directly in the AAS)

### Semantic IDs

- Use standardized semantic IDs from [IDTA Submodel Templates](https://industrialdigitaltwin.org/content-hub/submodels) when possible
- Consistent use of semantic IDs enables automatic plugin-based visualizations
- Document custom semantic IDs if you create domain-specific Submodels

## Known Limitations

The current version of the AAS Editor has the following limitations:

### Unsupported SubmodelElement Types

The following SubmodelElement types are **not yet supported** in the editor:

- **ReferenceElement**
- **AnnotatedRelationshipElement**
- **RelationshipElement**
- **Entity**
- **Capability**
- **BasicEventElement**

```{note}
While these elements cannot be created or edited through the Web UI, they can still be viewed if present in imported AAS.
```

### Unsupported Attributes

Some AAS attributes are not yet supported in the editor, including:

- **SupplementalSemanticIds**
- Some advanced metadata attributes

### Feature Requests

If you need support for specific SubmodelElement types or attributes, please:

- Check the [BaSyx GitHub repository](https://github.com/eclipse-basyx/basyx-aas-web-ui/issues) for existing feature requests
- Open a new issue to request the feature
- Consider contributing to the project if you have development experience

## Permissions and Access Control

Editor access can be controlled in several ways:

### Environment Variable Control

The editor pages can be completely disabled by setting:

```bash
ALLOW_EDITING=false
```

This is useful for:

- Read-only production deployments
- Demo or presentation environments
- Restricting editing to specific deployments

### Backend-Level Permissions

When RBAC (Role-Based Access Control) or ABAC (Attribute-Based Access Control) is configured on the backend:

- The Web UI respects backend permissions
- Users without edit permissions will see errors when attempting to save changes
- Some operations may be restricted based on user roles

```{seealso}
For information on configuring access control, see the [Security](./security.md) feature page.
```

## Troubleshooting

### Cannot Save Changes

If you cannot save your changes:

1. Check all input fields for **red error indicators**
2. Ensure all **required fields** are filled in
3. Verify that value types match the entered data
4. Check the browser console for any error messages

### Changes Not Appearing After Save

If changes don't appear after saving:

1. Verify that you're connected to the correct infrastructure
2. Check if registries and repositories are in sync
3. Try refreshing the page to reload data from the backend
4. Check for error notifications in the Web UI

### Import Fails

If importing an AAS environment fails:

1. Verify the file format is supported (AASX, JSON, or XML)
2. Ensure the file contains valid AAS data according to the V3 metamodel
3. Check file size limits on your backend infrastructure
4. Review error messages for specific validation issues
