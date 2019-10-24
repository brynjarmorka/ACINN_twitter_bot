#!/usr/bin/env python
'''This is the main part of the twitter bot.
'''
import tweepy
from get_data import get_weather_data, get_climate_data
import time
import sched
import pandas as pd
import sys
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


def update_twitter(config, message):
    '''This then updates twitter
    '''
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(config['api_key'], config['api_secret_key'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])
    
    # Create API object
    api = tweepy.API(auth)
    
    # Create a tweet
    api.update_status(message)


def dummy_update_twitter(config, message):
    '''To print what would normally be tweeted for testing.
    '''
    print('This would have been sent: ', message)
    print(config)


def get_config():
    '''Read config from config.ini
    '''
    ini = ConfigParser()
    ini.read('config.ini')
    config = {}
    for key in ['api_key', 'api_secret_key', 'access_token', 
                'access_token_secret']:
        config[key] = ini.get('twitter_credentials', key)

    return config


def detect_anomaly(weather, climate):
    '''Find out if the current weather is special
    TODO: actually implement the logic!
    '''
    message = ''
    month = time.now().month()
    m = month - 1  # month index
    for var in climate.keys():
        # TODO: run the logic: first aggregate the last day, then check if
        # some threshold is exceeded.
        # Example message: 
        message += ('Todays maximum temperature of '
                    + '{:.1f}'.format(weather.iloc[-1, :['tl']]) 
                    + '°C was the highest recorded for this station!')
    else:
        message = None

    return message


def main(config, climate):
    weather = get_weather_data('innsbruck')
    message = detect_anomaly(weather, climate)
   
    if message is not None:
        # TODO: remove the dummy_:
        dummy_update_twitter(config, message)


if __name__ == '__main__':
    climate = get_climate_data('innsbruck')
    config = get_config()
    scheduler = sched.scheduler(time.time, time.sleep)
    # Now we create a list of timestamps and schedule an execution of main()
    # every evening:
    date_range = pd.date_range(pd.to_datetime('2019-10-24 21:00'), 
                               periods=10000, 
                               tz='Europe/Vienna').to_pydatetime().tolist()
    timestamps = [d.timestamp() for d in date_range]
    for date in timestamps:
        scheduler.enterabs(date, 1, main, (config, climate))
    scheduler.run()
