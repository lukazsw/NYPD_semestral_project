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
    before_merge = set(
        list(data['gdp']['Country Name']) + list(data['pop']['Country Name']) + list(data['co2']['Country Name']))

    data_total = pd.merge(data['gdp'], data['pop'], how='outer', on=['Year', 'Country Name'])
    data_total = pd.merge(data_total, data['co2'], how='inner', on=['Year', 'Country Name'])

    after_merge = set(list(data_total['Country Name']))

    difference = before_merge - after_merge

    if difference:
        print('\nThese countries failed to match:', difference)

    data_total.dropna()
    return data_total


def co2_per_capita(data, n=5):
    co2_per_capita_data = data.copy()
    co2_per_capita_data['CO2 per Capita'] = co2_per_capita_data['CO2 Emission'] / co2_per_capita_data['Population']
    co2_per_capita_data = co2_per_capita_data.drop(columns=['GDP', 'Population'])
    co2_per_capita_data = co2_per_capita_data.sort_values(['Year', 'CO2 per Capita'], ascending=[True, False])

    result = pd.DataFrame(columns=co2_per_capita_data.columns)
    for year in co2_per_capita_data["Year"].unique():
        top_n = co2_per_capita_data[co2_per_capita_data["Year"] == year].head(n)
        result = pd.concat([result, top_n])
    # test
    return result


def gdp_per_capita(data, n=5):
    gdp_per_capita_data = data.copy()
    gdp_per_capita_data['GDP per Capita'] = gdp_per_capita_data['GDP'] / gdp_per_capita_data['Population']
    gdp_per_capita_data = gdp_per_capita_data.drop(columns=['CO2 Emission', 'Population'])
    gdp_per_capita_data = gdp_per_capita_data.sort_values(['Year', 'GDP per Capita'], ascending=[True, False])

    result = pd.DataFrame(columns=gdp_per_capita_data.columns)
    for year in gdp_per_capita_data["Year"].unique():
        top_n = gdp_per_capita_data[gdp_per_capita_data["Year"] == year].head(n)
        result = pd.concat([result, top_n])

    return result


def co2_change(data):
    co2_change_data = data.copy()
    co2_change_data['CO2 per Capita'] = co2_change_data['CO2 Emission'] / co2_change_data['Population']
    co2_change_data = co2_change_data.drop(columns=['CO2 Emission', 'Population', 'GDP'])

    end_year = co2_change_data['Year'].max()
    start_year = end_year - 10

    co2_change_data = co2_change_data.loc[(co2_change_data['Year'] == start_year) |
                                          (co2_change_data['Year'] == end_year)]

    co2_change_data = co2_change_data.pivot(index='Country Name', columns='Year', values='CO2 per Capita')
    co2_change_country = co2_change_data[end_year] - co2_change_data[start_year]

    return co2_change_country.idxmax(), co2_change_country.idxmin()


def data_analysis(gdp_src, pop_src, co2_src, start_year, end_year):
    data = load_data(gdp_src, pop_src, co2_src)
    data = clean_data(data)
    data = melt_data(data)
    data = merge_data(data)
    result_co2_change = co2_change(data)
    print('\n')
    print('The country that has most increased CO2 emissions per capita over the last 10 years:',
          result_co2_change[0])
    print('The country that has least increased CO2 emissions per capita over the last 10 years:',
          result_co2_change[1])
    print('\n')

    if start_year:
        data = data[data['Year'] >= start_year]
    else:
        start_year = data['Year'].min()

    if end_year:
        data = data[data['Year'] <= end_year]
    else:
        end_year = data['Year'].max()

    if data.empty:
        raise ValueError("Wrong range of years.")
    else:
        print('Countries that emitted the most CO2 per capita between', start_year, '-', end_year, ':')
        print(co2_per_capita(data))
        print('\n')
        print('Countries with the highest GDP per capita between:', start_year, '-', end_year, ':')
        print(gdp_per_capita(data))
