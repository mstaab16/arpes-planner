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


app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                /* Mobile-first responsive design */
                @media (max-width: 768px) {
                    /* Make config boxes stack in single column */
                    .config-row {
                        flex-direction: column !important;
                    }
                    
                    .config-row > div {
                        margin-right: 0 !important;
                        margin-bottom: 10px !important;
                        flex: none !important;
                        width: 100% !important;
                    }
                    
                    /* Make plots stack vertically */
                    .plot-container {
                        flex-direction: column !important;
                    }
                    
                    .plot-container > div {
                        margin-right: 0 !important;
                        margin-bottom: 20px !important;
                        flex: none !important;
                        width: 100% !important;
                    }
                    
                    /* Adjust padding for mobile */
                    .main-container {
                        padding: 15px !important;
                    }
                    
                    .config-section {
                        padding: 20px !important;
                    }
                    
                    /* Make title more readable on mobile */
                    .title {
                        font-size: 1.8rem !important;
                        padding: 20px !important;
                    }
                    
                    .subtitle {
                        font-size: 0.9rem !important;
                    }
                    
                    /* Improve plot responsiveness on mobile */
                    .plot-container .js-plotly-plot {
                        width: 100% !important;
                        height: 400px !important;
                    }
                    
                    /* Adjust plot margins for mobile */
                    .plot-container .plotly-graph-div {
                        margin: 0 !important;
                        padding: 0 !important;
                    }
                    
                    /* Make plot titles more compact on mobile */
                    .plot-container .gtitle {
                        font-size: 1rem !important;
                        margin-bottom: 10px !important;
                    }
                    
                    /* Adjust colorbar positioning */
                    .plot-container .colorbar {
                        width: 20px !important;
                        height: 200px !important;
                    }
                }
                
                /* Tablet adjustments */
                @media (min-width: 769px) and (max-width: 1024px) {
                    .config-row {
                        flex-wrap: wrap !important;
                    }
                    
                    .config-row > div {
                        flex: 1 1 calc(50% - 10px) !important;
                        min-width: 250px !important;
                    }
                    
                    .plot-container {
                        flex-direction: column !important;
                    }
                    
                    .plot-container > div {
                        margin-right: 0 !important;
                        margin-bottom: 20px !important;
                    }
                    
                    /* Improve plot responsiveness on tablet */
                    .plot-container .js-plotly-plot {
                        width: 100% !important;
                        height: 500px !important;
                    }
                }
                
                /* Ensure proper spacing and readability */
                @media (max-width: 480px) {
                    .main-container {
                        padding: 10px !important;
                    }
                    
                    .config-section {
                        padding: 15px !important;
                    }
                    
                    .title {
                        font-size: 1.5rem !important;
                        padding: 15px !important;
                    }
                    
                    /* Even more compact plots for small mobile */
                    .plot-container .js-plotly-plot {
                        height: 350px !important;
                    }
                    
                    .plot-container .gtitle {
                        font-size: 0.9rem !important;
                        margin-bottom: 5px !important;
                    }
                }
                
                /* General plot improvements */
                .plot-container .js-plotly-plot {
                    max-width: 100% !important;
                    overflow: hidden !important;
                }
                
                .plot-container .plotly-graph-div {
                    width: 100% !important;
                }
            </style>
            <script>
			!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug getPageViewId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
			posthog.init('phc_2SL8mCI2sJXNV0sVxBogA1iSRmSkLuGq537A4K6Ixu2', {
				api_host: 'https://us.i.posthog.com',
				persistence: 'memory',
				person_profiles: 'always', // or 'always' to create profiles for anonymous users as well
			});
		</script>
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''

# Neobrutalist CSS styles
app.layout = html.Div([
            html.Div([
            html.Div([
                html.H1("Plan your ARPES experiment with style.", style={
                    'margin': '0',
                    'fontSize': 'clamp(1.5rem, 4vw, 2.5rem)',
                    'fontWeight': '800',
                    'textTransform': 'uppercase',
                    'letterSpacing': '-0.02em',
                    'fontFamily': 'Inter, sans-serif'
                }, className='title'),
                html.Div([
                    "A planning tool made by ",
                    html.A(
                        "Matthew Staab",
                        href="https://github.com/mstaab16",
                        target="_blank",
                        style={'color': '#fbbf24', 'textDecoration': 'underline'}
                    ),
                    "."
                ], style={
                    'marginTop': '10px',
                    'fontSize': 'clamp(0.9rem, 2.5vw, 1.1rem)',
                    'opacity': '0.9',
                    'fontFamily': 'Inter, sans-serif'
                }, className='subtitle')
            ], style={
                'background': '#1e40af',
                'color': '#ffffff',
                'padding': 'clamp(20px, 4vw, 30px)',
                'borderBottom': '4px solid #000000',
                'textAlign': 'center'
            }),
        
        # Configuration Section
        html.Div([
            html.H3("Configuration", style={
                'color': '#1e40af',
                'fontSize': 'clamp(1.1rem, 3vw, 1.3rem)',
                'fontWeight': '600',
                'marginBottom': '20px',
                'textTransform': 'uppercase',
                'letterSpacing': '0.05em',
                'fontFamily': 'Inter, sans-serif'
            }),
            
            # Energy Parameters Row
            html.Div([
                html.Div([
                    html.Div([
                        html.Label("Photon Energy (eV)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="Energy of the incident photons used in the ARPES experiment. Determines the kinetic energy of emitted electrons.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Div([
                        html.Label("Inner Potential (eV)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="The inner potential of the sample material. Affects the perpendicular momentum of emitted electrons.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Div([
                        html.Label("Work Function (eV)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="The work function of the sample surface. Energy required to remove an electron from the surface.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                })
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'flexWrap': 'wrap',
                'marginBottom': '20px'
            }, className='config-row'),
            
            # Sample Offset Parameters Row
            html.Div([
                html.Div([
                    html.Div([
                        html.Label("Sample Normal Offset Along Slit (deg)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="Location of normal emission along the slit direction.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
                    dcc.Input(id="offset-along-slit", type="number", value=0, debounce=True, style={
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Div([
                        html.Label("Sample Normal Offset Perpendicular to Slit (deg)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="Location of normal emission perpendicular to the slit direction (Polar angle / Deflector angle).")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
                    dcc.Input(id="offset-perpendicular-slit", type="number", value=0, debounce=True, style={
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                })
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'flexWrap': 'wrap',
                'marginBottom': '20px'
            }, className='config-row'),
            
            # Vector Parameters Row
            html.Div([
                html.Div([
                    html.Div([
                        html.Label("Sample Normal (x,y,z)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="The direction of normal emission from the sample surface. In the crystal coordinate system.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Div([
                        html.Label("Slit Direction (x,y,z)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="If the sample normal emission was aligned with 0 degrees on the analyzer this is the direction of the slit in the crystal coordinate system.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                })
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'flexWrap': 'wrap',
                'marginBottom': '20px'
            }, className='config-row'),
            
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
                    html.Div([
                        html.Label("Start (deg)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.8rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="Starting angle for the slit rotation scan in degrees. Analyzer coordinate system.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Div([
                        html.Label("End (deg)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.8rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="Ending angle for the slit rotation scan in degrees. Analyzer coordinate system.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Div([
                        html.Label("Count", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.8rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="Number of points to calculate along the slit angle scan. Max 200 to avoid bogging down the system.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                })
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'flexWrap': 'wrap',
                'marginBottom': '20px'
            }, className='config-row'),
            
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
                    html.Div([
                        html.Label("Start (deg)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.8rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="Starting angle for the deflector (polar) rotation scan in degrees. Analyzer coordinate system.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Div([
                        html.Label("End (deg)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.8rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="Ending angle for the deflector (polar) rotation scan in degrees. Analyzer coordinate system.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Div([
                        html.Label("Count", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.8rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="Number of points to calculate along the deflector angle scan. Max 200 to avoid bogging down the system.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                })
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'flexWrap': 'wrap',
                'marginBottom': '20px'
            }, className='config-row'),
            
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
                    html.Div([
                        html.Label("b1 (kx,ky,kz) (1/Å)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="First primitive reciprocal lattice vector in units of inverse Angstroms. Defines the crystal structure. In the crystal coordinate system.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Div([
                        html.Label("b2 (kx,ky,kz) (1/Å)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="Second primitive reciprocal lattice vector in units of inverse Angstroms. Defines the crystal structure. In the crystal coordinate system.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                }),
                html.Div([
                    html.Div([
                        html.Label("b3 (kx,ky,kz)", style={
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'color': '#000000',
                            'marginBottom': '8px',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.05em',
                            'fontFamily': 'Inter, sans-serif'
                        }),
                        html.Div("ⓘ", style={
                            'marginLeft': '8px',
                            'marginBottom': '8px',
                            'cursor': 'help',
                            'fontSize': '1.2rem',
                            'color': '#1e40af',
                            'position': 'relative',
                            'display': 'inline-block'
                        }, title="Third primitive reciprocal lattice vector in units of inverse Angstroms. Defines the crystal structure. In the crystal coordinate system.")
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}),
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
                    'marginBottom': '10px',
                    'background': '#ffffff',
                    'border': '2px solid #000000',
                    'padding': '15px',
                    'boxShadow': '3px 3px 0px #000000'
                })
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'flexWrap': 'wrap',
                'marginBottom': '20px'
            })
            
        ], style={
            'background': '#f8fafc',
            'border': '4px solid #000000',
            'padding': 'clamp(20px, 4vw, 30px)',
            'marginBottom': '20px',
            'boxShadow': '4px 4px 0px #000000'
        }, className='config-section'),
        
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
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'flexWrap': 'wrap'
        }, className='plot-container'),
        
        dcc.Download(id="download-csv"),
        dcc.Store(id='calculated-data-store')
        
            ], style={
            'padding': 'clamp(15px, 3vw, 30px)',
            'maxWidth': '1400px',
            'margin': '0 auto'
        }, className='main-container')
    
], style={
    'background': '#ffffff',
    'color': '#000000',
    'margin': '0',
    'padding': '0',
    'fontFamily': 'Inter, sans-serif',
    'minHeight': '100vh'
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
     Output("calculated-data-store", "data")],
    [Input("photon-energy", "value"),
     Input("inner-potential", "value"),
     Input("work-function", "value"),
     Input("offset-along-slit", "value"),
     Input("offset-perpendicular-slit", "value"),
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
                offset_along_slit, offset_perpendicular_slit,
                sample_normal_str, slit_direction_str,
                slit_start, slit_end, slit_count,
                deflector_start, deflector_end, deflector_count,
                b1_str, b2_str, b3_str):
    
    inputs = [photon_energy, inner_potential, work_function, offset_along_slit, offset_perpendicular_slit,
              sample_normal_str, slit_direction_str, slit_start, slit_end, slit_count,
              deflector_start, deflector_end, deflector_count, b1_str, b2_str, b3_str]
    if any(i is None for i in inputs):
        raise PreventUpdate

    if slit_count > COUNT_LIMIT or deflector_count > COUNT_LIMIT:
        return go.Figure(), go.Figure(), {}

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
    sample_normal_offsets_along_slit = np.full(n_points, offset_along_slit)
    sample_normal_offsets_perpendicular_to_slit = np.full(n_points, offset_perpendicular_slit)

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
        return go.Figure(), go.Figure(), {}

    reciprocal_lattice = np.array([b1, b2, b3])
    sample_normals = np.tile(sample_normal, (n_points, 1))
    slit_directions = np.tile(slit_direction, (n_points, 1))

    try:
        # Call the function
        final_momentum_coords, projected_coords, _ = absolute_and_projected_momentum_coords(
            photon_energies, slit_values, deflector_values, inner_potentials, work_functions,
            sample_normal_offsets_along_slit, sample_normal_offsets_perpendicular_to_slit,
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
                size=4,
                color=slit_values,
                colorscale='Viridis',
                colorbar_title='Slit Angle (deg)',
                opacity=0.8
            )
        )])
        
        absolute_fig.update_layout(
            title=dict(
                text="Absolute Momentum Coordinates",
                font=dict(size=16),
                x=0.5,
                xanchor='center'
            ),
            scene=dict(
                xaxis_title="k_x (Å⁻¹)",
                yaxis_title="k_y (Å⁻¹)",
                zaxis_title="k_z (Å⁻¹)",
                aspectmode='data',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            margin=dict(l=0, r=0, b=0, t=50),
            height=500,
            autosize=True
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
                size=4,
                color=slit_values,
                colorscale='Viridis',
                colorbar_title='Slit Angle (deg)',
                opacity=0.8
            ),
            showlegend=False
        )])
        
        projected_fig.update_layout(
            title=dict(
                text="Momentum coordinates in the first Brillouin zone",
                font=dict(size=16),
                x=0.5,
                xanchor='center'
            ),
            scene=dict(
                xaxis_title="k_x_rel (Å⁻¹)",
                yaxis_title="k_y_rel (Å⁻¹)",
                zaxis_title="k_z_rel (Å⁻¹)",
                aspectmode='data',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            margin=dict(l=0, r=0, b=0, t=50),
            height=500,
            autosize=True
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
                line=dict(color='black', width=1),
                showlegend=False,
            ))



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

        return absolute_fig, projected_fig, data_to_store
        
    except Exception as e:
        return go.Figure(), go.Figure(), {}

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
    sample_normal_offset_along_slit, # (n,)
    sample_normal_offset_perpendicular_to_slit, # (n,)
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
        offset_slit = sample_normal_offset_along_slit[i]
        offset_deflector = sample_normal_offset_perpendicular_to_slit[i]

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
    import os
    port = int(os.environ.get('PORT', 8050))
    host = os.environ.get('HOST', 'localhost')
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.title = "ARPES Planner"
    app.description = "A planning tool made by <a href='https://github.com/mstaab16'>Matthew Staab</a>."
    app.run(debug=debug, host=host, port=port)
