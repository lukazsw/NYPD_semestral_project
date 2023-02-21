import argparse
import os

THIS_DIR = os.path.dirname(os.path.relpath(__file__))


def parse_path(path):
    return os.path.join(THIS_DIR, os.pardir, path)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gdp_file", type=str, required=True,
                        help="Path to the CSV file containing GDP data.")
    parser.add_argument("--population_file", type=str, required=True,
                        help="Path to the CSV file containing population data.")
    parser.add_argument("--emissions_file", type=str, required=True,
                        help="Path to the CSV file containing CO2 emissions data.")
    parser.add_argument("--start_year", type=int, default=1960,
                        help="Starting year for analysis (inclusive).")
    parser.add_argument("--end_year", type=int, default=2021,
                        help="Ending year for analysis (inclusive).")
    return parser.parse_args()


if __name__ == '__main__':
    print("Hello World!\n")
