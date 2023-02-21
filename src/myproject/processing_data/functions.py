import pandas as pd


def load_data(gdp_src, pop_src, co2_src):
    gdp = pd.read_csv(gdp_src, skiprows=3)
    pop = pd.read_csv(pop_src, skiprows=3)
    co2 = pd.read_csv(co2_src)
    data_total = {
        'gdp': gdp,
        'pop': pop,
        'co2': co2
    }
    return data_total


def clean_data(data):
    data['gdp'] = data['gdp'].drop(columns=['Indicator Name', 'Indicator Code', 'Country Code'])
    data['gdp'] = data['gdp'].drop(data['gdp'].columns[-1], axis=1)
    data['gdp']['Country Name'] = data['gdp']['Country Name'].str.upper()

    data['pop'] = data['pop'].drop(columns=['Indicator Name', 'Indicator Code', 'Country Code'])
    data['pop'] = data['pop'].drop(data['pop'].columns[-1], axis=1)
    data['pop']['Country Name'] = data['pop']['Country Name'].str.upper()

    data['co2']['Total'] += data['co2']['Bunker fuels (Not in Total)']
    data['co2'] = data['co2'].drop(columns=['Solid Fuel', 'Liquid Fuel', 'Gas Fuel', 'Cement', 'Gas Flaring',
                                            'Per Capita', 'Bunker fuels (Not in Total)'])
    data['co2'] = data['co2'].rename({'Total': 'CO2 Emission', 'Country': 'Country Name'}, axis=1)

    return data


def melt_data(data):
    data['gdp'] = data['gdp'].melt(id_vars='Country Name', var_name='Year', value_name='GDP')
    data['gdp']['Year'] = data['gdp']['Year'].astype('int64')

    data['pop'] = data['pop'].melt(id_vars='Country Name', var_name='Year', value_name='Population')
    data['pop']['Year'] = data['pop']['Year'].astype('int64')

    return data


def merge_data(data):
    data_total = pd.merge(data['gdp'], data['pop'], how='outer', on=['Year', 'Country Name'])
    data_total = pd.merge(data_total, data['co2'], how='inner', on=['Year', 'Country Name'])
    return data_total


def co2_per_capita(data):
    co2_per_capita_data = data.copy()
    co2_per_capita_data['CO2 per Capita'] = co2_per_capita_data['CO2 Emission'] / co2_per_capita_data['Population']
    co2_per_capita_data = co2_per_capita_data.drop(columns=['GDP', 'Population'])
    co2_per_capita_data = co2_per_capita_data.sort_values(['Year', 'CO2 per Capita'], ascending=[True, False])

    result = pd.DataFrame(columns=co2_per_capita_data.columns)
    for year in co2_per_capita_data["Year"].unique():
        top_5 = co2_per_capita_data[co2_per_capita_data["Year"] == year].head(5)
        result = pd.concat([result, top_5])

    return result


def gdp_per_capita(data):
    gdp_per_capita_data = data.copy()
    gdp_per_capita_data['GDP per Capita'] = gdp_per_capita_data['GDP'] / gdp_per_capita_data['Population']
    gdp_per_capita_data = gdp_per_capita_data.drop(columns=['CO2 Emission', 'Population'])
    gdp_per_capita_data = gdp_per_capita_data.sort_values(['Year', 'GDP per Capita'], ascending=[True, False])

    result = pd.DataFrame(columns=gdp_per_capita_data.columns)
    for year in gdp_per_capita_data["Year"].unique():
        top_5 = gdp_per_capita_data[gdp_per_capita_data["Year"] == year].head(5)
        result = pd.concat([result, top_5])

    return result
