from dash import Dash, html, dcc, callback, Output, Input, State
import numpy as np
from scipy.spatial import Voronoi
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import pandas as pd

ELECTRON_SCHRODINGER_CONSTANT = 0.262468423640825284
COUNT_LIMIT = 200
ZONE_COEFFICENTS = (np.indices((3, 3, 3)) - 1).reshape((3, 27))

# Custom CSS styles
external_stylesheets = [{
    'href': 'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap',
    'rel': 'stylesheet'
}]

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Neobrutalist CSS styles
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1("ARPES Momentum Calculator", style={
                'margin': '0',
                'fontSize': '2.5rem',
                'fontWeight': '800',
                'textTransform': 'uppercase',
                'letterSpacing': '-0.02em',
                'fontFamily': 'Inter, sans-serif'
            }),
            html.Div("Advanced Photoelectron Spectroscopy Momentum Coordinate Analysis", style={
                'marginTop': '10px',
                'fontSize': '1.1rem',
                'opacity': '0.9',
                'fontFamily': 'Inter, sans-serif'
            })
        ], style={
            'background': '#1e40af',
            'color': '#ffffff',
            'padding': '30px',
            'borderBottom': '4px solid #000000',
            'textAlign': 'center'
        }),
        
        # Configuration Section
        html.Div([
            html.H3("Configuration", style={
                'color': '#1e40af',
                'fontSize': '1.3rem',
                'fontWeight': '600',
                'marginBottom': '20px',
                'textTransform': 'uppercase',
                'letterSpacing': '0.05em',
                'fontFamily': 'Inter, sans-serif'
            }),
            
            # Energy Parameters Row
            html.Div([
                html.Div([
                    html.Label("Photon Energy (eV)", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.9rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="photon-energy", type="number", value=21.2, debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'marginRight': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Label("Inner Potential (eV)", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.9rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="inner-potential", type="number", value=13, debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'marginRight': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Label("Work Function (eV)", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.9rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="work-function", type="number", value=4.5, debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                })
            ], style={
                'display': 'flex',
                'marginBottom': '20px'
            }),
            
            # Sample Offset Parameters Row
            html.Div([
                html.Div([
                    html.Label("Sample Normal Offset Along Slits (deg)", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.9rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="offset-along-slits", type="number", value=0, debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'marginRight': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Label("Sample Normal Offset Perpendicular to Slits (deg)", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.9rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="offset-perpendicular-slits", type="number", value=0, debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                })
            ], style={
                'display': 'flex',
                'marginBottom': '20px'
            }),
            
            # Vector Parameters Row
            html.Div([
                html.Div([
                    html.Label("Sample Normal (x,y,z)", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.9rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="sample-normal", type="text", value="0,0,1", debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'marginRight': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Label("Slit Direction (x,y,z)", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.9rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="slit-direction", type="text", value="1,0,0", debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                })
            ], style={
                'display': 'flex',
                'marginBottom': '20px'
            }),
            
            html.H4("Slit Angles", style={
                'color': '#000000',
                'fontSize': '1.1rem',
                'fontWeight': '600',
                'margin': '25px 0 15px 0',
                'textTransform': 'uppercase',
                'letterSpacing': '0.05em',
                'fontFamily': 'Inter, sans-serif'
            }),
            html.Div([
                html.Div([
                    html.Label("Start", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.8rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="slit-angle-start", type="number", value=-15, debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'marginRight': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Label("End", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.8rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="slit-angle-end", type="number", value=15, debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'marginRight': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Label("Count", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.8rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="slit-angle-count", type="number", value=31, min=1, max=COUNT_LIMIT, step=1, debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                })
            ], style={
                'display': 'flex',
                'marginBottom': '20px'
            }),
            
            html.H4("Deflector (Polar) Angles", style={
                'color': '#000000',
                'fontSize': '1.1rem',
                'fontWeight': '600',
                'margin': '25px 0 15px 0',
                'textTransform': 'uppercase',
                'letterSpacing': '0.05em',
                'fontFamily': 'Inter, sans-serif'
            }),
            html.Div([
                html.Div([
                    html.Label("Start", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.8rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="deflector-angle-start", type="number", value=-15, debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'marginRight': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Label("End", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.8rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="deflector-angle-end", type="number", value=15, debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'marginRight': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Label("Count", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.8rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="deflector-angle-count", type="number", value=31, min=1, max=COUNT_LIMIT, step=1, debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                })
            ], style={
                'display': 'flex',
                'marginBottom': '20px'
            }),
            
            html.H4("Primitive Reciprocal Lattice Vectors", style={
                'color': '#000000',
                'fontSize': '1.1rem',
                'fontWeight': '600',
                'margin': '25px 0 15px 0',
                'textTransform': 'uppercase',
                'letterSpacing': '0.05em',
                'fontFamily': 'Inter, sans-serif'
            }),
            html.Div([
                html.Div([
                    html.Label("b1 (kx,ky,kz)", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.9rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="b1-vec", type="text", value="1,0,0", debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'marginRight': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Label("b2 (kx,ky,kz)", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.9rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="b2-vec", type="text", value="0,1,0", debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'marginRight': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Label("b3 (kx,ky,kz)", style={
                        'display': 'block',
                        'fontWeight': '600',
                        'color': '#000000',
                        'marginBottom': '8px',
                        'fontSize': '0.9rem',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'fontFamily': 'Inter, sans-serif'
                    }),
                    dcc.Input(id="b3-vec", type="text", value="0,0,1", debounce=True, style={
                        'width': '100%',
                        'padding': '12px',
                        'border': '2px solid #000000',
                        'background': '#ffffff',
                        'fontSize': '1rem',
                        'fontWeight': '500',
                        'boxSizing': 'border-box',
                        'fontFamily': 'Inter, sans-serif'
                    })
                ], style={
                    'flex': '1',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                })
            ], style={
                'display': 'flex',
                'marginBottom': '20px'
            })
            
        ], style={
            'background': '#f8fafc',
            'border': '4px solid #000000',
            'padding': '30px',
            'marginBottom': '20px',
            'boxShadow': '4px 4px 0px #000000'
        }),
        
        # Download Button Section
        html.Div([
            html.Button("Download CSV", id="download-btn", style={
                'background': '#fbbf24',
                'color': '#000000',
                'border': '3px solid #000000',
                'padding': '15px 30px',
                'fontSize': '1rem',
                'fontWeight': '600',
                'textTransform': 'uppercase',
                'letterSpacing': '0.05em',
                'cursor': 'pointer',
                'boxShadow': '4px 4px 0px #000000',
                'fontFamily': 'Inter, sans-serif'
            })
        ], style={
            'textAlign': 'center',
            'marginBottom': '20px'
        }),
        
        # Plot Section
        html.Div([
            # Absolute Coordinates Plot
            html.Div([
                dcc.Graph(id="absolute-plot")
            ], style={
                'background': '#f8fafc',
                'border': '3px solid #000000',
                'padding': '20px',
                'marginBottom': '20px',
                'boxShadow': '4px 4px 0px #000000',
                'flex': '1',
                'marginRight': '10px'
            }),
            
            # Projected Coordinates Plot
            html.Div([
                dcc.Graph(id="projected-plot")
            ], style={
                'background': '#f8fafc',
                'border': '3px solid #000000',
                'padding': '20px',
                'marginBottom': '20px',
                'boxShadow': '4px 4px 0px #000000',
                'flex': '1'
            })
        ], style={'display': 'flex'}),
        
        # Results Section
        html.Div([
            html.Div(id="results-info")
        ], style={
            'background': '#1e40af',
            'color': '#ffffff',
            'border': '3px solid #000000',
            'padding': '20px',
            'marginBottom': '20px',
            'boxShadow': '4px 4px 0px #000000'
        }),
        
        dcc.Download(id="download-csv"),
        dcc.Store(id='calculated-data-store')
        
    ], style={
        'padding': '30px'
    })
    
], style={
    'background': '#ffffff',
    'color': '#000000',
    'margin': '0',
    'padding': '20px',
    'fontFamily': 'Inter, sans-serif'
})

def parse_text_input(input_str, is_matrix=False):
    """Parse comma-separated values from text input"""
    if not input_str or input_str.strip() == "":
        return None
    try:
        if is_matrix:
            rows = input_str.strip().split(";")
            data = [[float(x.strip()) for x in row.split(",")] for row in rows]
            return np.array(data)
        else:
            return np.array([float(x.strip()) for x in input_str.split(",")])
    except:
        return None

@callback(
    [Output("absolute-plot", "figure"),
     Output("projected-plot", "figure"),
     Output("results-info", "children"),
     Output("calculated-data-store", "data")],
    [Input("photon-energy", "value"),
     Input("inner-potential", "value"),
     Input("work-function", "value"),
     Input("offset-along-slits", "value"),
     Input("offset-perpendicular-slits", "value"),
     Input("sample-normal", "value"),
     Input("slit-direction", "value"),
     Input("slit-angle-start", "value"),
     Input("slit-angle-end", "value"),
     Input("slit-angle-count", "value"),
     Input("deflector-angle-start", "value"),
     Input("deflector-angle-end", "value"),
     Input("deflector-angle-count", "value"),
     Input("b1-vec", "value"),
     Input("b2-vec", "value"),
     Input("b3-vec", "value")]
)
def update_plot(photon_energy, inner_potential, work_function,
                offset_along_slits, offset_perpendicular_slits,
                sample_normal_str, slit_direction_str,
                slit_start, slit_end, slit_count,
                deflector_start, deflector_end, deflector_count,
                b1_str, b2_str, b3_str):
    
    inputs = [photon_energy, inner_potential, work_function, offset_along_slits, offset_perpendicular_slits,
              sample_normal_str, slit_direction_str, slit_start, slit_end, slit_count,
              deflector_start, deflector_end, deflector_count, b1_str, b2_str, b3_str]
    if any(i is None for i in inputs):
        raise PreventUpdate

    if slit_count > COUNT_LIMIT or deflector_count > COUNT_LIMIT:
        return go.Figure(), go.Figure(), html.Div(f"Error: Slit and deflector counts cannot be greater than {COUNT_LIMIT}."), {}

    # Create angle grids
    slit_angles = np.linspace(slit_start, slit_end, slit_count)
    deflector_angles = np.linspace(deflector_start, deflector_end, deflector_count)
    slit_values_grid, deflector_values_grid = np.meshgrid(slit_angles, deflector_angles)
    
    slit_values = slit_values_grid.flatten()
    deflector_values = deflector_values_grid.flatten()
    n_points = len(slit_values)

    # Parse single inputs and expand them for all points
    photon_energies = np.full(n_points, photon_energy)
    inner_potentials = np.full(n_points, inner_potential)
    work_functions = np.full(n_points, work_function)
    sample_normal_offsets_along_slits = np.full(n_points, offset_along_slits)
    sample_normal_offsets_perpendicular_to_slits = np.full(n_points, offset_perpendicular_slits)

    sample_normal = parse_text_input(sample_normal_str)
    sample_normal = np.array([sample_normal])
    sample_normal /= np.linalg.norm(sample_normal)
    slit_direction = parse_text_input(slit_direction_str)
    slit_direction = np.array([slit_direction])
    slit_direction /= np.linalg.norm(slit_direction)
    
    b1 = parse_text_input(b1_str)
    b2 = parse_text_input(b2_str)
    b3 = parse_text_input(b3_str)

    if sample_normal is None or slit_direction is None or b1 is None or b2 is None or b3 is None:
        return go.Figure(), go.Figure(), html.Div("Error: Invalid vector or matrix input."), {}

    reciprocal_lattice = np.array([b1, b2, b3])
    sample_normals = np.tile(sample_normal, (n_points, 1))
    slit_directions = np.tile(slit_direction, (n_points, 1))

    try:
        # Call the function
        final_momentum_coords, projected_coords, _ = absolute_and_projected_momentum_coords(
            photon_energies, slit_values, deflector_values, inner_potentials, work_functions,
            sample_normal_offsets_along_slits, sample_normal_offsets_perpendicular_to_slits,
            sample_normals, slit_directions, reciprocal_lattice
        )
        
        # Create 3D scatter plot for absolute coordinates
        hover_data = np.stack((slit_values, deflector_values), axis=-1)
        absolute_fig = go.Figure(data=[go.Scatter3d(
            x=final_momentum_coords[:, 0],
            y=final_momentum_coords[:, 1],
            z=final_momentum_coords[:, 2],
            customdata=hover_data,
            hovertemplate=(
                "<b>kx:</b> %{x:.3f} Å⁻¹<br>"
                "<b>ky:</b> %{y:.3f} Å⁻¹<br>"
                "<b>kz:</b> %{z:.3f} Å⁻¹<br>"
                "<b>Slit Angle:</b> %{customdata[0]:.2f}°<br>"
                "<b>Deflector Angle:</b> %{customdata[1]:.2f}°"
                "<extra></extra>"
            ),
            mode='markers',
            marker=dict(
                size=5,
                color=slit_values,
                colorscale='Viridis',
                colorbar_title='Slit Angle (deg)'
            )
        )])
        
        absolute_fig.update_layout(
            title="Absolute Momentum Coordinates",
            scene=dict(
                xaxis_title="k_x (Å⁻¹)",
                yaxis_title="k_y (Å⁻¹)",
                zaxis_title="k_z (Å⁻¹)",
                aspectmode='data'
            ),
            margin=dict(l=0, r=0, b=0, t=40)
        )
        
        # Create 3D scatter plot for projected coordinates
        projected_fig = go.Figure(data=[go.Scatter3d(
            x=projected_coords[:, 0],
            y=projected_coords[:, 1],
            z=projected_coords[:, 2],
            customdata=hover_data,
            hovertemplate=(
                "<b>kx_rel:</b> %{x:.3f} Å⁻¹<br>"
                "<b>ky_rel:</b> %{y:.3f} Å⁻¹<br>"
                "<b>kz_rel:</b> %{z:.3f} Å⁻¹<br>"
                "<b>Slit Angle:</b> %{customdata[0]:.2f}°<br>"
                "<b>Deflector Angle:</b> %{customdata[1]:.2f}°"
                "<extra></extra>"
            ),
            mode='markers',
            marker=dict(
                size=5,
                color=slit_values,
                colorscale='Viridis',
                colorbar_title='Slit Angle (deg)'
            )
        )])
        
        projected_fig.update_layout(
            title="Projected Momentum Coordinates",
            scene=dict(
                xaxis_title="k_x_rel (Å⁻¹)",
                yaxis_title="k_y_rel (Å⁻¹)",
                zaxis_title="k_z_rel (Å⁻¹)",
                aspectmode='data'
            ),
            margin=dict(l=0, r=0, b=0, t=40)
        )


        voronoi_points = np.dot(ZONE_COEFFICENTS.T, reciprocal_lattice)
        voronoi = Voronoi(voronoi_points)
        for ridge_points, ridge in zip(voronoi.ridge_points, voronoi.ridge_vertices):
            if -1 in ridge or len(ridge) < 2:
                continue
            # 13 is the (0,0,0) BZ center
            if 13 not in ridge_points:
                continue
            ridge_starts = voronoi.vertices[list(ridge) + [ridge[0]]]

            projected_fig.add_trace(go.Scatter3d(
                x=ridge_starts[:, 0],
                y=ridge_starts[:, 1],
                z=ridge_starts[:, 2],
                mode='lines',
                marker=dict(color='black', size=1),
                showlegend=False,
            ))



        # Create results info
        results_info = html.Div([
            html.H4("Results Summary"),
            html.P(f"Number of points: {n_points}"),
            html.P(f"k_x range: [{final_momentum_coords[:, 0].min():.3f}, {final_momentum_coords[:, 0].max():.3f}] Å⁻¹"),
            html.P(f"k_y range: [{final_momentum_coords[:, 1].min():.3f}, {final_momentum_coords[:, 1].max():.3f}] Å⁻¹"),
            html.P(f"k_z range: [{final_momentum_coords[:, 2].min():.3f}, {final_momentum_coords[:, 2].max():.3f}] Å⁻¹"),
        ])
        
        data_to_store = {
            'slit_angle': slit_values.tolist(),
            'deflector_angle': deflector_values.tolist(),
            'kx': final_momentum_coords[:, 0].tolist(),
            'ky': final_momentum_coords[:, 1].tolist(),
            'kz': final_momentum_coords[:, 2].tolist(),
            'kx_rel': projected_coords[:, 0].tolist(),
            'ky_rel': projected_coords[:, 1].tolist(),
            'kz_rel': projected_coords[:, 2].tolist(),
        }

        return absolute_fig, projected_fig, results_info, data_to_store
        
    except Exception as e:
        return go.Figure(), go.Figure(), html.Div(f"Error in calculation: {str(e)}"), {}

@callback(
    Output("download-csv", "data"),
    Input("download-btn", "n_clicks"),
    State("calculated-data-store", "data"),
    prevent_initial_call=True,
)
def download_csv(n_clicks, data):
    if not data:
        raise PreventUpdate
    df = pd.DataFrame(data)
    return dcc.send_data_frame(df.to_csv, "arpes_data.csv", index=False)

def absolute_and_projected_momentum_coords(
    photon_energies, # (n, )
    slit_values, # (n,)
    deflector_values, # (n,)
    inner_potentials, # (n,)
    work_functions, # (n,)
    sample_normal_offset_along_slits, # (n,)
    sample_normal_offset_perpendicular_to_slits, # (n,)
    sample_normals, # (n, 3)
    slit_directions, # (n, 3)
    reciprocal_lattice, # (3, 3)
):
    N = photon_energies.shape[0]
    final_momentum_coords = np.zeros((N, 3))
    projected_coords = np.zeros((N, 3))
    rounded_coords = np.zeros((N, 3))
    rad_per_deg = np.pi / 180.0

    B_inv = np.linalg.inv(reciprocal_lattice)


    for i in range(N):
        hv = photon_energies[i]
        slit_dir = slit_directions[i]
        normal = sample_normals[i]
        slit_angle = slit_values[i]
        deflector_angle = deflector_values[i]
        V0 = inner_potentials[i]
        phi = work_functions[i]
        offset_slit = sample_normal_offset_along_slits[i]
        offset_deflector = sample_normal_offset_perpendicular_to_slits[i]

        undeflected_slit_rotation_axis = np.cross(normal, slit_dir)
        basis = np.empty((3, 3))
        basis[0] = slit_dir
        basis[1] = undeflected_slit_rotation_axis
        basis[2] = normal

        slit_angle = rad_per_deg * (slit_angle - offset_slit)
        deflector_angle = rad_per_deg * (deflector_angle - offset_deflector)

        cos_slit = np.cos(slit_angle)
        sin_slit = np.sin(slit_angle)
        cos_deflector = np.cos(deflector_angle)
        sin_deflector = np.sin(deflector_angle)

        cos_slit_squared = cos_slit**2
        sin_defl_squared = sin_deflector**2
        sin_slit_squared = sin_slit**2

        cos_theta = cos_deflector * cos_slit
        cos_theta_squared = cos_theta**2
        sin_theta = np.sqrt(1 - cos_theta_squared)
        denom = np.sqrt(sin_slit_squared + sin_defl_squared * cos_slit_squared)
        denom = np.where(denom == 0, 1e-10, denom)
        cos_phi = sin_slit / denom
        sin_phi =  - sin_deflector * cos_slit / denom

        k_slit = np.sqrt(ELECTRON_SCHRODINGER_CONSTANT * (hv - phi)) * sin_theta * cos_phi
        k_deflector = np.sqrt(ELECTRON_SCHRODINGER_CONSTANT * (hv - phi)) * sin_theta * sin_phi
        k_normal = np.sqrt(ELECTRON_SCHRODINGER_CONSTANT * ((hv - phi) * cos_theta_squared + V0))

        k_vec_weird_basis = np.array([k_slit, k_deflector, k_normal])
        k = np.dot(k_vec_weird_basis, basis)

        final_momentum_coords[i] = k
        coords = np.dot(k, B_inv)
        rounded_coord = np.round(coords)
        rounded_coords[i] = rounded_coord
        relative_vec = k - np.dot(rounded_coord, reciprocal_lattice)
        # subtract nearest BZ center
        adjacent_bz_centers = np.dot(ZONE_COEFFICENTS.T, reciprocal_lattice)
        distances = np.sum((relative_vec - adjacent_bz_centers)**2, axis=1)
        nearest_bz_center = adjacent_bz_centers[np.argmin(distances)]
        relative_vec -= nearest_bz_center

        projected_coords[i] = relative_vec

    return final_momentum_coords, projected_coords, rounded_coords

if __name__ == '__main__':
    app.run(debug=True)
