"""
Step 3: Visualization of AAS and submodel data through Dash Web Application

This script demonstrates how to:
- Fetch AAS data from the BaSyx server
- Create an interactive web dashboard using Dash
- Visualize AAS and Submodel data in a user-friendly format
"""

import time
import requests
import dash
from dash import html, Input, Output


# API endpoints
API_URL = "http://localhost:8080/api/v3.0/shells"
API_SUBMODEL_URL = "http://localhost:8080/api/v3.0/submodels"


def fetch_aas_data():
    """
    Fetch AAS data from the BaSyx server.
    Implements retry logic to handle server startup delays.
    """
    for attempt in range(5):
        try:
            response = requests.get(API_URL, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            if attempt < 4:
                print(f"🔁 AAS server not ready yet. Retrying in 2 seconds... (Attempt {attempt + 1}/5)")
                time.sleep(2)
            else:
                return {"error": "❌ Failed to connect to AAS server. Please ensure the server is running."}
        except requests.exceptions.RequestException as e:
            return {"error": f"❌ Error fetching AAS data: {str(e)}"}
    
    return {"error": "❌ Failed to fetch AAS data after 5 attempts"}


def fetch_submodel_data():
    """
    Fetch submodel data from the BaSyx server.
    Implements retry logic to handle server startup delays.
    """
    for attempt in range(5):
        try:
            response = requests.get(API_SUBMODEL_URL, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            if attempt < 4:
                print(f"🔁 Submodel server not ready yet. Retrying in 2 seconds... (Attempt {attempt + 1}/5)")
                time.sleep(2)
            else:
                return {"error": "❌ Failed to connect to Submodel server. Please ensure the server is running."}
        except requests.exceptions.RequestException as e:
            return {"error": f"❌ Error fetching Submodel data: {str(e)}"}
    
    return {"error": "❌ Failed to fetch Submodel data after 5 attempts"}


def create_dash_app():
    """Create and configure the Dash application."""
    
    # Initialize the Dash app
    app = dash.Dash(__name__)
    
    # Define the layout of the web application
    app.layout = html.Div([
        html.H1(
            "BaSyx AAS Viewer",
            style={
                "textAlign": "center",
                "color": "#FF8C00",
                "marginBottom": "30px"
            }
        ),
        
        html.Div([
            html.Button(
                "🔄 Refresh Data",
                id="refresh-btn",
                n_clicks=0,
                style={
                    "fontSize": "16px",
                    "padding": "10px 20px",
                    "marginBottom": "20px",
                    "cursor": "pointer",
                    "backgroundColor": "#FF8C00",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "5px"
                }
            )
        ], style={"textAlign": "center"}),
        
        html.Hr(),
        
        html.H2(
            "Asset Administration Shells",
            style={"color": "#333", "marginTop": "20px"}
        ),
        html.Div(
            id="aas-output",
            style={
                "backgroundColor": "#f5f5f5",
                "padding": "15px",
                "borderRadius": "5px",
                "marginBottom": "30px"
            }
        ),
        
        html.H2(
            "Submodels",
            style={"color": "#333"}
        ),
        html.Div(
            id="submodels-output",
            style={
                "backgroundColor": "#f5f5f5",
                "padding": "15px",
                "borderRadius": "5px"
            }
        )
    ], style={"maxWidth": "1200px", "margin": "0 auto", "padding": "20px"})
    
    # Callback to update AAS and Submodels output
    @app.callback(
        [Output("aas-output", "children"),
         Output("submodels-output", "children")],
        [Input("refresh-btn", "n_clicks")]
    )
    def update_view(n_clicks):
        """
        Update the view when the refresh button is clicked.
        Fetches fresh data from the BaSyx server.
        """
        print(f"Fetching data... (Click #{n_clicks})")
        
        # Fetch data from both endpoints
        aas_data = fetch_aas_data()
        submodel_data = fetch_submodel_data()
        
        # Format the data for display
        aas_display = html.Pre(
            str(aas_data),
            style={
                "whiteSpace": "pre-wrap",
                "wordWrap": "break-word",
                "fontSize": "14px",
                "fontFamily": "monospace"
            }
        )
        
        submodel_display = html.Pre(
            str(submodel_data),
            style={
                "whiteSpace": "pre-wrap",
                "wordWrap": "break-word",
                "fontSize": "14px",
                "fontFamily": "monospace"
            }
        )
        
        return aas_display, submodel_display
    
    return app


def main():
    """Start the Dash visualization server."""
    
    print("=" * 60)
    print("Step 3: Starting Visualization Dashboard")
    print("=" * 60)
    print()
    print("⚠️  Important: Make sure the BaSyx server is running!")
    print("   (Run start_server.py in a separate terminal)")
    print()
    print("=" * 60)
    print("Dash Web Application is starting...")
    print("=" * 60)
    print()
    print("Access the dashboard at: http://127.0.0.1:8050")
    print()
    print("Press Ctrl+C to stop the application")
    print("=" * 60)
    print()
    
    # Create and run the app
    app = create_dash_app()
    app.run(debug=True, host="0.0.0.0", port=8050)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Visualization dashboard stopped gracefully")
