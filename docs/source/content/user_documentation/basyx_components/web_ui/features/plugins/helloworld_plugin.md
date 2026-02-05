# HelloWorld Plugin

> **As a** BaSyx AAS Web UI developer  
> **I want to** use a simple example plugin as a starting point  
> **so that** I can learn how to create custom Submodel plugins.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- `http://hello.world.de/plugin_submodel`

## Feature Overview

The HelloWorld Plugin is a simple example plugin designed specifically for developers who want to create their own custom plugins for the BaSyx AAS Web UI. It demonstrates the basic structure and functionality of a Submodel plugin by displaying Submodel content in a generic way.

```{figure} ./images/helloworld_plugin.png
---
width: 100%
alt: HelloWorld Plugin
name: helloworld_plugin
---
HelloWorld Plugin Example
```

## Purpose

This plugin serves as a **template and learning resource** for plugin development. It is not intended for production use but rather as a starting point that demonstrates:

- How plugins are structured
- How to access Submodel data
- How to display SubmodelElements
- Best practices for plugin development

## Key Features

- **Generic Submodel Display**: Shows all SubmodelElements in a simple format
- **Clean Code Structure**: Well-documented code that's easy to understand
- **Minimal Dependencies**: Uses only core UI components
- **Extensible Design**: Easy to modify and extend for specific use cases

## Usage

### As a Developer

1. Examine the plugin source code to understand the structure
2. Copy the plugin as a starting point for your own plugin
3. Modify the semantic ID to match your target Submodel
4. Customize the visualization and interaction logic
5. Add domain-specific features as needed

### For Testing

1. Create a test Submodel with the semantic ID `http://hello.world.de/plugin_submodel`
2. Add various SubmodelElements to test different element types
3. Navigate to the Submodel in the AAS Treeview
4. Open the **Visualization** tab to see the HelloWorld Plugin in action

## Plugin Structure

The HelloWorld Plugin demonstrates the following plugin components:

### Data Handling

- Receiving Submodel data as prop from the UI
- Parsing SubmodelElements
- Handling different element types

### Visualization

- Rendering SubmodelElements in a generic view
- Displaying properties, values, and metadata
- Organizing elements hierarchically

## Learning Resources

To learn more about creating custom plugins:

- Review the [Plugin Development Guide](../../../../../developer_documentation/basyx_web_ui/creating_submodel_plugins.md)
- Study the source code of other plugins in the repository
- Experiment with the HelloWorld Plugin by modifying it
- Join the BaSyx community for support and discussions

## Best Practices

When developing plugins based on the HelloWorld Plugin:

- **Keep it simple**: Start with basic functionality and add features incrementally
- **Follow conventions**: Use the same patterns as existing plugins
- **Document thoroughly**: Make your code easy for others to understand
- **Test extensively**: Ensure your plugin works in all scenarios
- **Consider reusability**: Design components that can be reused
- **Handle errors gracefully**: Provide meaningful error messages

## Notes

```{note}
The HelloWorld Plugin is **not an official IDTA Submodel template**. It's a development tool created by the BaSyx community for educational purposes.
```

```{hint}
If you create a useful plugin, consider contributing it back to the BaSyx project so others can benefit from your work!
```
