#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the main part of the twitter bot.
"""
import tweepy
import sys
import os.path
from configparser import ConfigParser
from get_data import get_weather_data, get_climate_data
import datetime
from pathlib import Path


def update_twitter(config, message):
    """This actually updates twitter, if the config.ini have the valid keys.
    
    Parameters
    ----------
    config : dict
        Dictionary with api-keys and access token to post to Twitter
    message : string
        String to be tweeted, here just printed to the console
    """
    # Authentificate
    client = tweepy.Client(
        consumer_key=config["api_key"],
        consumer_secret=config["api_secret_key"],
        access_token=config["access_token"],
        access_token_secret=config["access_token_secret"],
    )

    # Create Tweet

    # The app and the corresponding credentials must have the Write permission

    # Check the App permissions section of the Settings tab of your app, under the
    # Twitter Developer Portal Projects & Apps page at
    # https://developer.twitter.com/en/portal/projects-and-apps

    # Make sure to reauthorize your app / regenerate your access token and secret
    # after setting the Write permission

    response = client.create_tweet(text=message)
    print(f'https://twitter.com/user/status/{response.data["id"]}')


def dummy_update_twitter(config, message):
    """Prints to the console the generated message. Also prints the config.
    Parameters
    ----------
    config : dict
        Dictionary with api-keys and access token to post to Twitter
    message : string
        String to be tweeted, here just printed to the console
    """
    print(f"This would have been tweeted: \n{message}\n\nThis is the config:\n{config}")


def get_api_key():
    """Read API-key / access token file named ".twitter_bot_API.ini" which should be in your HOME dir.
    Exits the script if there is no file
    Returns
    ----------
    config : dict
        Dictionary with api-keys and access token to post to Twitter
    """

    # Accessing the hidden file in the HOME dir of the user:
    api_key_path = Path("~/.twitter_bot_API.ini")
    full_path = os.path.expanduser(api_key_path)
    if not os.path.exists(full_path):
        print(
            f"FileNotFoundError: '.twitter_bot_API.ini' must be your HOME dir, {full_path}"
        )
        sys.exit()
    else:
        ini = ConfigParser()
        ini.read(full_path)
        api_key_dict = {}
        for key in ["api_key", "api_secret_key", "access_token", "access_token_secret"]:
            api_key_dict[key] = ini.get("twitter_credentials", key)
        return api_key_dict


def detect_anomaly(weather, climate):
    """
    Compares weather to the climate.
    If it cannot find any interesting data, it will return Nones.
    Parameters
    ----------
    weather : pandas DataFrame
        The data from the local weather station in a dataframe. 24h data
        Check out weather_variables.md to see its variables.
    climate : pandas DataFrome
        The local monthly climate based on a static file. From the past _____ years.
    Returns
    -------
    message : list with interesting data.
        The data that is to be used then by the message generator.
    """
    # Initialize output list
    totweet = {'Temperature': None, 'Extreme': False,'Precipitation': None}
    
    # find todays month:
    month = datetime.datetime.today().month
    #time = str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute)

    # Climate
    c = climate.iloc[climate.index == month]

    # Temperature
    wtemp = weather.tl.mean()
    
    ## Exceptional event?
    if wtemp > float(c.p95) or wtemp < float(c.p05):
        # we have an anomalous temperature! 
        dif = round(wtemp - float(c['mean']), 1)
        totweet['Temperature'] = [round(wtemp, 1), dif]
    ## Never-before event?
    if wtemp > float(c['max']) or wtemp < float(c['min']):
        # we have an extreme temperature! 
        totweet['extreme'] = True
    
    # Precipitation
    wppt = weather.rr.sum()/6 # ppt intensity each 10 minutes, translated to actual ppt.
    if wppt > 5: # 5mm/24 h threshold
        totweet['Precipitaiton'] = str(round(wppt, 1))

    return totweet

def text_generator(totweet):
    """
    Function that generates the message that is going to be tweeted.

    Parameters
    ----------
    totweet : dictionary
        dictionary with the keys: 'Temperature' [temperature, anomaly] 
        [float or None, float or None],, 'Extreme' bool, 'Precipitaiton': float or None.

    Returns
    -------
    Message (s) to be tweeted.

    """
    message = None
    # check temperature
    if totweet['Temperature'] is not None:
        if totweet['Temperature'] > 0 and totweet['Extreme']:
            emoji = '\U0000203C\U0001F975\U0001F975\U0000203C'
            txt = 'an extreme'
        
        if totweet['Temperature'] > 0 and not totweet['Extreme']:
            emoji = '\U0001F975'
            txt = 'an important'
            
        if totweet['Temperature'] < 0 and totweet['Extreme']:
            emoji = '\U0000203C\U0001F976\U0001F976\U0000203C'
            txt = 'an extreme'
            
        if totweet['Temperature'] < 0 and not totweet['Extreme']:
            emoji = '\U0001F976'
            txt = 'an important'
            
        message = f'{emoji} In the last 24h we had {txt} anomalous temperature of {totweet["Temperature"][0]}ºC, {totweet["Temperature"][1]}ºC away from the monthly mean. {emoji}'
        
    # check precipitation
    # add ppt message
    if totweet['Precipitation'] is not None and message is not None:
        message = message + f'\n \U0001F4A7 And and a considerable precipitation accumulation of {totweet["Precipitation"]}mm \U0001F4A7'
    # create ppt message
    if totweet['Precipitation'] is not None and message is None:
        message = f'\U0001F4A7 In the last 24h we had a considerable precipitation accumulation of {totweet["Precipitaiton"]}mm \U0001F4A7'

    return message

def main():
    """Runs weather and climate comparison, makes a message and post to twitter."""
    station = "innsbruck"  # could also support "ellboegen", "obergurgl", "sattelberg", if we get climate data there.
    config = get_api_key()
    climate = get_climate_data(station)
    weather = get_weather_data(station)
    totweet = detect_anomaly(weather, climate)
    message = text_generator(totweet)

    if message is not None:
        # TODO: remove the dummy_ for actually posting to Twitter:
        #update_twitter(config, message)
        dummy_update_twitter(config, message)


if __name__ == "__main__":
    """When run from terminal all the workflow is lounched and if anomaly is 
    found a tweet is produced.
    """
    main()
    
    sys.exit()
