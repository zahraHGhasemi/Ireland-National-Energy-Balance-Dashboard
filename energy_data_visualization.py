
import dash
from callback import register_callbacks
from dash_layout import dash_layout
from read_data import get_year_min_max, get_df

if __name__ == '__main__':
    app = dash.Dash(__name__)
    filename = "National-Energy-Balance.xlsx"
    df = get_df(filename)
    min_year, max_year = get_year_min_max(filename)
    app.layout = dash_layout(min_year, max_year)
    register_callbacks(app, df)
    app.run(debug=True)

