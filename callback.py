
from dash import Input, Output, State, dcc
from dash.exceptions import PreventUpdate
from constant import DICT_FUELS, DICT_SECTORS, MAIN_FUELS, UNIT_DICT
from read_data import get_df
from utils import get_current_graph_data, create_chart_figure

def register_callbacks(app, melted_df):

    @app.callback(
        Output('main-graph', 'figure'),

        Input('dashboard-tabs', 'value'),

        # Shared input
        Input('chart-type-dropdown', 'value'),
        Input('year-range-slider', 'value'),
        Input('unit-selection-dropdown', 'value'),

        # System tab
        Input('sector-selection-dropdown', 'value'),
        Input('fuel-selection-dropdown', 'value'),

        # Sector tab
        Input('sector-tab-sector-dropdown', 'value'),
        Input('sector-tab-subsector-dropdown', 'value'),
        Input('sector-tab-detail-radio', 'value'),

        # Fuel tab
        Input('fuel-tab-fuel-dropdown', 'value'),
        Input('fuel-tab-subfuel-dropdown', 'value'),
        Input('fuel-tab-detail-radio', 'value'),
    )
    def update_main_graph(
        active_tab,
        chart_type,
        year_range,
        unit,

        # System
        selected_sector,
        selected_fuels,

        # Sector
        sector_tab_sector,
        selected_subsector,
        sector_show_details,

        # Fuel
        selected_fuel,
        selected_subfuels,
        fuel_show_details
    ):
        filtered_df = get_current_graph_data(
            active_tab,
            chart_type,
            year_range,
            selected_sector,
            selected_fuels,
            sector_tab_sector,
            selected_subsector,
            sector_show_details,
            selected_fuel,
            selected_subfuels,
            fuel_show_details,
            melted_df
        )
        filtered_df['value'] = filtered_df['value'] * UNIT_DICT.get(unit, 1)
        if filtered_df.empty:
            return {}

        color = 'sector' if active_tab == 'tab-3' else 'fuels'
        return create_chart_figure(
            filtered_df,
            chart_type,
            color=color,
            unit=unit
        )


    @app.callback(
        Output('download-graph-data', 'data'),
        Input('download-data-button', 'n_clicks'),
        State('dashboard-tabs', 'value'),
        State('chart-type-dropdown', 'value'),
        State('year-range-slider', 'value'),
        State('sector-selection-dropdown', 'value'),
        State('fuel-selection-dropdown', 'value'),
        State('sector-tab-sector-dropdown', 'value'),
        State('sector-tab-subsector-dropdown', 'value'),
        State('sector-tab-detail-radio', 'value'),
        State('fuel-tab-fuel-dropdown', 'value'),
        State('fuel-tab-subfuel-dropdown', 'value'),
        State('fuel-tab-detail-radio', 'value'),
        prevent_initial_call=True
    )
    def download_current_graph_data(
        n_clicks,
        active_tab,
        chart_type,
        year_range,
        selected_sector,
        selected_fuels,
        sector_tab_sector,
        selected_subsector,
        sector_show_details,
        selected_fuel,
        selected_subfuels,
        fuel_show_details
    ):
        if not n_clicks:
            raise PreventUpdate

        filtered_df = get_current_graph_data(
            active_tab,
            chart_type,
            year_range,
            selected_sector,
            selected_fuels,
            sector_tab_sector,
            selected_subsector,
            sector_show_details,
            selected_fuel,
            selected_subfuels,
            fuel_show_details,
            melted_df
        )

        if filtered_df.empty:
            raise PreventUpdate

        return dcc.send_data_frame(
            filtered_df.to_csv,
            "output_df.csv",
            index=False
        )


    @app.callback(
        Output('fuel-selection-dropdown', 'options'),
        Output('fuel-selection-dropdown', 'value'),
        Input('sector-selection-dropdown', 'value')
    )
    def update_fuel_options(selected_sector):
        if not selected_sector:
            return [], None
        filtered_df = melted_df[melted_df['sector'] == selected_sector]
        unique_fuels = [fuel for fuel in MAIN_FUELS if fuel in filtered_df['fuels'].unique()]
        options = [{'label': fuel, 'value': fuel} for fuel in unique_fuels]
        value = [fuel for fuel in unique_fuels]
        return options, value




    @app.callback(
        Output('sector-tab-subsector-dropdown', 'options'),
        Output('sector-tab-subsector-dropdown', 'value'),
        Input('sector-tab-sector-dropdown', 'value')
    )
    def update_sector_tab_subsector_options(selected_sector):
        if not selected_sector:
            return [], None
        dict_sector_subsectors = DICT_SECTORS.get(selected_sector, [])
        options = [{'label': subsector, 'value': subsector} for subsector in dict_sector_subsectors if subsector in melted_df['sector'].unique()]
        options.append({'label': 'All Subsectors', 'value': 'all'})
        value = 'all'
        return options, value





    @app.callback(
        Output('fuel-tab-subfuel-dropdown', 'options'),
        Output('fuel-tab-subfuel-dropdown', 'value'),
        Input('fuel-tab-fuel-dropdown', 'value')
    )
    def update_fuel_tab_subfuel_options(selected_fuel):
        if not selected_fuel:
            return []
        unique_subfuels = [subfuel for subfuel in DICT_FUELS.get(selected_fuel, []) if subfuel in melted_df['fuels'].unique()]
        options = [{'label': subfuel, 'value': subfuel} for subfuel in unique_subfuels]
        value = [subfuel for subfuel in unique_subfuels]
        return options, value


