
import colorsys
import textwrap

from constant import DICT_FUELS, MAIN_FUELS, MAIN_SECTORS
import plotly.express as px
import pandas as pd



def find_fuels_with_single_entry():
    fuels_with_single_entry = []
    for fuel, subfuels in DICT_FUELS.items():
        if len(subfuels) == 1:
            fuels_with_single_entry.append(fuel)
    return fuels_with_single_entry

def generate_color_palette(n_colors):
    """
    Generate a diverse color palette for n_colors unique series.
    Uses HSL color space to ensure distinct colors even with many items.
    
    Args:
        n_colors (int): Number of colors to generate
        
    Returns:
        list: List of hex color codes
    """
    if n_colors <= 0:
        return []
    
    colors = []
    for i in range(n_colors):
        # Distribute hues evenly across the color wheel (0-1)
        hue = (i / n_colors) % 1.0
        # Use saturation 0.7 and lightness 0.5 for vibrant, distinct colors
        saturation = 0.7
        lightness = 0.5
        
        # Convert HSL to RGB using colorsys
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        
        # Convert to hex
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        colors.append(hex_color)
    
    return colors

def create_chart_figure(df_filtered, chart_type, color, unit=None):
    
    # Sort the categories alphabetically so color mapping stays stable across chart types
    unique_categories = sorted(df_filtered[color].dropna().astype(str).unique(), key=str)
    n_unique = len(unique_categories)
    color_palette = generate_color_palette(n_unique)
    category_orders = {color: unique_categories} if n_unique > 0 else None
    
    # Determine which columns to add to hover (those not already used)
    hover_cols = []
    hover_data_dict = {}
    if 'sector' in df_filtered.columns:
        hover_cols.append('sector')
        hover_data_dict['sector'] = True
    if 'fuels' in df_filtered.columns:
        hover_cols.append('fuels')
        hover_data_dict['fuels'] = True
    title = ""
    if color == 'sector':
        title = ",".join(df_filtered['fuels'].unique()) + " " + df_filtered['year'].min().astype(str) + "-" + df_filtered['year'].max().astype(str)
    if color == 'fuels':
        title = ",".join(df_filtered['sector'].unique()) + " " + df_filtered['year'].min().astype(str) + "-" + df_filtered['year'].max().astype(str)
    title = "<br>".join(textwrap.wrap(title, width=80))
    title = {
        "text": title,
        "x": 0.5,
        "xanchor": "center"
    }
    hover_data_dict['year'] = True
    # Don't format value here, we'll handle it in the template
    hover_data_dict['value'] = True
    
    if chart_type == 'stacked_bar':
        fig = px.bar(
            df_filtered,
            x='year',
            y='value',
            color=color,
            color_discrete_sequence=color_palette,
            category_orders=category_orders,
            hover_data=hover_data_dict
        )
        if 'sector' in hover_cols and 'fuels' in hover_cols:
            fig.update_traces(hovertemplate='<b>Year:</b> %{x}<br><b>Sector:</b> %{customdata[0]}<br><b>Fuel:</b> %{customdata[1]}<br><b>Value:</b> %{y:.2f}<extra></extra>')
        return fig.update_layout(barmode='stack', xaxis_title='Year', yaxis_title= unit, title = title)
    elif chart_type == 'stacked_area':
        fig = px.area(
            df_filtered,
            x='year',
            y='value',
            color=color,
            color_discrete_sequence=color_palette,
            category_orders=category_orders,
            hover_data=hover_data_dict
        )
        if 'sector' in hover_cols and 'fuels' in hover_cols:
            fig.update_traces(hovertemplate='<b>Year:</b> %{x}<br><b>Sector:</b> %{customdata[0]}<br><b>Fuel:</b> %{customdata[1]}<br><b>Value:</b> %{y:.2f}<extra></extra>')
        return fig.update_layout(xaxis_title='Year', yaxis_title= unit, title = title)
    elif chart_type == 'line':
        fig = px.line(
            df_filtered,
            x='year',
            y='value',
            color=color,
            markers=True,
            color_discrete_sequence=color_palette,
            category_orders=category_orders,
            hover_data=hover_data_dict
        )
        if 'sector' in hover_cols and 'fuels' in hover_cols:
            fig.update_traces(hovertemplate='<b>Year:</b> %{x}<br><b>Sector:</b> %{customdata[0]}<br><b>Fuel:</b> %{customdata[1]}<br><b>Value:</b> %{y:.2f}<extra></extra>')
        return fig.update_layout(xaxis_title='Year', yaxis_title= unit, title = title)
    elif chart_type == 'share_100':
        total_value_per_year = df_filtered.groupby('year')['value'].sum().reset_index()
        total_value_per_year.rename(columns={'value': 'total_year_value'}, inplace=True)
        share_data = pd.merge(df_filtered, total_value_per_year, on='year')
        share_data['percentage'] = (share_data['value'] / share_data['total_year_value']) * 100
        
        hover_data_dict_pct = {col: True for col in hover_cols}
        hover_data_dict_pct['year'] = True
        hover_data_dict_pct['percentage'] = True
        
        fig = px.bar(
            share_data,
            x='year',
            y='percentage',
            color=color,
            color_discrete_sequence=color_palette,
            category_orders=category_orders,
            hover_data=hover_data_dict_pct
        )
        if 'sector' in hover_cols and 'fuels' in hover_cols:
            fig.update_traces(hovertemplate='<b>Year:</b> %{x}<br><b>Sector:</b> %{customdata[0]}<br><b>Fuel:</b> %{customdata[1]}<br><b>Percentage:</b> %{y:.2f}%<extra></extra>')
        return fig.update_layout(barmode='stack', xaxis_title='Year', yaxis_title='Percentage Share (%)', yaxis_range=[0, 100], title=title)
    elif chart_type == 'avg_growth_rate':
        total_yearly_data = df_filtered.groupby('year')['value'].sum().reset_index()
        total_yearly_data.set_index('year', inplace=True)
        total_yearly_data['growth_rate'] = total_yearly_data['value'].pct_change() * 100
        total_yearly_data.reset_index(inplace=True)
        growth_rate_data = total_yearly_data.dropna(subset=['growth_rate'])
        if not growth_rate_data.empty:
            fig = px.line(growth_rate_data, x='year', y='growth_rate', markers=True)
            return fig.update_layout(xaxis_title='Year', yaxis_title='Growth Rate (%)', title=title)
        else:
            fig = px.line(title="Not enough data to calculate growth rate.")
            return fig

def prepare_system_tab_data(selected_sector, selected_fuels, year_range, chart_type, melted_df):
    if not selected_sector or not selected_fuels:
        return pd.DataFrame()  

    if isinstance(selected_fuels, str):
        selected_fuels = [selected_fuels]

    filtered_df = melted_df[
        (melted_df['sector'] == selected_sector)
        &
        (melted_df['fuels'].isin(selected_fuels))
    ]
    filtered_df = filter_by_year_range(filtered_df, year_range)
    return filtered_df
   
def prepare_sector_tab_data(selected_subsector, sector_tab_sector, sector_show_details, year_range, melted_df):
    if not selected_subsector:
        return pd.DataFrame()

    if isinstance(selected_subsector, str):
        selected_subsector = [selected_subsector]

    if selected_subsector != ["all"]:
        filtered_df = melted_df[
            melted_df['sector'].isin(selected_subsector)
        ]
    else:
        filtered_df = melted_df[
            melted_df['sector'] == sector_tab_sector
        ]
    filtered_df = filter_by_year_range(filtered_df, year_range)

    if sector_show_details != 'yes':
        filtered_df = filtered_df[
            filtered_df['fuels'].isin(MAIN_FUELS)
        ]
    else:
        filtered_df = filtered_df[
            (~filtered_df['fuels'].isin(MAIN_FUELS))
            |
            (
                filtered_df['fuels'].isin(
                    find_fuels_with_single_entry()
                )
            )
        ]
    return filtered_df
def prepare_fuel_tab_data(selected_subfuels, selected_fuel, fuel_show_details, year_range, melted_df):
    if not selected_subfuels:
        return pd.DataFrame()

    if isinstance(selected_subfuels, str):
        selected_subfuels = [selected_subfuels]

    filtered_df = melted_df[
        melted_df['sector'].isin(MAIN_SECTORS)
    ]

    filtered_df = filtered_df[
        filtered_df['fuels'].isin(selected_subfuels)
    ]
    filtered_df = filter_by_year_range(filtered_df, year_range)

    if fuel_show_details != 'yes':
        filtered_df = (
            filtered_df
            .groupby(
                ['year', 'sector', 'unit'],
                as_index=False
            )['value']
            .sum()
        )

        filtered_df['fuels'] = (
            selected_fuel
            + " ("
            + ", ".join(selected_subfuels)
            + ")"
        )
    return filtered_df

 

def filter_by_year_range(df, year_range):
    if not year_range or len(year_range) != 2:
        return df

    start_year, end_year = sorted(year_range)
    return df[
        (df['year'] >= start_year)
        &
        (df['year'] <= end_year)
    ]


def get_current_graph_data(
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
):
    if active_tab == 'tab-1':
        return prepare_system_tab_data(
            selected_sector,
            selected_fuels,
            year_range,
            chart_type,
            melted_df
        )

    if active_tab == 'tab-2':
        return prepare_sector_tab_data(
            selected_subsector,
            sector_tab_sector,
            sector_show_details,
            year_range,
            melted_df
        )

    if active_tab == 'tab-3':
        return prepare_fuel_tab_data(
            selected_subfuels,
            selected_fuel,
            fuel_show_details,
            year_range,
            melted_df
        )

    return pd.DataFrame()


