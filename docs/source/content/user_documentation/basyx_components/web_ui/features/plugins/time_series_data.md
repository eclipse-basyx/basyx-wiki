# Time Series Data

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Time Series Data Submodels using different chart types  
> **so that** I can analyze temporal data patterns and trends.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- **V1.1**: `https://admin-shell.io/idta/TimeSeries/1/1`

## Feature Overview

The Time Series Data plugin provides powerful visualization capabilities for time-based data stored in Asset Administration Shells according to the IDTA Time Series Data specification. It supports three segment types for storing and accessing time series data:

1. **InternalSegment**: Time series data stored directly within the AAS Submodel
2. **ExternalSegment**: Time series data stored in files or blob SubmodelElements (e.g., CSV files)
3. **LinkedSegment**: Time series data from linked time series databases (e.g., InfluxDB)

The plugin offers multiple chart types for visualization, making it ideal for monitoring, analysis, and historical data review.

```{note}
For a complete working example with InfluxDB, MQTT, and all three segment types, see the [TimeSeriesData example on GitHub](https://github.com/eclipse-basyx/basyx-aas-web-ui/tree/main/examples/TimeSeriesData).
```

```{figure} ./images/time_series_data.png
---
width: 100%
alt: Time Series Data Plugin
name: time_series_data_plugin
---
Time Series Data Plugin
```
## Key Features

- **Three Segment Types**:
  - **InternalSegment**: Data defined within the AAS
  - **ExternalSegment**: Data from files or blob SubmodelElements (CSV with RFC 4180 format)
  - **LinkedSegment**: Real-time data from time series databases (InfluxDB tested)
- **Multiple Chart Types**: Line Chart, Area Chart, Scatter Chart, Histogram, Gauge, Display Field
- **Chart Configuration Options**:
  - Time range selection
  - Interpolation mode
  - Number of bins (for Histogram)
  - Stacked bars (for Histogram)
- **Interactive Charts**: Zoom, pan, and hover for detailed information
- **Multi-series Support**: Display and compare multiple y-variables simultaneously
- **Database Integration**: Direct connection to InfluxDB with API token authentication
- **Variable Selection**: Choose time variable and multiple y-variables from the submodel metadata

## Usage

### General Steps

1. Navigate to a Submodel with the Time Series Data semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. In the **Preview Configuration** card:
   - Select a **Segment** (Internal, External, or Linked)
   - Select the **time variable** from the metadata records
   - Select one or more **y-variables** to visualize
4. Click **Fetch Data** to load the time series data
5. In the **Preview Chart** card:
   - Select a **Chart Type** (Line, Area, Scatter, Histogram, Gauge, Display Field)
   - Adjust chart options if needed (time range, interpolation, etc.)
   - View the visualization

## Segment Types

### InternalSegment

**InternalSegment** defines time series data directly within the AAS Submodel structure. Data points are stored as properties with timestamps and values, making it suitable for small to medium-sized datasets that don't change frequently.

**Characteristics:**

- Data embedded in the Submodel
- No external dependencies
- Best for static or infrequently updated data
- Immediate availability

### ExternalSegment

**ExternalSegment** references time series data stored in files or blob SubmodelElements. The plugin supports CSV files following RFC 4180 format with a header line.

**Characteristics:**

- Data stored in separate files
- Supports larger datasets
- CSV format with headers (time column + value columns)
- Referenced via File SubmodelElement
- Suitable for archived or batch data

### LinkedSegment

**LinkedSegment** connects to external time series databases for real-time or large-scale data. The example includes InfluxDB with Telegraf for MQTT data ingestion.

**Characteristics:**

- Real-time data access
- Scalable for large datasets
- Supports time series databases (InfluxDB tested)
- Configurable queries using Flux language
- API token authentication
- Can use `{{y-value}}` template in queries for dynamic y-variable injection

**Database Configuration:**

- **Endpoint**: URL of the time series database
- **Query**: Flux query to fetch data (supports `{{y-value}}` placeholder)
- **API Token**: Authentication token (via UI or `VITE_INFLUXDB_TOKEN` environment variable)

## Supported Chart Types

### Line Chart

Best for continuous data and trend analysis. Displays time series as connected lines.

**Configurable options:**

- Time range selection
- Interpolation mode

### Area Chart

Emphasizes volume and cumulative values by filling the area under the line.

**Configurable options:**

- Time range selection
- Interpolation mode

### Scatter Chart

Shows individual data points without connecting lines, ideal for identifying patterns and outliers.

**Configurable options:**

- Time range selection

### Histogram

Displays the distribution of values in bins, useful for frequency analysis.

**Configurable options:**

- Number of bins
- Stacked bars option

### Gauge

Displays the latest value as a gauge, ideal for real-time monitoring of current states.

### Display Field

Shows the most recent value for each y-variable in a simple text display with units.

## Working Example

A complete Docker Compose example demonstrating all three segment types is available in the BaSyx AAS Web UI repository:

**[TimeSeriesData Example](https://github.com/eclipse-basyx/basyx-aas-web-ui/tree/main/examples/TimeSeriesData)**

The example includes:

- InfluxDB time series database
- Telegraf for MQTT data ingestion
- MQTT publisher for simulated sensor data
- Pre-configured AAS with all three segment types
- Demo data for immediate testing

## References

- [IDTA Time Series Data V1.1 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2023/03/IDTA-02008-1-1_Submodel_TimeSeriesData.pdf)
- [TimeSeriesData Example (GitHub)](https://github.com/eclipse-basyx/basyx-aas-web-ui/tree/main/examples/TimeSeriesData)
- [InfluxDB Documentation](https://docs.influxdata.com/)
- [Flux Query Language](https://docs.influxdata.com/flux/)
