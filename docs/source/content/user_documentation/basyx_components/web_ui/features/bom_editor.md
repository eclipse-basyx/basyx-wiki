# BOM (Hierarchical Structures) Editor

> **As a** user of the BaSyx Web UI  
> **I want to** create and edit hierarchical structures (BOMs) of assets in the AAS  
> **So that** I can represent complex relationships between assets without having to manually manage each individual asset and relationship.

```{figure} ./images/bom_viewer.png
---
width: 100%
alt: BOM Viewer
name: bom_viewer
---
BOM Viewer
```

## Feature Overview

The BOM Editor is accessible via the **Visualization tab** in the AAS UI when a **Hierarchical Structure submodel template** is selected in the submodel tree.

### Editor Mode

In **Editor Mode** (AASEditor, SubmodelEditor), you can:
- **Add** Nodes to the hierarchical structure
- **Edit** existing nodes and their properties
- **Delete** nodes from the structure
- **Edit relations** between nodes

## Using the BOM Editor
1. Select a **Hierarchical Structure submodel template** from the submodel tree.
2. Click on the **Visualization tab** to open the BOM Editor.

### Editing Nodes
- To start editing a node, you have to enter edit mode by clicking the **Edit** button or switching to AASEditor or SubmodelEditor mode.

```{figure} ./images/bv_edit_mode.png
---
width: 30%
alt: BOM Viewer Edit Mode
name: bom_viewer_edit_mode
---
BOM Viewer Edit Mode
```
```{figure} ./images/bv_context.png
---
width: 30%
alt: BOM Viewer Edit Mode
name: bom_viewer_edit_mode
---
BOM Viewer Context Menu
```

- Click on a node to select it. You can then modify its properties in the properties panel.
- To add a new Child Node, right-click on the parent node and select **Add Child Entity** from the context menu.
- To delete a node, select it and click the **Delete** button or use the context menu.

### Editing Relationships
- To Edit a Relationship, click on the Edge (the line between two nodes) and a dialog will appear allowing you to modify the relationship properties.