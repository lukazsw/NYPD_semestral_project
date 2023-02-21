import argparse
import os
import processing_data.functions as data_fun

THIS_DIR = os.path.dirname(os.path.relpath(__file__))


def parse_path(path):
    return os.path.join(THIS_DIR, os.pardir, path)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-gdp_file", type=str, default='data/gdp.csv',
                        help="Path to the CSV file containing GDP data.")
    parser.add_argument("-population_file", type=str, default='data/pop.csv',
                        help="Path to the CSV file containing population data.")
    parser.add_argument("-emissions_file", type=str, default='data/co2.csv',
                        help="Path to the CSV file containing CO2 emissions data.")
    parser.add_argument("-start_year", type=int, default=None,
                        help="Starting year for analysis (inclusive).")
    parser.add_argument("-end_year", type=int, default=None,
                        help="Ending year for analysis (inclusive).")
    return parser.parse_args()


if __name__ == '__main__':
    arg = parse_arguments()
    gdp_src = parse_path(arg.gdp_file)
    pop_src = parse_path(arg.population_file)
    co2_src = parse_path(arg.emissions_file)
    data = data_fun.load_data(gdp_src, pop_src, co2_src)
    data = data_fun.clean_data(data)
    print(data)
