import dash
from dash import dcc, html, Input, Output, dash_table, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# Monthly_data
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

# Bank logo paths
bank_logos = {
    'KCB': '/assets/bank-logos/KCB.png',
    'DTB': '/assets/bank-logos/DTB.png',
    'NCBA': '/assets/bank-logos/NCBA.png',
    'Prime': '/assets/bank-logos/Prime.jpg',
    'SBM': '/assets/bank-logos/SBM.png',
    'Standard Investment Bank': '/assets/bank-logos/SIB.png',
    'Others': '/assets/bank-logos/Others.jpg'
}

# Bank color scheme
bank_colors = {
    'KCB': '#008000',      
    'DTB': '#FF0000',      
    'NCBA': '#000000',     
    'Prime': '#00008B',    
    'SBM': '#87CEEB',      
    'Others': '#FFD700',   
    'Standard Investment Bank': '#00008B'  
}

# App initialization
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

server = app.server

# Custom CSS 
app.index_string = '''<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Partner Report</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                font-family: 'Bebas Neue', sans-serif;
            }
            
            .regular-text {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            
            .card-body p, .card-body text {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            
            .card {
                margin-bottom: 1rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s;
            }
            
            .card:hover {
                transform: translateY(-5px);
            }
            
            .partner-logo {
                width: 100px;
                height: 100px;
                object-fit: contain;
                margin: 10px;
            }
            
            .market-share-card {
                background: linear-gradient(135deg, #f6f9fc 0%, #f1f4f8 100%);
            }
            
            .logo {
                transition: transform 0.3s ease;
            }
            
            .logo:hover {
                transform: scale(1.05);
            }
            
            /* Enhanced Responsive Styles */
            .js-plotly-plot {
                width: 100% !important;
            }

            .js-plotly-plot .plotly {
                width: 100% !important;
            }
            
            @media (max-width: 768px) {
                .partner-logo {
                    width: 60px;
                    height: 60px;
                    margin: 5px;
                }
                
                .card {
                    margin-bottom: 0.5rem;
                }
                
                h1 {
                    font-size: 1.8rem !important;
                }
                
                h3 {
                    font-size: 1.4rem !important;
                }
                
                h4 {
                    font-size: 1.2rem !important;
                }
                
                h5 {
                    font-size: 1rem !important;
                }
                
                .dash-table-container {
                    overflow-x: auto;
                }
                
                .card-body {
                    padding: 0.75rem;
                }
                
                .mobile-stack {
                    flex-direction: column;
                }
                
                .mobile-full-width {
                    width: 100% !important;
                }
                
                .mobile-text-small {
                    font-size: 0.9rem !important;
                }
                
                .mobile-chart-height {
                    height: 300px !important;
                }
            }
            
            @media (max-width: 576px) {
                .partner-logo {
                    width: 50px;
                    height: 50px;
                }
                
                h1 {
                    font-size: 1.5rem !important;
                }
                
                .mobile-padding {
                    padding: 0.5rem !important;
                }
                
                .mobile-margin {
                    margin: 0.5rem !important;
                }
            }
            
            /* Enhanced Dark mode support */
            @media (prefers-color-scheme: dark) {
                .card {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                }
                
                .market-share-card {
                    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                }
                
                .text-primary {
                    color: #3498db !important;
                }
                
                .text-success {
                    color: #2ecc71 !important;
                }
                
                .text-info {
                    color: #3498db !important;
                }
                
                .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner td,
                .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner th {
                    background-color: #2c3e50 !important;
                    color: #ecf0f1 !important;
                }
                
                .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner th {
                    background-color: #34495e !important;
                }
                
                .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:nth-child(odd) td {
                    background-color: #283747 !important;
                }
                
                .dash-table-container {
                    border: 1px solid #4a6278;
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

# App layout 
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(
                    src='/assets/vngrd.PNG',
                    className='logo',
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
                'padding': {'xs': '20px', 'md': '40px'},
                'marginBottom': {'xs': '15px', 'md': '30px'},
                'width': '100%'
            }, className="mobile-padding"),
            html.H1(
                "Partner Report",
                className="text-primary text-center mb-4",
                style={'letterSpacing': '2px'}
            )
        ])
    ]),

    # Partner selection row
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
    Output("partner-details", "children"),
    [Input("LEMFI-logo", "n_clicks"),
     Input("NALA-logo", "n_clicks"),
     Input("Cellulant-logo", "n_clicks"),
     Input("DLocal-logo", "n_clicks")]
)
def display_partner_details(lemfi_clicks, nala_clicks, cellulant_clicks, dlocal_clicks):
    if not ctx.triggered:
        return []

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    partner = triggered_id.replace("-logo", "")
    
    if partner == "DLocal":
        data_column = "DLocal/TTS"
        count_column = "DLocal_TTS_count"
    else:
        data_column = partner
        count_column = f"{partner}_count"

    # Extract partner-specific data
    partner_data = monthly_data[["Month", data_column, count_column]].copy()
    partner_data.columns = ["Month", "Volume", "Count"]
    partner_data = partner_data[partner_data['Volume'] > 0]

    # Calculate statistics
    total_volume = partner_data['Volume'].sum()
    total_count = partner_data['Count'].sum()
    avg_transaction = total_volume / total_count if total_count > 0 else 0

    # Title card with partner logo 
    partner_logo_map = {
        "LEMFI": "LEMFI.png",
        "NALA": "Nala.png",
        "Cellulant": "Cellulant.png",
        "DLocal": "DLocal.png"
    }
    
    title_card = dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Img(
                    src=f'/assets/partner-logos/{partner_logo_map[partner]}',
                    className="title-partner-logo",
                    style={
                        'height': '60px',  # Default size
                        'objectFit': 'contain',
                        'marginBottom': '10px'
                    }
                )
            ], className="text-center")
        ])
    ], className=f"shadow-sm mb-4 {partner}")

    # Combined volume and count chart
    combined_chart = go.Figure()
    
    # Volume line
    combined_chart.add_trace(go.Scatter(
        x=partner_data['Month'],
        y=partner_data['Volume'],
        name='Volume (USD)',
        yaxis='y1',
        line=dict(color='#2E86C1', width=3)
    ))
    
    # Count bars
    combined_chart.add_trace(go.Bar(
        x=partner_data['Month'],
        y=partner_data['Count'],
        name='Transaction Count',
        yaxis='y2',
        marker_color='rgba(231, 76, 60, 0.7)'
    ))
    
    combined_chart.update_layout(
        title={
            'text': f"{partner} Transaction Analysis",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, family='Bebas Neue')
        },
        yaxis=dict(
            title="Volume (USD)",
            titlefont=dict(color="#2E86C1"),
            tickfont=dict(color="#2E86C1"),
            gridcolor='rgba(189, 195, 199, 0.2)',
            tickformat="$,.0f"
        ),
        yaxis2=dict(
            title="Transaction Count",
            titlefont=dict(color="#E74C3C"),
            tickfont=dict(color="#E74C3C"),
            overlaying="y",
            side="right",
            gridcolor='rgba(189, 195, 199, 0.2)'
        ),
        plot_bgcolor='white',
        height=None,
        autosize=True,
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

    # Peak Volume Analysis Card
    peak_volume_card = dbc.Card([
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
        ], className="mobile-padding")
    ], className="shadow-sm mb-4")

    # Rolling Average Chart
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
        title={
            'text': "Volume Trend Analysis",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, family='Bebas Neue')
        },
        yaxis=dict(
            title="Volume (USD)",
            titlefont=dict(color="#2E86C1"),
            tickfont=dict(color="#2E86C1"),
            gridcolor='rgba(189, 195, 199, 0.2)',
            tickformat="$,.0f"
        ),
        plot_bgcolor='white',
        height=None,
        autosize=True,
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

    # Bank distribution with logos
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

    # Pie chart
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
        title={
            'text': "Bank Distribution",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, family='Bebas Neue')
        },
        height=None,
        autosize=True,
        margin=dict(t=80, b=30, l=20, r=20),
        showlegend=True,
        legend=dict(orientation="h", y=-0.1)
    )

    # Transaction table
    transaction_table = dash_table.DataTable(
        data=partner_data.to_dict('records'),
        columns=[
            {"name": "Month", "id": "Month"},
            {"name": "Volume (USD)", "id": "Volume", 
             "type": "numeric", "format": {"specifier": "$,.2f"}},
            {"name": "Transaction Count", "id": "Count"}
        ],
        style_table={
            'overflowX': 'auto',
            'minWidth': '100%'
        },
        style_cell={
            'textAlign': 'center',
            'padding': '10px',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
            'minWidth': '100px',
            'whiteSpace': 'normal',
            'height': 'auto',
            'backgroundColor': 'rgba(44, 62, 80, 0.9)',
            'color': '#ecf0f1'
        },
        style_header={
            'fontWeight': 'bold',
            'border': '1px solid #4a6278',
            'fontFamily': 'Bebas Neue',
            'backgroundColor': '#34495e',
            'color': '#ecf0f1'
        },
        style_data={
            'border': '1px solid #4a6278'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgba(40, 55, 71, 0.9)'
            }
        ],
        css=[{
            'selector': '.dash-table-container',
            'rule': 'max-width: 100%; overflow-x: auto; background-color: #2c3e50;'
        }]
    )

    # Return complete layout
    return [
        title_card,
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
        
        dbc.Row([
            dbc.Col([peak_volume_card], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            figure=rolling_chart,
                            config={'responsive': True},
                            className="mobile-chart-height"
                        )
                    ])
                ], className="shadow-sm")
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            figure=combined_chart,
                            config={'responsive': True},
                            className="mobile-chart-height"
                        )
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
                        dcc.Graph(
                            figure=pie_chart,
                            config={'responsive': True},
                            className="mobile-chart-height"
                        )
                    ])
                ], className="shadow-sm")
            ], width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Transaction Details", 
                               className="text-center m-0 mobile-text-small")
                    ]),
                    dbc.CardBody([
                        transaction_table
                    ], className="mobile-padding")
                ], className="shadow-sm")
            ], width=12)
        ], className="mb-4")
    ]

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
