#!/usr/bin/env python
'''This is the main part of the twitter bot.
'''
import tweepy
from get_data import get_weather_data, get_climate_data
import time
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

    if True:
        message = 'asdf'
    else:
        message = None

    return message


def main():
    climate = get_climate_data('innsbruck')
    config = get_config()

    while True:
        weather = get_weather_data('innsbruck')
        message = detect_anomaly(weather, climate)
        
        if message is not None:
            # TODO: remove the dummy_:
            dummy_update_twitter(config, message)
        print('Waiting...')
        time.sleep(600)
    


if __name__ == '__main__':
    main()
