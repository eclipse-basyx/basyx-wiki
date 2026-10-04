# Production Calendar

> **As a** BaSyx AAS Web UI user  
> **I want to** see the shifts, breaks and maintenance windows of a machine or production line in a calendar  
> **so that** I can tell at a glance when the asset is planned to produce, to pause or to be serviced.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- `https://admin-shell.io/idta/SubmodelTemplate/ProductionCalendar/1/0`

## Feature Overview

The Production Calendar plugin visualizes Submodels based on the IDTA Submodel Template *Production Calendar*. The Submodel stores the calendar as an iCalendar file (RFC 5545, `.ics`). The plugin loads this file, expands its events (including recurring ones) and shows them in a week or month view. Below the calendar, the specification extension variables that give the `X-` properties of the file their meaning are listed.

All times are shown as wall-clock time of the time zone of the calendar (for example `Europe/Berlin`), independent of the time zone of the browser. The time zone is shown as a badge next to the title.

```{figure} ./images/production_calendar_week.png
---
width: 100%
alt: Production Calendar Plugin, week view
name: production_calendar_plugin_week
---
Production Calendar Plugin in the week view
```

## Key Features

- **Week and month view**: Switch between both views with the toggle in the upper right corner. The arrows and *Today* navigate through time. The week view starts on Monday and shows only the hours in which events occur
- **Recurring events**: Recurrence rules (`RRULE`, for example *every weekday* or *first Saturday of the month*), exception dates (`EXDATE`, for example public holidays), single changed occurrences (`RECURRENCE-ID`), `RDATE`, `DURATION` and all-day events are supported
- **Time zones**: Events with a `TZID` (and the embedded `VTIMEZONE`), in UTC or without a time zone (floating) are displayed correctly, also across the change to and from daylight saving time
- **Color coding**: Events are colored by their `CATEGORIES` or `X-` property: production (green), break (orange), maintenance (red) and all other events (grey). A legend below the calendar lists the kinds that occur in the visible period
- **Event details**: Select an event to see its name, time, description, location, categories and `X-` properties
- **Specification extension variables**: Each `X-` property that is defined in the Submodel (for example `X-PRODUCTION-DAY`, `X-BREAK`, `X-MAINTENANCE`) is listed with its specification text. A badge shows whether the property is used in the calendar

```{figure} ./images/production_calendar_month.png
---
width: 100%
alt: Production Calendar Plugin, month view
name: production_calendar_plugin_month
---
Month view of the same calendar
```

```{figure} ./images/production_calendar_event.png
---
width: 100%
alt: Production Calendar Plugin, event details
name: production_calendar_plugin_event
---
Details of an event
```

## Usage

1. Navigate to a Submodel with the Production Calendar semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. Switch between **Week** and **Month** and move through the calendar with the arrow buttons. Use **Today** to return to the current date
4. Select an event to see its details
5. Expand an entry of **Specification Extension Variables** to read the specification of the property

```{figure} ./images/production_calendar_specs.png
---
width: 100%
alt: Specification extension variables of the Production Calendar Plugin
name: production_calendar_plugin_specs
---
Specification extension variables below the calendar
```

## Submodel Structure

The plugin expects the following structure, based on the IDTA Submodel Template *Production Calendar*:

| idShort | Type | Description |
|---------|------|-------------|
| `calendar` | `File` (`text/calendar`) | The iCalendar file (`.ics`) with the events. Required |
| `specificationExtensionVariables` | `SubmodelElementList` | Optional. One entry per `X-` property used in the calendar |

Each entry of `specificationExtensionVariables` is a `SubmodelElementCollection` with:

| idShort | Type | Description |
|---------|------|-------------|
| `variableName` | `Property` (`xs:string`) | Name of the `X-` property, for example `X-BREAK` |
| `variableSpecification` | `File` (`text/plain`) | Text that describes the meaning and the allowed values of the property |

The elements are found by their semantic ID or by their idShort.

## Classification of Events

An event is assigned to one of the following kinds. The `CATEGORIES` of the event are checked first, then the names of its `X-` properties (a property with the value `FALSE` is ignored):

| Kind | Color | Matches (case-insensitive) |
|------|-------|----------------------------|
| Break | orange | `break`, `pause` |
| Maintenance | red | `maint`, `service` |
| Production | green | `production`, `shift` |
| Other | grey | everything else |

## Limitations

- The file must be a valid iCalendar document. Otherwise an error message is shown instead of the calendar
- If the time zone of the calendar cannot be resolved to an IANA time zone (`X-WR-TIMEZONE` or the `TZID` of the first `VTIMEZONE`), the calendar is shown in UTC
- The calendar is read-only. Editing events is not supported
