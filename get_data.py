import pandas as pd
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import sys


def get_weather_data(station):
    """
    Some clever documentation.
    Loads data from the past 24 hours, with some lag (around 3 hours)
    This function was written by Brynjar in the climvis project, winter 2021. Modified
    """
    interval = "1"  # The data we load inn is the past 1 day
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


def get_climate_data(station):
    """
    Computes monthly climate stats 

    Parameters:
    ----------
    station : string
        Name of the location of the station in study

    --------
    returns: pandas dataframe
        monthly climate stats ( ----to be added-----) from the location
    """
    # read file
    df = pd.read_csv('./sample_data_20000101_20101231.csv')
    
    # some formatting
    df.index = pd.to_datetime(df['time'], format='%Y-%m-%d')
    
    # select location
    if station == 'innsbruck':
        stat_id = 11803.0
    if station == 'other_station':
        stati_id = 666
    else:
        print('station not implemented')
        
    df[df['station'] == stat_id]

    # compute some stats
    climate = pd.DataFrame(None, columns = ['mean', 'p95', 'p05'])
    climate['mean'] = df.groupby(by=[df.index.month]).mean().t
    climate['p95'] = df.groupby(by=[df.index.month]).quantile(0.95).t
    climate['p05'] = df.groupby(by=[df.index.month]).quantile(0.05).t
    #df.groupby(by=[df.index.month]).max()
    #df.groupby(by=[df.index.month]).min()

    return climate


# TODO: delete old get_climate_data, kept temporary to see old structure
# def get_climate_data(station):
#     '''Here we aggregate climate information to get monthly extreme values.
#     TODO: find better base data, this is only hourly from 1986-2012
#     '''
#     filename = station + '_weather_data1980_2012.csv'
#     df = pd.read_csv(filename, skiprows=1, header='infer', delimiter=';')
#     df['time'] = pd.to_datetime(df['rawdate'])
#     df = df.set_index('time')
#
#     out = {}
#     # Now that we have the climate data, we need to find monthly extreme
#     # values:
#     out['tl_max'] = df['ttx'].groupby(df.index.month).max().values
#     out['tl_min'] = df['ttx'].groupby(df.index.month).min().values
#     out['ff_max'] = df['vex'].groupby(df.index.month).max().values
#     out['td_max'] = df['tfx'].groupby(df.index.month).max().values
#     out['td_min'] = df['tfx'].groupby(df.index.month).max().values
#     out['rr_max'] = df['rsx'].groupby(df.index.month).max().values
#
#     return out


if __name__ == "__main__":
    # TESTING:
    weather = get_weather_data("innsbruck")
    climate = get_climate_data("innsbruck")
    print(weather)
    print(climate)
