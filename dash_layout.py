from dash import dcc
from dash import html

from constant import MAIN_FUELS, MAIN_SECTORS, SYSTEM_TABLE_OPTIONS

def dash_layout(min_year, max_year):
    return html.Div([

        # ======================
        # Header
        # ======================
        html.Div([
            html.H1(
                "Ireland National Energy Balance Dashboard",
                style={
                    "textAlign": "center",
                    "marginBottom": "10px"
                }
            ),
        ]),

        # ======================
        # Main Layout
        # ======================
        html.Div([

            # =====================================
            # LEFT PANEL (SETTINGS)
            # =====================================
            html.Div([

                html.H3("Year Range"),

                dcc.RangeSlider(
                    id='year-range-slider',
                    min=min_year,
                    max=max_year,
                    step=1,
                    value=[min_year, max_year],
                    allowCross=False,
                    tooltip={
                        "placement": "bottom"
                    }
                ),

                html.Hr(),

                html.H3("Chart Type Selection"),

                dcc.Dropdown(
                    id='chart-type-dropdown',
                    options=[
                        {'label': 'Stacked Bar Chart', 'value': 'stacked_bar'},
                        {'label': 'Stacked Area Chart', 'value': 'stacked_area'},
                        {'label': 'Line Chart', 'value': 'line'},
                        {'label': 'Share of Each (100%)', 'value': 'share_100'},
                        {'label': 'Average Annual Growth Rate', 'value': 'avg_growth_rate'}
                    ],
                    value='stacked_bar',
                    clearable=False
                ),

                html.Hr(),

                dcc.Tabs(
                    id="dashboard-tabs",
                    value='tab-1',
                    children=[

                        # ======================
                        # SYSTEM TAB
                        # ======================
                        dcc.Tab(
                            label='System',
                            value='tab-1',
                            children=[
                                html.Div([

                                    html.H3("System Selection"),

                                    dcc.Dropdown(
                                        id='sector-selection-dropdown',
                                        options=SYSTEM_TABLE_OPTIONS,
                                        value=SYSTEM_TABLE_OPTIONS[0]['value'],
                                        multi=False,
                                        placeholder="Select a metric",
                                        clearable=False
                                    ),

                                    html.Br(),

                                    html.H3("Fuel Selection"),

                                    dcc.Dropdown(
                                        id='fuel-selection-dropdown',
                                        multi=True,
                                        placeholder="Select fuels",
                                        clearable=False
                                    ),

                                ], style={"padding": "10px"})
                            ]
                        ),

                        # ======================
                        # SECTOR TAB
                        # ======================
                        dcc.Tab(
                            label='Sector',
                            value='tab-2',
                            children=[
                                html.Div([

                                    html.H3("Sector-Specific Analysis"),

                                    html.Label("Select Sector:"),
                                    dcc.Dropdown(
                                        id='sector-tab-sector-dropdown',
                                        options=MAIN_SECTORS,
                                        value=MAIN_SECTORS[0],
                                        placeholder="Select a sector",
                                        clearable=False
                                    ),

                                    html.Br(),

                                    html.Label("Select Subsector:"),
                                    dcc.Dropdown(
                                        id='sector-tab-subsector-dropdown',
                                        multi=False,
                                        placeholder="Select subsectors",
                                        clearable=False
                                    ),

                                    html.Br(),

                                    html.Label("Show Details:"),
                                    dcc.RadioItems(
                                        id='sector-tab-detail-radio',
                                        options=[
                                            {'label': 'Yes', 'value': 'yes'},
                                            {'label': 'No', 'value': 'no'}
                                        ],
                                        value='no',
                                        inline=True
                                    ),

                                ], style={"padding": "10px"})
                            ]
                        ),

                        # ======================
                        # FUEL TAB
                        # ======================
                        dcc.Tab(
                            label='Fuel',
                            value='tab-3',
                            children=[
                                html.Div([

                                    html.H3("Fuel-Specific Analysis"),

                                    html.Label("Select Fuel:"),
                                    dcc.Dropdown(
                                        id='fuel-tab-fuel-dropdown',
                                        options=[
                                            {'label': fuel, 'value': fuel}
                                            for fuel in MAIN_FUELS
                                        ],
                                        value=MAIN_FUELS[0],
                                        placeholder="Select a fuel",
                                        clearable=False
                                    ),

                                    html.Br(),

                                    html.Label("Select Subfuel:"),
                                    dcc.Dropdown(
                                        id='fuel-tab-subfuel-dropdown',
                                        options=[],
                                        multi=True,
                                        placeholder="Select subfuels",
                                        clearable=False
                                    ),

                                    html.Br(),

                                    html.Label("Show Details:"),
                                    dcc.RadioItems(
                                        id='fuel-tab-detail-radio',
                                        options=[
                                            {'label': 'Yes', 'value': 'yes'},
                                            {'label': 'No', 'value': 'no'}
                                        ],
                                        value='no',
                                        inline=True
                                    ),

                                ], style={"padding": "10px"})
                            ]
                        ),
                    ]
                )

            ],
            style={
                "width": "28%",
                "padding": "20px",
                "backgroundColor": "#f8f9fa",
                "borderRadius": "12px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
                "height": "fit-content"
            }),

            # =====================================
            # RIGHT PANEL (GRAPH AREA)
            # =====================================
            html.Div([

                dcc.Graph(
                    id='main-graph',
                    style={"height": "80vh"}
                )

            ],
            style={
                "width": "70%",
                "padding": "20px",
                "backgroundColor": "white",
                "borderRadius": "12px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
            })

        ],
        style={
            "display": "flex",
            "gap": "20px",
            "padding": "20px",
            "alignItems": "flex-start"
        })

        ,

        html.Button(
            "Download Data",
            id='download-data-button',
            n_clicks=0,
            style={
                "position": "fixed",
                "right": "28px",
                "bottom": "28px",
                "zIndex": 1000,
                "padding": "12px 18px",
                "backgroundColor": "#0d6efd",
                "color": "white",
                "border": "none",
                "borderRadius": "6px",
                "boxShadow": "0 3px 8px rgba(0,0,0,0.2)",
                "cursor": "pointer",
                "fontWeight": "600"
            }
        ),

        dcc.Download(id='download-graph-data')

    ])