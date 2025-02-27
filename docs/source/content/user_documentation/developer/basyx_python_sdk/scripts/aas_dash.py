import requests
import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd


API_URL = "http://localhost:8080/api/v3.0/shells"
API_SUBMODEL_URL = "http://localhost:8080/api/v3.0/submodels"

def fetch_aas_data():
    """Fetch AAS data from the Basyx server."""
    try:
        response = requests.get(API_URL)
        data = response.json()
        return data  # Return full AAS data
    except Exception as e:
        return {"error": str(e)}
    
def fetch_submodel_data():
    """Fetch submodel data from the Basyx server."""
    try:
        response = requests.get(API_SUBMODEL_URL)
        data = response.json()
        return data  # Return full submodel data
    except Exception as e:
        return {"error": str(e)}
    
def fetch_submodel_data_prev():
    """Fetch Submodel data from the BaSyx server and parse its elements."""
    try:
        headers = {"Accept": "application/json"}  # Ensure JSON response
        response = requests.get(API_SUBMODEL_URL, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract submodels list
            submodels = data.get("result", [])  
            submodel_data = []
            
            for sub in submodels:
                submodel_id = sub.get("id", "Unknown")
                submodel_elements = sub.get("submodelElements", [])
                
                # Extract properties
                properties = [
                    f"{prop['idShort']}: {prop.get('value', 'N/A')}" 
                    for prop in submodel_elements
                ]
                
                # Store submodel as dict
                submodel_data.append({
                    "id": submodel_id,
                    "properties": properties
                })
            
            return submodel_data  # Return structured list
        
    except Exception as e:
        print(f"Error fetching Submodel data: {e}")
    
    return []


# Initialize Dash App
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div([
    html.H1("AAS Viewer - Dash Web App"),
    html.Button("Refresh Data", id="refresh-btn", n_clicks=0),
    html.H3("Asset Administration Shells"),
    html.Div(id="aas-output"),
    html.H3("Submodels"),
html.Div(id="submodels-output")   
])

# Callback to Update AAS Output and Submodels Table
@app.callback(
    [Output("aas-output", "children"),
     Output("submodels-output", "children")],
    [Input("refresh-btn", "n_clicks")]
)
def update_view(n_clicks):
    aas_data = fetch_aas_data()
    submodels = fetch_submodel_data()
    
    # Convert JSON data into a readable format
    aas_tree = html.Pre(str(aas_data), style={"whiteSpace": "pre-wrap"})
    #aas_list = [html.Pre(json.dumps(aas, indent=2)) for aas in aas_data]

    submodel_tree = html.Pre(str(submodels), style={"whiteSpace": "pre-wrap"})

    return aas_tree, submodel_tree #return aas_tree, table_data

# Run the Dash App
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
