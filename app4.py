import dash
from dash import dcc, html, Input, Output, dash_table, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# Transaction data (monthly_data)
monthly_data = pd.DataFrame({
    'Month': [
        'Sep\'23', 'Oct\'23', 'Nov\'23', 'Dec\'23', 'Jan\'24', 'Feb\'24',
        'Mar\'24', 'Apr\'24', 'May\'24', 'Jun\'24', 'Jul\'24', 'Aug\'24',
        'Sep\'24', 'Oct\'24', 'Nov\'24', 'Dec\'24'
    ],
    'LEMFI': [0.0, 0.0, 0.0, 1010000.0, 8500000.0, 4750000.0, 10100000.0, 
              7150000.0, 6250000.0, 7500000.0, 6250000.0, 10149900.0, 
              6950000.0, 18750000.0, 14950000.0, 10950000.0],
    'LEMFI_count': [0, 0, 0, 4, 20, 13, 17, 12, 13, 17, 15, 16, 10, 18, 16, 12],
    'NALA': [0.0, 0.0, 0.0, 4180000.0, 1995000.0, 500000.0, 2568000.0, 
             1800000.0, 1300000.0, 400000.0, 0.0, 1995000.0, 100000.0, 
             3460000.0, 710000.0, 0.0],
    'NALA_count': [0, 0, 0, 13, 5, 2, 5, 6, 4, 2, 0, 6, 1, 10, 3, 0],
    'Cellulant': [544000.0, 2300000.0, 8985000.0, 2950000.0, 200000.0, 
                  300000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'Cellulant_count': [2, 7, 21, 6, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'DLocal/TTS': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   0.0, 1000000.0, 1150000.0, 470000.0, 0.0],
    'DLocal_TTS_count': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 4, 0]
})

# Bank distribution data
bank_distribution = {
    'LEMFI': {
        'KCB': 46.1, 
        'DTB': 18.3, 
        'NCBA': 12.6, 
        'Prime': 6.7, 
        'SBM': 1.3, 
        'Others': 15.0
    },
    'NALA': {
        'DTB': 52.2,
        'KCB': 17.2,
        'NCBA': 1.0,
        'Prime': 3.4,
        'SBM': 3.1,
        'Others': 23.1
    },
    'Cellulant': {
        'Standard Investment Bank': 42.0,
        'Others': 58.0
    },
    'DLocal/TTS': {
        'KCB': 59.0,
        'DTB': 3.1,
        'Prime': 37.9
    }
}

# Dictionary for bank logo paths
bank_logos = {
    'KCB': '/assets/bank-logos/KCB.png',
    'DTB': '/assets/bank-logos/DTB.png',
    'NCBA': '/assets/bank-logos/NCBA.png',
    'Prime': '/assets/bank-logos/Prime.jpg',
    'SBM': '/assets/bank-logos/SBM.png',
    'Standard Investment Bank': '/assets/bank-logos/SIB.png',
    'Others': '/assets/bank-logos/Others.png'
}

# Updated bank color scheme
bank_colors = {
    'KCB': '#008000',      # Green
    'DTB': '#FF0000',      # Red
    'NCBA': '#000000',     # Black
    'Prime': '#00008B',    # Dark Blue
    'SBM': '#87CEEB',      # Light Blue
    'Others': '#FFD700',   # Yellow
    'Standard Investment Bank': '#00008B'  # Dark Blue
}

# Initialize the app with custom styling
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.FLATLY,
        'https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap'
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)

# This is important for Render deployment
server = app.server

# Enhanced Custom CSS with updated dark mode support
app.index_string = '''<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Partner Report</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                --background-light: #ffffff;
                --card-bg-light: #ffffff;
                --text-light: #2c3e50;
                --border-light: #dee2e6;
                
                --background-dark: #121212;
                --card-bg-dark: #1e1e1e;
                --text-dark: #ffffff;
                --border-dark: #404040;
            }

            * {
                font-family: 'Bebas Neue', sans-serif;
                transition: background-color 0.3s ease, color 0.3s ease;
            }
            
            body {
                background-color: var(--background-light);
                color: var(--text-light);
            }

            .title-text {
                color: #2c3e50;
                transition: color 0.3s ease;
            }
            
            .regular-text {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            
            .card {
                margin-bottom: 1rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                background-color: var(--card-bg-light);
                border: 1px solid var(--border-light);
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            }
            
            .partner-logo {
                width: 100px;
                height: 100px;
                object-fit: contain;
                margin: 10px;
            }

            .partner-logo-title {
                max-width: 150px;
                height: 100px;
                object-fit: contain;
                margin: auto;
                display: block;
            }
            
            .market-share-card {
                background: linear-gradient(135deg, #f6f9fc 0%, #f1f4f8 100%);
            }
            
            .logo {
                transition: all 0.3s ease;
                display: none;
            }

            .logo.light {
                display: block;
            }

            .logo.dark {
                display: none;
            }

            /* Chart Styles */
            .js-plotly-plot {
                width: 100% !important;
            }

            .js-plotly-plot .plotly {
                width: 100% !important;
            }

            /* Dark Mode */
            @media (prefers-color-scheme: dark) {
                body {
                    background-color: var(--background-dark);
                    color: var(--text-dark);
                }

                .title-text {
                    color: #ffffff !important;
                }
                
                .card {
                    background-color: var(--card-bg-dark);
                    border-color: var(--border-dark);
                    color: var(--text-dark);
                }
                
                .market-share-card {
                    background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
                }

                .logo.light {
                    display: none;
                }

                .logo.dark {
                    display: block;
                }

                .btn-light {
                    background-color: #2d2d2d;
                    border-color: var(--border-dark);
                    color: var(--text-dark);
                }

                .btn-light:hover {
                    background-color: #3d3d3d;
                    border-color: #505050;
                }

                /* Dark mode chart improvements */
                .js-plotly-plot .plotly .main-svg {
                    background-color: var(--card-bg-dark) !important;
                }

                .js-plotly-plot .plotly .gridlayer path {
                    stroke: #404040 !important;
                }

                .js-plotly-plot .plotly .ticktext,
                .js-plotly-plot .plotly .legendtext,
                .js-plotly-plot .plotly .gtitle {
                    fill: var(--text-dark) !important;
                }

                /* Plot background */
                .js-plotly-plot .plot-container .plot-background {
                    fill: var(--card-bg-dark) !important;
                }

                /* Axis lines */
                .js-plotly-plot .plotly path.xgrid,
                .js-plotly-plot .plotly path.ygrid {
                    stroke: #404040 !important;
                }
            }

            /* Responsive Styles */
            @media (max-width: 768px) {
                .partner-logo {
                    width: 60px;
                    height: 60px;
                    margin: 5px;
                }
                
                .card {
                    margin-bottom: 0.5rem;
                }
                
                h1 { font-size: 1.8rem !important; }
                h2 { font-size: 1.6rem !important; }
                h3 { font-size: 1.4rem !important; }
                h4 { font-size: 1.2rem !important; }
                h5 { font-size: 1rem !important; }
                
                .partner-logo-title {
                    max-width: 120px;
                    height: 80px;
                }
            }

            @media (max-width: 576px) {
                .partner-logo {
                    width: 50px;
                    height: 50px;
                }
                
                .partner-logo-title {
                    max-width: 100px;
                    height: 60px;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>'''

# App layout with enhanced responsive features
app.layout = dbc.Container([
    # Enhanced Header with responsive logo and title
    dbc.Row([
        dbc.Col([
            html.Div([
                # Light mode logo
                html.Img(
                    src='/assets/vngrd.PNG',
                    className='logo light',
                    style={
                        'height': '150px',
                        'max-width': '100%',
                        'object-fit': 'contain'
                    }
                ),
                # Dark mode logo
                html.Img(
                    src='/assets/vngrd-dark.PNG',
                    className='logo dark',
                    style={
                        'height': '150px',
                        'max-width': '100%',
                        'object-fit': 'contain'
                    }
                )
            ], style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '40px',
                'marginBottom': '30px',
                'width': '100%'
            }, className="mobile-padding"),
            html.H1(
                "Partner Report",
                className="title-text text-center mb-4",
                style={'letterSpacing': '2px'}
            )
        ])
    ]),

    # Partner selection row with responsive cards
    dbc.Row([
        # LEMFI Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Img(
                            src='/assets/partner-logos/LEMFI.png',
                            className='partner-logo mb-3'
                        )
                    ], className="text-center"),
                    dbc.Button(
                        "Select LEMFI",
                        id="LEMFI-logo",
                        color="light",
                        className="w-100",
                        n_clicks=0
                    )
                ], className="mobile-padding")
            ], className="market-share-card h-100")
        ], xs=12, sm=6, md=3, className="mb-3"),

        # NALA Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Img(
                            src='/assets/partner-logos/Nala.png',
                            className='partner-logo mb-3'
                        )
                    ], className="text-center"),
                    dbc.Button(
                        "Select NALA",
                        id="NALA-logo",
                        color="light",
                        className="w-100",
                        n_clicks=0
                    )
                ], className="mobile-padding")
            ], className="market-share-card h-100")
        ], xs=12, sm=6, md=3, className="mb-3"),

        # Cellulant Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Img(
                            src='/assets/partner-logos/Cellulant.png',
                            className='partner-logo mb-3'
                        )
                    ], className="text-center"),
                    dbc.Button(
                        "Select Cellulant",
                        id="Cellulant-logo",
                        color="light",
                        className="w-100",
                        n_clicks=0
                    )
                ], className="mobile-padding")
            ], className="market-share-card h-100")
        ], xs=12, sm=6, md=3, className="mb-3"),

        # DLocal Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Img(
                            src='/assets/partner-logos/DLocal.png',
                            className='partner-logo mb-3'
                        )
                    ], className="text-center"),
                    dbc.Button(
                        "Select DLocal",
                        id="DLocal-logo",
                        color="light",
                        className="w-100",
                        n_clicks=0
                    )
                ], className="mobile-padding")
            ], className="market-share-card h-100")
        ], xs=12, sm=6, md=3, className="mb-3"),
    ], className="mb-4 g-2"),

    # Title card for selected partner
    dbc.Row([
        dbc.Col([
            html.Div(
                id="selected-partner-title",
                children=[],
                className="mb-4"
            )
        ], width=12)
    ]),

    # Content section
    dbc.Row([
        dbc.Col([
            html.Div(
                id="partner-details",
                children=[],
                className="mobile-padding"
            )
        ], width=12)
    ])
], fluid=True, className="px-2 px-md-4")

@app.callback(
    [Output("partner-details", "children"),
     Output("selected-partner-title", "children")],
    [Input("LEMFI-logo", "n_clicks"),
     Input("NALA-logo", "n_clicks"),
     Input("Cellulant-logo", "n_clicks"),
     Input("DLocal-logo", "n_clicks")]
)
def display_partner_details(lemfi_clicks, nala_clicks, cellulant_clicks, dlocal_clicks):
    if not ctx.triggered:
        return [], []

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    partner = triggered_id.replace("-logo", "")
    
    if partner == "DLocal":
        data_column = "DLocal/TTS"
        count_column = "DLocal_TTS_count"
    else:
        data_column = partner
        count_column = f"{partner}_count"

    # Create simplified title card with centered logo only
    title_card = dbc.Card([
        dbc.CardBody([
            html.Img(
                src=f'/assets/partner-logos/{partner}.png',
                className="partner-logo-title"
            ),
        ], className="d-flex justify-content-center align-items-center")
    ], className="shadow-sm title-card")

    # Extract partner-specific data
    partner_data = monthly_data[["Month", data_column, count_column]].copy()
    partner_data.columns = ["Month", "Volume", "Count"]
    partner_data = partner_data[partner_data['Volume'] > 0]

    # Calculate statistics
    total_volume = partner_data['Volume'].sum()
    total_count = partner_data['Count'].sum()
    avg_transaction = total_volume / total_count if total_count > 0 else 0

    # Create charts with updated dark mode compatibility
    combined_chart = go.Figure()
    combined_chart.add_trace(go.Scatter(
        x=partner_data['Month'],
        y=partner_data['Volume'],
        name='Volume (USD)',
        yaxis='y1',
        line=dict(color='#2E86C1', width=3)
    ))
    
    combined_chart.add_trace(go.Bar(
        x=partner_data['Month'],
        y=partner_data['Count'],
        name='Transaction Count',
        yaxis='y2',
        marker_color='rgba(231, 76, 60, 0.7)'
    ))
    
    combined_chart.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title={
            'text': f"{partner} Transaction Analysis",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, family='Bebas Neue')
        },
        yaxis=dict(
            title="Volume (USD)",
            titlefont=dict(color="#2E86C1"),
            tickfont=dict(color="#2E86C1"),
            gridcolor='rgba(189, 195, 199, 0.2)',
            tickformat="$,.0f",
            showgrid=True
        ),
        yaxis2=dict(
            title="Transaction Count",
            titlefont=dict(color="#E74C3C"),
            tickfont=dict(color="#E74C3C"),
            overlaying="y",
            side="right",
            gridcolor='rgba(189, 195, 199, 0.2)',
            showgrid=False
        ),
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(t=80, b=30, l=40, r=40)
    )

    # Create rolling average chart with dark mode compatibility
    rolling_chart = go.Figure()
    rolling_chart.add_trace(go.Scatter(
        x=partner_data['Month'],
        y=partner_data['Volume'],
        name='Actual Volume',
        line=dict(color='#2E86C1', width=2)
    ))
    
    rolling_avg = partner_data['Volume'].rolling(window=3, min_periods=1).mean()
    rolling_chart.add_trace(go.Scatter(
        x=partner_data['Month'],
        y=rolling_avg,
        name='3-Month Rolling Average',
        line=dict(color='#E74C3C', width=3, dash='dot')
    ))
    
    rolling_chart.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title={
            'text': "Volume Trend Analysis",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, family='Bebas Neue')
        },
        yaxis=dict(
            title="Volume (USD)",
            titlefont=dict(color="#2E86C1"),
            tickfont=dict(color="#2E86C1"),
            gridcolor='rgba(189, 195, 199, 0.2)',
            tickformat="$,.0f",
            showgrid=True
        ),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(t=80, b=30, l=40, r=40)
    )

# Create bank distribution with improved dark mode visibility
    bank_dist = bank_distribution[data_column]
    max_share = max(bank_dist.values())
    
    bank_images = html.Div([
        html.Div([
            html.Img(src=bank_logos[bank], 
                    className='partner-logo'),
            html.Div(f"{bank_dist[bank]}%", 
                    className="mobile-text-small",
                    style={'textAlign': 'center', 'marginTop': '5px'})
        ], style={'textAlign': 'center'})
        for bank in bank_dist.keys()
    ], className="d-flex justify-content-around align-items-center mb-4 flex-wrap")

    # Enhanced pie chart with dark mode compatibility
    pie_chart = go.Figure(data=[go.Pie(
        labels=list(bank_dist.keys()),
        values=list(bank_dist.values()),
        hole=0.3,
        marker=dict(colors=[bank_colors[bank] for bank in bank_dist.keys()]),
        textinfo='percent+label',
        textposition='outside',
        pull=[0.1 if share == max_share else 0 for share in bank_dist.values()],
        textfont=dict(family='Bebas Neue', size=12)
    )])

    pie_chart.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title={
            'text': "Bank Distribution",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, family='Bebas Neue')
        },
        height=500,
        margin=dict(t=80, b=30, l=20, r=20),
        showlegend=True,
        legend=dict(orientation="h", y=-0.1)
    )

    # Return the complete layout with title card
    main_content = [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Total Volume", className="text-center mobile-text-small"),
                        html.H3(f"${total_volume:,.2f}", 
                               className="text-center text-primary mobile-text-small")
                    ])
                ])
            ], xs=12, sm=12, md=4, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Total Transactions", className="text-center mobile-text-small"),
                        html.H3(f"{total_count:,}", 
                               className="text-center text-success mobile-text-small")
                    ])
                ])
            ], xs=12, sm=12, md=4, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Average Transaction", className="text-center mobile-text-small"),
                        html.H3(f"${avg_transaction:,.2f}", 
                               className="text-center text-info mobile-text-small")
                    ])
                ])
            ], xs=12, sm=12, md=4, className="mb-3"),
        ], className="mb-4 g-2"),

        # Peak Volume Analysis Card
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Pre-settlement Risk Analysis", 
                               className="text-center m-0 mobile-text-small")
                    ]),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5("Maximum Monthly Volume", 
                                           className="text-center mb-2 mobile-text-small"),
                                    html.H3(f"${partner_data['Volume'].max():,.2f}", 
                                           className="text-center text-danger mobile-text-small")
                                ], className="mb-3"),
                            ], xs=12, sm=12, md=4),
                            dbc.Col([
                                html.Div([
                                    html.H5("Average Monthly Volume", 
                                           className="text-center mb-2 mobile-text-small"),
                                    html.H3(f"${partner_data['Volume'].mean():,.2f}", 
                                           className="text-center text-primary mobile-text-small")
                                ], className="mb-3"),
                            ], xs=12, sm=12, md=4),
                            dbc.Col([
                                html.Div([
                                    html.H5("Volume Volatility", 
                                           className="text-center mb-2 mobile-text-small"),
                                    html.H3(f"{partner_data['Volume'].std() / partner_data['Volume'].mean():.1%}", 
                                           className="text-center text-warning mobile-text-small")
                                ], className="mb-3"),
                            ], xs=12, sm=12, md=4),
                        ], className="mobile-stack"),
                        html.Div([
                            html.P("Suggested Pre-settlement Limit Range:", 
                                   className="text-center mb-2 mobile-text-small"),
                            html.H4([
                                f"${partner_data['Volume'].max() * 1.2:,.2f}",
                                " - ",
                                f"${partner_data['Volume'].max() * 1.5:,.2f}"
                            ], className="text-center text-success mobile-text-small")
                        ])
                    ])
                ])
            ], width=12)
        ], className="mb-4"),

        # Charts and Tables
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=rolling_chart, config={'displayModeBar': False})
                    ])
                ], className="shadow-sm")
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=combined_chart, config={'displayModeBar': False})
                    ])
                ], className="shadow-sm")
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Bank Distribution", 
                               className="text-center m-0 mobile-text-small")
                    ]),
                    dbc.CardBody([
                        bank_images,
                        dcc.Graph(figure=pie_chart, config={'displayModeBar': False})
                    ])
                ], className="shadow-sm")
            ], width=12)
        ], className="mb-4"),

        # Transaction Details Table
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Transaction Details", 
                               className="text-center m-0 mobile-text-small")
                    ]),
                    dbc.CardBody([
                        dash_table.DataTable(
                            data=partner_data.to_dict('records'),
                            columns=[
                                {"name": "Month", "id": "Month"},
                                {"name": "Volume (USD)", "id": "Volume", 
                                 "type": "numeric", "format": {"specifier": "$,.2f"}},
                                {"name": "Transaction Count", "id": "Count"}
                            ],
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'textAlign': 'center',
                                'padding': '10px',
                                'backgroundColor': 'transparent',
                                'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
                                'minWidth': '100px',
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            },
                            style_header={
                                'backgroundColor': 'rgba(0,0,0,0.05)',
                                'fontWeight': 'bold',
                                'border': '1px solid var(--border-light)',
                                'fontFamily': 'Bebas Neue'
                            },
                            style_data={
                                'border': '1px solid var(--border-light)'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgba(0,0,0,0.02)'
                                }
                            ]
                        )
                    ])
                ], className="shadow-sm")
            ], width=12)
        ], className="mb-4")
    ]

    return main_content, title_card

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
