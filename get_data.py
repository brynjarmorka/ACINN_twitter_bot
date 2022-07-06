import pandas as pd
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import sys


def get_weather_data(station="innsbruck"):
    """
    Loads data from the past 24 hours.
    This function was written by Brynjar in the climvis project, winter 2021. Modified
    """
    interval = "1"  # The data we load inn is the past 1 day. Can be 1, 3 or 7
    if station == "innsbruck":
        print("selected station is innsbruck")
    elif station == "other_station":
        Warning("Warning: Station is not innsbruck")
    else:
        raise ValueError("station not implemented")

    url = f"https://acinn-data.uibk.ac.at/{station}/{interval}"
    # Parse the given url
    try:
        req = urlopen(Request(url)).read()
    except HTTPError:
        sys.exit(
            f"HTTPError. The url did not work. Check your connection. Check the url yourself:\n{url}"
        )
    # Read the data
    df = pd.read_json(req.decode("utf-8"))
    df["time"] = [
        datetime(1970, 1, 1) + timedelta(milliseconds=ds) for ds in df["datumsec"]
    ]
    # Check if the df is empty.
    if df.isnull().values.any():
        sys.exit(
            f"Something is wrong on the ACINN database. Try again, or visit the url yourself:\n{url}"
        )

    return df


def get_climate_data(station="innsbruck"):
    """
    Computes monthly climate stats
    Parameters:
    ----------
    station : string
        Name of the location of the station in study. Default: innsbruck
    --------
    returns: pandas dataframe
        monthly climate stats ( ----to be added-----) from the location
    """
    # read file
    df = pd.read_parquet("df_ibk.parquet.gzip")
    # compute some stats
    climate = pd.DataFrame(None, columns=["min", "p05", "mean", "p95", "max"])
    climate["min"] = df.groupby(by=[df.index.month]).min().t
    climate["p05"] = df.groupby(by=[df.index.month]).quantile(0.05).t
    climate["mean"] = df.groupby(by=[df.index.month]).mean().t
    climate["p95"] = df.groupby(by=[df.index.month]).quantile(0.95).t
    climate["max"] = df.groupby(by=[df.index.month]).max().t

    return climate


#if __name__ == "__main__":
    # TESTING:
    #weather = get_weather_data("innsbruck")
    #climate = get_climate_data("innsbruck")
    #print(weather)
    #print(climate)
