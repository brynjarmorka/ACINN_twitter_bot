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
    Compares weather to the climate and makes a message.
    If it cannot find any interesting data, it will return None.
    Parameters
    ----------
    weather : pandas DataFrame
        The data from the local weather station in a dataframe. 24h data
        Check out weather_variables.md to see its variables.
    climate : pandas DataFrome
        The local monthly climate based on a static file. From the past _____ years.
    Returns
    -------
    message : string or None
        The message to be posted on twitter. If it's None, no tweet should be posted.
    """

    # placeholder code:
    month = datetime.datetime.now().month
    time = str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute)

    w = weather["tl"].mean()
    c = climate["mean"][month]
    dif = round(w - c, 1)

    if dif > 0:
        dif = "+" + str(dif)
    w = round(w, 1)
    message = f"Last 24h mean temperature ({time}) is {w} deg. and differs from monthly climate values by {dif} deg."
    return message


def main():
    """Runs weather and climate comparison, makes a message and post to twitter."""
    station = "innsbruck"  # could also support "ellboegen", "obergurgl", "sattelberg", if we get climate data there.
    config = get_api_key()
    climate = get_climate_data(station)
    weather = get_weather_data(station)
    message = detect_anomaly(weather, climate)

    if message is not None:
        # TODO: remove the dummy_ for actually posting to Twitter:
        update_twitter(config, message)


if __name__ == "__main__":
    """Scheduler, i.e. running main() in an interval"""
    main()

    sys.exit()
