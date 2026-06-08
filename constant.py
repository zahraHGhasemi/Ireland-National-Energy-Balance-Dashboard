PAGE_URL = "https://www.seai.ie/data-and-insights/seai-statistics/key-publications/national-energy-balance"

UNIQUE_SYSTEM_TABLE = ["Indigenous Production",
                  "Imports",
                  "Exports",
                  "Mar. Bunkers",
                  "Stock Change",
                  "Primary Energy Supply (incl non-energy)",
                  "Primary Energy Requirement (excl. non-energy)",
                  "Transformation Input",
                  "Public Thermal Power Plants (Input)",
                  "Combined Heat and Power Plants (Input)",
                  "Pumped & Battery Storage (Input)",
                  "Briquetting Plants (Input)",
                  "Oil Refineries & other energy sector (Input)",
                  "Transformation Output",
                  "Public Thermal Power Plants (Output)",
                  "Combined Heat and Power Plants (Output)",
                  "Pumped & Battery Storage (Output)",
                  "Briquetting Plants (Output)",
                  "Oil Refineries & other energy sector (Output)",
                  "Exchanges and transfers",
                  "Own Use and Distribution Losses",
                  "Available Final Energy Consumption",
                  "Non-Energy Consumption",
                  "Total Final Energy Consumption"
                  ]
MAIN_FUELS = ['Coal','Peat', 'Oil','Natural Gas', 'Renewables', 'Non-Renewable  Waste', 'Electricity', 'Heat', "TOTAL"]
DICT_FUELS = {
    'Coal': ['Bituminous Coal', 'Anthracite + Manufactured Ovoids', 'Coke', 'Lignite \\ Brown Coal Briquettes'],
    'Peat': ['Milled Peat',	 'Sod Peat',	 'Briquettes'],
    'Oil': ['Crude', 'Refinery Feedstocks', 'Refinery Gas', 'Gasoline', 'Kerosene',
            'Jet Kerosene',	'Fueloil',	'LPG',	'Gasoil / Diesel /DERV', 'Petroleum Coke',
            'Naphta','Bitumen',	'White Spirit',	'Lubricants'
            ],
    'Natural Gas': ['Natural Gas'],
    'Renewables': ['Hydro',	 'Wind',	 'Biomass',	 'Renewable Waste',	 'Landfill Gas',	 'Biogas',	 'Biodiesel',	 'Bioethanol',	 'Solar Photovoltaic',	 'Solar Thermal',	 'Ambient Heat'],
    'Non-Renewable  Waste': ['Non-Renewable  Waste'],
    'Electricity': ['Electricity'],
    'Heat': ['Heat']
}
DICT_SECTORS = {
    'Industry*': ['Non-Energy Mining',
                  "Food & beverages",
                  "Textiles and textile products",
                  'Wood and wood products',
                  'Pulp, paper, publishing and printing',
                  'Chemicals & man-made fibres',
                  'Rubber and plastic products',
                  'Other non-metallic mineral products',
                  'Basic metals and fabricated metal products',
                  'Machinery and equipment n.e.c.',
                  'Electrical and optical equipment',
                  'Transport equipment manufacture',
                  'Other manufacturing',
                  'Construction'],
    'Transport': ['Road Freight',
                  'Road Light Goods Vehicle',
                  'Road Private Car',
                  'Public Passenger Services',
                  'Rail',
                  'Domestic Aviation',
                  'International Aviation',
                  'Fuel Tourism',
                  'Navigation',
                  'Unspecified (other road and pipeline)',
                  ],
    'Residential':['Residential'],
    'Commercial Services*':['Wholesale, Retail and Vehicle Repair',
                            'Transportation and Storage',
                            'Accommodation and Food Services',
                            'Information and Communication',
                            'Financial, Insurance and Real Estate Activities',
                            'Other Services Sectors'
                            ],
    'Public Services*':['Water Supply, Sewerage, and Waste Management',
                        'Public Administration',
                        'Education',
                        'Health, Residential Care and Social Work Activities'
                        ],
    'Agricultural':['Agricultural'],
    'Fisheries':['Fisheries'],
    "Public Thermal Power Plants (Input)": ["Public Thermal Power Plants (Input)"]

}
UNIT_DICT = {
    'ktoe': 1,
    'TJ': 41.87,
    'TWh': 0.01163
}   
MAIN_FUELS = list(DICT_FUELS.keys())
MAIN_SECTORS = list(DICT_SECTORS.keys())
SYSTEM_TABLE_OPTIONS = [{'label': sector, 'value': sector} for sector in UNIQUE_SYSTEM_TABLE]
SYSTEM_TABLE_OPTIONS.extend({'label': sector, 'value': sector} for sector in MAIN_SECTORS)
UNIT = 'ktoe'
