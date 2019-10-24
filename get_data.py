import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def get_weather_data(station):
    '''Get the current weather data from the University of Innsbruck station
    We always get the last 3 hours.
    '''
    base_url = 'http://meteo145.uibk.ac.at/'
    time = str(3)
    
    url = base_url + station + '/' + time
    
    df = pd.read_json(url)
    df['time'] = [datetime(1970, 1, 1) + timedelta(milliseconds=ds)
                  for ds in df['datumsec']]
    df = df.set_index('time')
    df = df.drop(columns='datumsec')
    
    for column in df.columns:
        df[df[column] == -99.9] = np.nan

    return df


def get_climate_data(station):
    '''Here we aggregate climate information to get monthly extreme values.
    TODO: find better base data, this is only hourly from 1986-2012
    '''
    filename = station + '_weather_data1980_2012.csv'
    df = pd.read_csv(filename, skiprows=1, header='infer', delimiter=';')
    df['time'] = pd.to_datetime(df['rawdate'])
    df = df.set_index('time')

    out = {}
    # Now that we have the climate data, we need to find monthly extreme
    # values:
    out['tl_max'] = df['ttx'].groupby(df.index.month).max().values
    out['tl_min'] = df['ttx'].groupby(df.index.month).min().values
    out['ff_max'] = df['vex'].groupby(df.index.month).max().values
    out['td_max'] = df['tfx'].groupby(df.index.month).max().values
    out['td_min'] = df['tfx'].groupby(df.index.month).max().values
    out['rr_max'] = df['rsx'].groupby(df.index.month).max().values
    
    return out


if __name__ == '__main__':
    # TESTING:
    # weather = get_weather_data('innsbruck')
    climate = get_climate_data('innsbruck')
    print(climate)


