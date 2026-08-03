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
- **Unified Time Range**: One relative or absolute range controls both data retrieval and every visualization
- **Chart Configuration Options**:
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
   - Select a relative or absolute **Time Range**
4. Click **Fetch Data** to resolve and commit the range, then load matching data
5. In the **Preview Chart** card:
   - Select a **Chart Type** (Line, Area, Scatter, Histogram, Gauge, Display Field)
   - Adjust chart-specific options such as interpolation or histogram bins
   - View the visualization

## Time Range

The time range in **Preview Configuration** applies to the query and to all chart types. It defaults to the last minute and is session-local: reopening the plugin restores the default.

**Relative** ranges can use a preset (`1m`, `5m`, `15m`, `1h`, `6h`, `12h`, `24h`, `7d`, `30d`, or `1y`) or a custom positive value in milliseconds, seconds, minutes, hours, days, weeks, months, or years. Months and years use calendar-aware subtraction.

**Absolute** ranges use local start and end date-times. The plugin converts them to UTC before querying and rejects incomplete or reversed ranges.

When **Fetch Data** is clicked, the relative range is resolved once:

- LinkedSegment ranges end at the current time.
- InternalSegment and ExternalSegment ranges end at the newest available timestamp, which keeps archived data usable.
- Absolute ranges always use their exact start and end.

Changing the selector does not alter LinkedSegment `StartTime` or `EndTime`; those fields describe the segment data rather than transient visualization state. If the committed range contains no records, the plugin shows an empty state instead of stale chart data.

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
- Supports standard Flux time variables and the `{{y-value}}` field placeholder

**Database Configuration:**

- **Endpoint**: URL of the time series database
- **Query**: Flux query to fetch data (supports the variables documented below)
- **API Token**: Authentication token (via UI or `VITE_INFLUXDB_TOKEN` environment variable)

### Flux query variables

Flux queries copied from the InfluxDB query editor or a Grafana Flux panel can use these variables without modification:

| Variable | Value supplied by the plugin |
| --- | --- |
| `v.timeRangeStart` | Selected range start as a UTC RFC 3339 time literal |
| `v.timeRangeStop` | Selected range end as a UTC RFC 3339 time literal |
| `v.windowPeriod` | Range duration divided into approximately 360 points, rounded to milliseconds with a minimum of `1ms` |

The following query is ready to paste into a LinkedSegment `Query` property:

```text
from(bucket: "basyx")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "mqtt_consumer")
  |> filter(fn: (r) => r["_field"] == "{{y-value}}")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```

The three `v.*` variables describe the committed time range. The separate `{{y-value}}` placeholder is replaced with the y-variable selected in the plugin. Other `v.*` references are left untouched, so variables defined inside the Flux query continue to work; unresolved database variables are reported by InfluxDB. The plugin does not rewrite hard-coded `range()` calls or provide arbitrary Grafana dashboard variables.

## Supported Chart Types

### Line Chart

Best for continuous data and trend analysis. Displays time series as connected lines.

**Configurable options:**

- Interpolation mode

### Area Chart

Emphasizes volume and cumulative values by filling the area under the line.

**Configurable options:**

- Interpolation mode

### Scatter Chart

Shows individual data points without connecting lines, ideal for identifying patterns and outliers.

The x-axis uses the time range committed in Preview Configuration.

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
- [InfluxDB query variables](https://docs.influxdata.com/influxdb/v2/visualize-data/variables/)
- [Flux Query Language](https://docs.influxdata.com/flux/)
