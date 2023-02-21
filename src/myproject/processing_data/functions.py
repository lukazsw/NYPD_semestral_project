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
    data['gdp'] = data['gdp'].dropna(how='all', axis=1)
    data['pop'] = data['pop'].dropna(how='all', axis=1)
    data['co2'] = data['co2'].dropna(how='all', axis=1)

    data['gdp'] = data['gdp'].drop(columns=['Indicator Name', 'Indicator Code', 'Country Code'])
    data['gdp'] = data['gdp'].drop(data['gdp'].columns[-1], axis=1)
    data['pop'] = data['pop'].drop(columns=['Indicator Name', 'Indicator Code', 'Country Code'])
    data['pop'] = data['pop'].drop(data['pop'].columns[-1], axis=1)

    return data
