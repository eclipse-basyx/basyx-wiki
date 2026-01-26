# BaSyx Python SDK - Dev Container Example

This example demonstrates how to use the BaSyx Python SDK to create, host, and visualize Asset Administration Shells (AAS) and Submodels.

## 🚀 Quick Start

### Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VS Code

### Running the Example

1. **Open in Dev Container**
   - Open this folder in VS Code
   - When prompted, click "Reopen in Container" (or press `F1` → "Dev Containers: Reopen in Container")
   - Wait for the container to build and dependencies to install

2. **Run the Example**
   ```bash
   python main.py
   ```
   
   This will present you with an interactive menu to:
   - Create an AAS and Submodel
   - Start the BaSyx server
   - Start the visualization dashboard
   - Run all steps together

3. **Access the Services**
   - **BaSyx AAS API**: [http://localhost:8080/api/v3.0/shells](http://localhost:8080/api/v3.0/shells)
   - **Submodel API**: [http://localhost:8080/api/v3.0/submodels](http://localhost:8080/api/v3.0/submodels)
   - **Visualization Dashboard**: [http://localhost:8050](http://localhost:8050)

## 📁 Project Structure

```
.
├── .devcontainer/
│   └── devcontainer.json      # Dev container configuration
├── storage/                   # AAS data storage (created at runtime)
├── Dockerfile                 # Container image definition
├── requirements.txt           # Python dependencies
├── main.py                    # Main script with interactive menu
├── create_aas.py             # Step 1: Create AAS and Submodel
├── start_server.py           # Step 2: Start BaSyx server
├── visualization.py          # Step 3: Dash visualization dashboard
└── README.md                 # This file
```

## 🔧 Running Individual Steps

### Step 1: Create AAS and Submodel

```bash
python create_aas.py
```

Creates an example AAS with a Submodel containing two properties:
- `Temperature`: 25.3°C (Float)
- `Pressure`: 100 bar (Integer)

The data is saved to `storage/aas_data.json`.

### Step 2: Start BaSyx Server

```bash
python start_server.py
```

Starts the BaSyx AAS and Submodel server on port 8080. The server reads AAS data from the `storage/` directory and provides REST API endpoints.

**Important**: Keep this running in a separate terminal for the visualization to work.

### Step 3: Start Visualization Dashboard

```bash
python visualization.py
```

Launches a Dash web application on port 8050 that fetches and displays AAS and Submodel data from the BaSyx server.

**Note**: The BaSyx server (Step 2) must be running before starting the visualization.

## 🛠️ Development

### Environment Variables

- `STORAGE_TYPE`: Storage backend type (default: `LOCAL_FILE_READ_ONLY`)
  - `LOCAL_FILE_READ_ONLY`: Read-only mode, loads files into memory
  - `LOCAL_FILE_BACKEND`: Writable backend, changes can be persisted
- `API_BASE_PATH`: Optional base path for the API endpoints

### Modifying the Example

1. **Change AAS Properties**: Edit `create_aas.py` to add more properties or submodels
2. **Customize Visualization**: Modify `visualization.py` to change the dashboard layout
3. **Add More Data**: Place additional `.json`, `.xml`, or `.aasx` files in the `storage/` directory

## 📚 Learn More

- [BaSyx Python SDK Documentation](https://basyx-python-sdk.readthedocs.io/en/latest/)
- [BaSyx Python SDK GitHub](https://github.com/eclipse-basyx/basyx-python-sdk)
- [Asset Administration Shell Specification](https://www.plattform-i40.de/IP/Redaktion/EN/Standardartikel/specification-administrationshell.html)

## 🐛 Troubleshooting

### Port Already in Use

If you see an error about ports 8080 or 8050 being already in use:
```bash
# Find and stop the process using the port
lsof -ti:8080 | xargs kill -9  # For BaSyx server
lsof -ti:8050 | xargs kill -9  # For visualization
```

### Server Connection Failed

If the visualization cannot connect to the server:
1. Make sure the BaSyx server is running (`python start_server.py`)
2. Verify the server is accessible at [http://localhost:8080/api/v3.0/shells](http://localhost:8080/api/v3.0/shells)
3. Check that the `storage/aas_data.json` file exists (run `python create_aas.py` if not)

### No AAS Data Found

If the server reports no AAS data:
1. Run `python create_aas.py` to generate the example data
2. Check that `storage/aas_data.json` exists and is not empty

## 📄 License

This example is part of the Eclipse BaSyx project and is licensed under the Eclipse Public License 2.0.
