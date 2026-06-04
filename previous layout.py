# app.layout = html.Div([
#     html.H1("National Energy Balance Dashboard"),
#     html.H3("Chart Type Selection"),
#                 dcc.Dropdown(
#                     id='chart-type-dropdown',
#                     options=[
#                         {'label': 'Stacked Bar Chart', 'value': 'stacked_bar'},
#                         {'label': 'Stacked Area Chart', 'value': 'stacked_area'},
#                         {'label': 'Line Chart', 'value': 'line'},
#                         {'label': 'Share of Each (100%)', 'value': 'share_100'},
#                         {'label': 'Average Annual Growth Rate', 'value': 'avg_growth_rate'}
#                     ],
#                     value='stacked_bar',
#                     clearable=False
#                 ),
#     dcc.Tabs(id="dashboard-tabs", value='tab-1', children=[
#         dcc.Tab(label='System', value='tab-1', children=[
#             html.Div(id='system-content', children=[
#               html.H3("System Selection"),
#                 dcc.Dropdown(
#                     id='sector-selection-dropdown',
#                     options=system_table_options,
#                     value=system_table_options[0]['value'],
#                     multi=False,
#                     placeholder="Select a metric"
#                 ),
#                 html.H3("Fuel Selection"),
#                 dcc.Dropdown(
#                     id='fuel-selection-dropdown',
#                     multi=True,
#                     placeholder="Select fuels"
#                 ),
#                 dcc.Graph(id='system-overview-graph')
#             ])
#         ]),
#         dcc.Tab(label='Sector', value='tab-2', children=[
#             html.Div(id='sector-content', children=[
#                 html.Div([
#                     html.H3("Sector-Specific Analysis"),
#                     html.Div([
#                         html.Label("Select Sector:"),
#                         dcc.Dropdown(
#                             id='sector-tab-sector-dropdown',
#                             options= main_sectors,
#                             value = main_sectors[0],
#                             placeholder="Select a sector"
#                         ),
#                     ]),
#                     html.Div([
#                         html.Label("Select Subsector:"),
#                         dcc.Dropdown(
#                             id='sector-tab-subsector-dropdown',
#                             multi= False,
#                             placeholder="Select subsectors"
#                         ),
#                     ]),
#                     html.Div([
#                         html.Label("Show Details:"),
#                         dcc.RadioItems(
#                             id='sector-tab-detail-radio',
#                             options=[
#                                 {'label': 'Yes', 'value': 'yes'},
#                                 {'label': 'No', 'value': 'no'}
#                             ],
#                             value='no',
#                             inline=True
#                         ),
#                     ]),
#                     dcc.Graph(id='sector-tab-graph')
#                 ])
#             ])

#         ]),
#         dcc.Tab(label='Fuel', value='tab-3', children=[
#             html.Div(id='fuel-content', children=[
#                 html.H3("Fuel-Specific Analysis"),
#                 html.Div([
#                     html.Label("Select Fuel:"),
#                     dcc.Dropdown(
#                         id='fuel-tab-fuel-dropdown',
#                         options=[{'label': fuel, 'value': fuel} for fuel in main_fuels],
#                         value = main_fuels[0],
#                         placeholder="Select a fuel"
#                     ),
#                 ]),
#                 html.Div([
#                     html.Label("Select Subfuel:"), 
#                     dcc.Dropdown(
#                         id='fuel-tab-subfuel-dropdown',
#                         options=[], # Populated by callback
#                         multi=True,
#                         placeholder="Select subfuels"
#                     ),
#                 ]),
#                 html.Div([
#                     html.Label("Show Details:"),
#                     dcc.RadioItems(
#                         id='fuel-tab-detail-radio',
#                         options=[
#                             {'label': 'Yes', 'value': 'yes'},
#                             {'label': 'No', 'value': 'no'}
#                         ],
#                         value='no',
#                         inline=True
#                     ),
#                 ]),
#                 dcc.Graph(id='fuel-tab-graph')
#                 ])
#         ])
#     ]),
#     html.Div(id='tabs-content')
# ])
# @app.callback(
#     Output('system-overview-graph', 'figure'),
#     Input('sector-selection-dropdown', 'value'),
#     Input('fuel-selection-dropdown', 'value'),
#     Input('chart-type-dropdown', 'value')
# )
# def render_system_overview_graph(selected_sector, selected_fuels, chart_type):
#     if not selected_sector or not selected_fuels:
#         return None
#     if type(selected_fuels) == str:
#         selected_fuels = [selected_fuels]
#     filtered_df = melted_df[(melted_df['sector'] == selected_sector) & (melted_df['fuels'].isin(selected_fuels))]
#     fig = create_chart_figure(filtered_df, chart_type, color='fuels')
#     return fig



# @app.callback(
#     Output('sector-tab-graph', 'figure'),
#     Input('sector-tab-sector-dropdown', 'value'),
#     Input('sector-tab-subsector-dropdown', 'value'),
#     Input('chart-type-dropdown', 'value'),
#     Input('sector-tab-detail-radio', 'value'),

# )
# def render_sector_tab_graph(selected_sector, selected_subsector, chart_type, show_details):
#     if not selected_subsector:
#         return None
#     if type(selected_subsector) == str:
#         selected_subsector = [selected_subsector]
#     if selected_subsector != ["all"]:
#         filtered_df = melted_df[melted_df['sector'].isin(selected_subsector)]
#     else: 
#         filtered_df = melted_df[melted_df['sector'] == selected_sector]

#     if show_details != 'yes':
#         filtered_df = filtered_df[filtered_df['fuels'].isin(main_fuels)]
#     else:
#         filtered_df = filtered_df[(filtered_df['fuels'].isin(main_fuels) == False) | (filtered_df['fuels'].isin(find_fuels_with_single_entry()))]
        
#     fig = create_chart_figure(filtered_df, chart_type, color='fuels')
#     return fig



# @app.callback(
#     Output('fuel-tab-graph', 'figure'),
#     Input('fuel-tab-fuel-dropdown', 'value'),
#     Input('fuel-tab-subfuel-dropdown', 'value'),
#     Input('chart-type-dropdown', 'value'),
#     Input('fuel-tab-detail-radio', 'value'),

# )
# def render_fuel_tab_graph(selected_fuel, selected_subfuels, chart_type, show_details):
#     if not selected_subfuels:
#         return None
#     if type(selected_subfuels) == str:
#         selected_subfuels = [selected_subfuels]
#     filtered_df = melted_df[melted_df['sector'].isin(main_sectors)]
#     filtered_df = filtered_df[filtered_df['fuels'].isin(selected_subfuels)]
#     if show_details != 'yes':
#         filtered_df = filtered_df.groupby(['year', 'sector'], as_index=False)['value'].sum()
#         filtered_df['fuels'] = selected_fuel + "(" + ", ".join(selected_subfuels) + ")"
#     fig = create_chart_figure(filtered_df, chart_type, color='sector')
#     return fig

# @app.callback(
#     Output('tabs-content', 'children'),
#     Input('dashboard-tabs', 'value')
# )
# def render_content(tab):
    
#     if tab == 'tab-1':
#         return html.Div([
#             html.H3('System Overview Content'),
#         ])
#     elif tab == 'tab-2':
#         return html.Div([
#             html.H3('Sector Specific Analysis Content'),
#         ])
#     elif tab == 'tab-3':
#         return html.Div([
#             html.H3('Fuel Specific Analysis Content'),
#         ])