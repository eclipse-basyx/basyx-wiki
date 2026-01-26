# BaSyx Python SDK

This documentation provides a comprehensive guide for working with the BaSyx Python SDK to create, host, and visualize Asset Administration Shells (AAS) and Submodels. The example runs in a VS Code Dev Container for a consistent development environment.

For more examples and detailed explanations, see:

- BaSyx Python SDK [Tutorials](https://github.com/eclipse-basyx/basyx-python-sdk/blob/main/sdk/README.md#examples-and-tutorials)
- BaSyx Python SDK [Documentation](https://basyx-python-sdk.readthedocs.io/en/latest/)

## Overview

This example demonstrates three key aspects of working with BaSyx Python SDK:

### Step 1: AAS & Submodel Creation

Creates an Asset Administration Shell with a Submodel containing properties. The AAS represents a digital twin of an asset, while Submodels contain the actual data and functionality.

**Key Features:**

- Define AAS identifiers and asset information
- Create Submodels with typed properties
- Add semantic references for standardization
- Serialize to JSON format

### Step 2: Hosting AAS via BaSyx Repository

Reads AAS data from storage and serves it through a REST API using the BaSyx server infrastructure.

**Endpoints:**

- **AAS Repository:** `http://localhost:8080/api/v3.0/shells`
- **Submodel Repository:** `http://localhost:8080/api/v3.0/submodels`

**Supported Formats:**

- JSON (`.json`)
- XML (`.xml`)
- AASX packages (`.aasx`)

### Step 3: Visualization Dashboard

Interactive web-based dashboard built with Dash that fetches and displays AAS and Submodel data from the BaSyx server.

**Dashboard URL:** `http://127.0.0.1:8050`

## Download Example

Download the complete Dev Container example: [basyx-python-sdk-example.zip](./resources/basyx-python-sdk-example.zip)

## Prerequisites

Before running the example, ensure you have:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VS Code

## Quick Start

1. **Download and Extract**

   Download the example ZIP file and extract it to your desired location.

2. **Open in VS Code**

   Open the extracted folder in Visual Studio Code.

3. **Start Dev Container**

   When prompted, click "Reopen in Container" or press `F1` and select "Dev Containers: Reopen in Container". The container will automatically install all dependencies.

4. **Run the Example**

   Open a terminal in VS Code and run:

   ```bash
   python main.py
   ```

   Select from the interactive menu:
   - `1` - Create AAS and Submodel
   - `2` - Start BaSyx Server
   - `3` - Start Visualization Dashboard
   - `4` - Run Server and Dashboard together
   - `5` - Run all steps sequentially

## Step-by-Step Guide

### Step 1: Creating an AAS and Submodel

The `create_aas.py` script demonstrates how to create an AAS with a Submodel programmatically.

**Run:**

```bash
python create_aas.py
```

**Code Explanation:**

#### Define AAS Identifiers

```python
from basyx.aas import model

aas_identifier = "https://example.com/AAS"
submodel_identifier = "https://example.com/Submodel"
```

Identifiers uniquely identify AAS and Submodels. Use URIs for global uniqueness.

#### Create Asset Information

```python
asset_info = model.AssetInformation(
    asset_kind=model.AssetKind.INSTANCE,
    global_asset_id="Asset1"
)
```

The `AssetInformation` describes the physical or logical asset that the AAS represents. `AssetKind.INSTANCE` indicates a specific asset instance (as opposed to a type).

#### Create the Asset Administration Shell

```python
aas = model.AssetAdministrationShell(
    asset_information=asset_info,
    id_=model.Identifier(aas_identifier)
)
```

The AAS is the digital representation of the asset. It contains references to Submodels but no data itself.

#### Create and Link a Submodel

```python
submodel = model.Submodel(id_=model.Identifier(submodel_identifier))
submodel_reference = model.ModelReference.from_referable(submodel)
aas.submodel.add(submodel_reference)
```

Submodels contain the actual data. The AAS holds references to Submodels, allowing modular organization.

#### Define Properties

```python
prop1 = model.Property(
    id_short="Temperature",
    value_type=model.datatypes.Float,
    value=25.3,
    semantic_id=model.ExternalReference((
        model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value='http://acplt.org/Properties/FirstSimpleProperty'
        ),
    ))
)

submodel.submodel_element.add(prop1)
```

Properties are the basic data elements. Each property has:

- `id_short`: A human-readable identifier
- `value_type`: The data type (Float, Integer, String, etc.)
- `value`: The actual value
- `semantic_id`: Optional reference to a standardized definition

#### Serialize to JSON

```python
from basyx.aas.adapter.json import write_aas_json_file

data = model.DictObjectStore()
data.add(aas)
data.add(submodel)

write_aas_json_file("storage/aas_data.json", data)
```

The `DictObjectStore` holds multiple AAS objects. The JSON adapter serializes them according to the AAS specification.

### Step 2: Hosting the AAS via BaSyx Server

The `start_server.py` script starts a BaSyx server that exposes AAS data via REST API.

**Run:**

```bash
python start_server.py
```

Keep this running in a separate terminal.

**Code Explanation:**

#### Load AAS Files

```python
import pathlib
from basyx.aas import adapter

object_store = model.DictObjectStore()

for file in pathlib.Path(storage_path).iterdir():
    if file.suffix.lower() == ".json":
        with open(file, 'r') as f:
            adapter.json.read_aas_json_file_into(object_store, f)
```

The server scans the storage directory and loads all AAS files (JSON, XML, or AASX) into an in-memory object store.

#### Create WSGI Application

```python
from basyx.aas.adapter.http import WSGIApp

application = WSGIApp(object_store, file_store)
```

The `WSGIApp` creates a REST API that exposes the AAS data according to the official AAS API specification.

#### Start the Server

```python
from waitress import serve

serve(application, host="0.0.0.0", port=8080)
```

Waitress is a production-ready WSGI server that serves the BaSyx application on port 8080.

**API Endpoints:**

- `GET /api/v3.0/shells` - List all AAS
- `GET /api/v3.0/shells/{aasIdentifier}` - Get specific AAS
- `GET /api/v3.0/submodels` - List all Submodels
- `GET /api/v3.0/submodels/{submodelIdentifier}` - Get specific Submodel

### Step 3: Visualizing AAS Data

The `visualization.py` script creates an interactive dashboard using Dash.

**Run:**

```bash
python visualization.py
```

Access the dashboard at [http://localhost:8050](http://localhost:8050)

**Code Explanation:**

#### Fetch Data from BaSyx Server

```python
import requests

def fetch_aas_data():
    response = requests.get("http://localhost:8080/api/v3.0/shells")
    return response.json()
```

Uses the `requests` library to fetch AAS data from the running BaSyx server.

#### Create Dash Application

```python
import dash
from dash import html, Input, Output

app = dash.Dash(__name__)
```

Dash is a Python framework for building web applications. It's built on top of Flask, Plotly.js, and React.

#### Define Layout

```python
app.layout = html.Div([
    html.H1("BaSyx AAS Viewer"),
    html.Button("🔄 Refresh Data", id="refresh-btn", n_clicks=0),
    html.Div(id="aas-output"),
    html.Div(id="submodels-output")
])
```

The layout defines the structure of the web page using HTML components.

#### Add Callbacks

```python
@app.callback(
    [Output("aas-output", "children"),
     Output("submodels-output", "children")],
    [Input("refresh-btn", "n_clicks")]
)
def update_view(n_clicks):
    aas_data = fetch_aas_data()
    submodel_data = fetch_submodel_data()
    return html.Pre(str(aas_data)), html.Pre(str(submodel_data))
```

Callbacks make the app interactive. When the refresh button is clicked, the callback fetches fresh data and updates the display.

#### Run the Server

```python
app.run_server(debug=True, port=8050)
```

Starts the Dash development server on port 8050.

## Project Structure

```text
resources/
├── .devcontainer/
│   └── devcontainer.json      # Dev container configuration
├── storage/                   # AAS data storage directory
│   └── .gitkeep              # Placeholder for empty directory
├── Dockerfile                 # Container image definition
├── requirements.txt           # Python dependencies
├── main.py                    # Main script with interactive menu
├── create_aas.py             # Step 1: Create AAS and Submodel
├── start_server.py           # Step 2: Start BaSyx server
├── visualization.py          # Step 3: Dash visualization
└── README.md                 # Example documentation
```

## Configuration

### Environment Variables

Configure the BaSyx server behavior using environment variables:

- **`STORAGE_TYPE`** (default: `LOCAL_FILE_READ_ONLY`)
  - `LOCAL_FILE_READ_ONLY`: Read-only mode, loads files into memory
  - `LOCAL_FILE_BACKEND`: Writable backend for persistence

- **`API_BASE_PATH`** (optional)
  - Custom base path for API endpoints (e.g., `/basyx`)

Example:

```bash
export STORAGE_TYPE=LOCAL_FILE_BACKEND
python start_server.py
```

## Troubleshooting

### Port Already in Use

If you encounter port conflicts:

```bash
# Kill process on port 8080
lsof -ti:8080 | xargs kill -9

# Kill process on port 8050
lsof -ti:8050 | xargs kill -9
```

### Server Connection Failed

If the visualization cannot connect:

1. Ensure the BaSyx server is running (`python start_server.py`)
2. Verify server accessibility: [http://localhost:8080/api/v3.0/shells](http://localhost:8080/api/v3.0/shells)
3. Check that `storage/aas_data.json` exists

### No AAS Data Found

If the server reports no data:

1. Run `python create_aas.py` to generate example data
2. Verify `storage/aas_data.json` exists and is valid JSON

## Additional Resources

### Additional Resources BaSyx Python SDK

- [GitHub Repository](https://github.com/eclipse-basyx/basyx-python-sdk)
- [API Documentation](https://basyx-python-sdk.readthedocs.io/en/latest/)
- [Examples and Tutorials](https://github.com/eclipse-basyx/basyx-python-sdk/blob/main/sdk/README.md#examples-and-tutorials)

### Asset Administration Shell

- [Official Specification](https://industrialdigitaltwin.io/aas-specifications/index/home/index.html)
- [AAS Meta Model](https://github.com/admin-shell-io/aas-specs-metamodel)
- [AAS API](https://github.com/admin-shell-io/aas-specs-api)
- [Iindustrial Digital Twin Association](https://industrialdigitaltwin.org/)

### Related Components

- [BaSyx Components](../../user_documentation/basyx_components/)
- [BaSyx DockerHub](https://hub.docker.com/u/eclipsebasyx)
- [BaSyx Web UI](../../user_documentation/basyx_components/web_ui/)
