
import pandas as pd

def get_df(filename):
    excel_file = pd.ExcelFile(filename)
    all_sheets = excel_file.sheet_names

    combined_df = pd.DataFrame()

    for sheet_name in all_sheets:
        df_sheet = excel_file.parse(sheet_name)
        df_sheet = df_sheet.iloc[:71, :43]
        df_sheet.rename(columns={df_sheet.columns[0]: "sector"}, inplace=True)
        df_sheet.rename(columns={df_sheet.columns[1]: "NACE"}, inplace=True)
        df_sheet['year'] = int(sheet_name)
        df_sheet.columns = df_sheet.columns.str.strip()
        combined_df = pd.concat([combined_df, df_sheet], ignore_index=True)

    # --- Data Melting (from original 8800e1c2) ---
    all_columns_melt = combined_df.columns.tolist()
    id_vars = ['sector', 'NACE', 'year']
    value_vars = [col for col in all_columns_melt if col not in id_vars and col != 'TOTAL']
    melted_df = pd.melt(combined_df,
                        id_vars=id_vars,
                        value_vars=value_vars,
                        var_name='fuels',
                        value_name='value')

    # --- Handle Missing Values in 'value' column (from original 42b76ecf) ---
    melted_df['value'] = melted_df['value'].fillna(0)
    melted_df = melted_df[melted_df['value'] != 0]

    return melted_df

def get_year_min_max(filename):
    melted_df = get_df(filename)
    available_years = sorted(int(year) for year in melted_df['year'].dropna().unique())
    min_year = min(available_years)
    max_year = max(available_years)
    return min_year, max_year