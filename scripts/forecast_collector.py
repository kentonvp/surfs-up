import os
from pprint import PrettyPrinter
from surfsup.dto.forecast_parser import ForecastFetcher
from surfsup.utils import joinpath


def main():
    pp = PrettyPrinter(indent=2)
    # set up surfline api
    cwd = os.getcwd()
    print(cwd)
    db_path = joinpath(cwd, "data", "spot_lookups.csv")
    fcst_fetcher = ForecastFetcher(db_path, 16)
    forecast_results = fcst_fetcher.runner(["Blacks", "Blackies", "La Jolla Shores"])

    pp.pprint(forecast_results["Blacks"])
    fcst_fetcher.to_csv(forecast_results)


if __name__ == "__main__":
    main()
