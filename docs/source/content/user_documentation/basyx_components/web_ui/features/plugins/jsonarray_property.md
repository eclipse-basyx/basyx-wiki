# JSONArray Property

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize data series from Property values in charts  
> **so that** I can analyze numerical data patterns without external data sources.

## Semantic ID

This plugin is activated when a SubmodelElement has the following semantic ID:

- `http://iese.fraunhofer.de/prop_jsonarray`

## Feature Overview

The JSONArray Property plugin enables visualization of numerical data series stored directly in Property values. Unlike the Time Series Data plugin which requires structured Submodels, this plugin works with simple Properties containing JSON array data, making it ideal for quick data visualization without complex setup.

```{figure} ./images/jsonarray_property.png
---
width: 100%
alt: JSONArray Property Plugin
name: jsonarray_property_plugin
---
JSONArray Property Plugin with Single Series
```

## Key Features

- **Simple Data Format**: Works with Properties containing JSON arrays
- **Single or Multiple Series**: Visualize one or many data series simultaneously
- **Interactive Visualization**: Zoom, pan, and hover for details
- **No External Dependencies**: Data stored directly in the AAS
- **Easy Setup**: No additional configuration required

## Usage

1. Create a Property with the semantic ID `http://iese.fraunhofer.de/prop_jsonarray`
2. Set the Property value to a JSON array (see formats below)
3. Navigate to the Property in the AAS Treeview
4. Open the **Visualization** tab
5. The plugin automatically renders the data as a chart

## Supported Data Formats

### Single Series Format

For a single data series, use a simple JSON array:

```json
[31, 45, 23, 40, 45, 38]
```

This will display as a single line/bar series in the chart.

```{figure} ./images/jsonarray_single.png
---
width: 80%
alt: JSONArray Single Series
name: jsonarray_single
---
Single Series Visualization
```

### Multiple Series Format

For multiple data series, use a JSON object with named series:

```json
{
  "series1": [31, 40, 28, 51, 42, 109, 100],
  "Series2": [11, 32, 45, 32, 34, 52, 41]
}
```

Each series will be displayed with a different color and can be toggled on/off in the legend.

```{figure} ./images/jsonarray_multiple.png
---
width: 80%
alt: JSONArray Multiple Series
name: jsonarray_multiple
---
Multiple Series Visualization
```

## Chart Customization

The plugin provides various customization options:

### Display Options

- **Toggle Series**: Click on legend items to show/hide series
- **Zoom**: Select an area to zoom in
- **Pan**: Drag to move the visible area
- **Reset Zoom**: Return to the original view

### Color Schemes

- Each series automatically gets a distinct color
- Colors are consistent across views
- Accessible color palette for better readability

## Use Cases

### Sensor Readings

Store and visualize sensor measurements:

```json
{
  "Temperature": [22.1, 22.3, 22.5, 22.8, 23.0, 22.9],
  "Humidity": [45, 46, 47, 48, 47, 46]
}
```

### Performance Metrics

Track system performance over time:

```json
{
  "CPU Usage": [45, 52, 48, 61, 58, 55, 50],
  "Memory Usage": [68, 70, 72, 75, 73, 71, 69]
}
```

### Quality Measurements

Monitor product quality parameters:

```json
[98.5, 99.1, 98.8, 99.3, 99.0, 98.9, 99.2]
```

### Production Counts

Track production quantities:

```json
{
  "ProductA": [120, 135, 128, 142, 138, 145],
  "ProductB": [95, 102, 98, 105, 101, 108]
}
```

## Advantages

### Compared to Time Series Data Submodel

- **Simpler Setup**: No need for complex Submodel structure
- **Lightweight**: Less overhead for small datasets
- **Quick Prototyping**: Fast way to visualize data during development
- **Embedded Data**: Everything in one Property value

### Compared to File-based Storage

- **Direct Access**: No need to parse external files
- **Real-time Updates**: Changes immediately visible
- **No File Management**: No separate file storage needed

## Limitations

- **No Time Information**: Data points are indexed numerically, not by timestamp
- **Size Constraints**: Property values have size limits; not suitable for very large datasets
- **Limited Metadata**: No built-in support for units, labels, or descriptions per data point
- **No Database Queries**: Cannot filter or aggregate data like with time series databases

## Best Practices

1. **Keep It Reasonable**: Use for small to medium datasets (< 1000 points per series)
2. **Name Series Meaningfully**: Use descriptive names in the multiple series format
3. **Document Units**: Add description to the Property explaining units and context
4. **Consider Alternatives**: For large datasets or time-based data, use the Time Series Data plugin instead

## Example Property Configuration

Here's how to configure a Property for the JSONArray plugin:

```json
{
  "idShort": "PerformanceData",
  "modelType": "Property",
  "semanticId": {
    "keys": [{
      "type": "GlobalReference",
      "value": "http://iese.fraunhofer.de/prop_jsonarray"
    }]
  },
  "valueType": "xs:string",
  "value": "{\"CPU\": [45, 52, 48, 61], \"Memory\": [68, 70, 72, 75]}",
  "description": [
    {
      "language": "en",
      "text": "System performance metrics over last 4 hours. Values in percent."
    }
  ]
}
```
