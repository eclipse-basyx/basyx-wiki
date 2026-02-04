# Time Series Data

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Time Series Data Submodels using different chart types  
> **so that** I can analyze temporal data patterns and trends.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- **V1.1**: `https://admin-shell.io/idta/TimeSeries/1/1`

## Feature Overview

The Time Series Data plugin provides powerful visualization capabilities for time-based data stored in Asset Administration Shells. It supports multiple data sources and chart types, making it ideal for monitoring, analysis, and historical data review.

```{figure} ./images/time_series_data.png
---
width: 100%
alt: Time Series Data Plugin
name: time_series_data_plugin
---
Time Series Data Plugin
```

## Key Features

- **Multiple Chart Types**: Line charts, bar charts, area charts, and more
- **Flexible Data Sources**: 
  - AAS Properties
  - File SubmodelElements (CSV, JSON)
  - External time series databases (InfluxDB)
- **Interactive Charts**: Zoom, pan, and hover for detailed information
- **Time Range Selection**: Filter data by specific time ranges
- **Multi-series Support**: Display and compare multiple time series simultaneously
- **Export Capabilities**: Export chart data and images

## Usage

1. Navigate to a Submodel with the Time Series Data semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The plugin will automatically load and display the time series data
4. Use the chart controls to:
   - Select different chart types
   - Adjust time ranges
   - Toggle individual series on/off
   - Zoom into specific time periods
5. Export data or charts as needed

## Data Source Configuration

### AAS Properties
Time series data can be stored directly as Property values within the Submodel. The plugin reads the configured properties and renders them chronologically.

### File SubmodelElements
CSV or JSON files containing time series data can be referenced as File SubmodelElements. The plugin parses these files and visualizes the data.

### External Databases (InfluxDB)
For large-scale time series data, the plugin can connect to external InfluxDB instances. Connection details are configured within the Submodel.

```{figure} ./images/time_series_config.png
---
width: 80%
alt: Time Series Data Configuration
name: time_series_config
---
Time Series Data Source Configuration
```

## Supported Chart Types

- **Line Chart**: Best for continuous data and trend analysis
- **Bar Chart**: Ideal for discrete time intervals and comparisons
- **Area Chart**: Emphasizes volume and cumulative values
- **Scatter Plot**: Shows individual data points and correlations
- **Step Chart**: For data that changes in discrete steps

## References

- [IDTA Time Series Data V1.1 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2023/03/IDTA-02008-1-1_Submodel_TimeSeriesData.pdf)
