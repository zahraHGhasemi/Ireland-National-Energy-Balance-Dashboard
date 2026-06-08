
import requests
from urllib.parse import urljoin
from io import BytesIO
import pandas as pd
from constant import UNIT, PAGE_URL
from datetime import datetime
import re
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/"
}


def get_latest_excel_url(filename):
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    # Try recent possible paths
    candidate_urls = []

    for year in range(current_year, current_year - 3, -1):

        max_month = current_month if year == current_year else 12

        for month in range(max_month, 0, -1):

            url = (
                f"https://www.seai.ie/sites/default/files/"
                f"{year}-{month:02d}/{filename}"
            )

            candidate_urls.append(url)
    for url in candidate_urls:
        try:
            response = requests.head(
                url,
                headers=HEADERS,
                allow_redirects=True,
                timeout=10
            )

            if response.status_code == 200:
                print(f"Found: {url}")
                return url

        except requests.RequestException:
            continue

    raise Exception("Could not find latest National Energy Balance file")


def get_excel_df(filename):
    excel_url = get_latest_excel_url(filename)

    response = requests.get(
        excel_url,
        headers=HEADERS,
        timeout=30
    )
    response.raise_for_status()

    excel_file = BytesIO(response.content)

    return pd.ExcelFile(excel_file)

def extract_year(sheet_name):
    match = re.search(r"\b(19|20)\d{2}\b", str(sheet_name))

    if match:
        return int(match.group())

    return None

def get_df(filename):
    # excel_file = pd.ExcelFile(filename)
    excel_file = get_excel_df(filename)
    all_sheets = excel_file.sheet_names

    combined_df = pd.DataFrame()

    for sheet_name in all_sheets:
        df_sheet = excel_file.parse(sheet_name)
        df_sheet = df_sheet.iloc[:71, :43]
        df_sheet.rename(columns={df_sheet.columns[0]: "sector"}, inplace=True)
        df_sheet.rename(columns={df_sheet.columns[1]: "NACE"}, inplace=True)
        df_sheet['year'] = extract_year(sheet_name)
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
    melted_df['unit'] = UNIT
    return melted_df

def get_year_min_max(filename):
    melted_df = get_df(filename)
    available_years = sorted(int(year) for year in melted_df['year'].dropna().unique())
    min_year = min(available_years)
    max_year = max(available_years)
    return min_year, max_year