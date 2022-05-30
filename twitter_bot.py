#!/usr/bin/env python
"""
This is the main part of the twitter bot.
"""
import tweepy
import sys
import os.path
from configparser import ConfigParser
from get_data import get_weather_data, get_climate_data


def update_twitter(config, message):
    """This actually updates twitter, if the config.ini have the valid keys.

    Parameters
    ----------
    config : dict
        Dictionary with api-keys and access token to post to Twitter
    message : string
        String to be tweeted, here just printed to the console
    """
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(config["api_key"], config["api_secret_key"])
    auth.set_access_token(config["access_token"], config["access_token_secret"])

    api = tweepy.API(auth)  # Create API object
    api.update_status(message)  # Create a tweet


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


def get_config():
    """Read config from config.ini. User must have config.ini in the same dir as twitter_bot.py.
    Exits the script if there is no config.ini

    Returns
    ----------
    config : dict
        Dictionary with api-keys and access token to post to Twitter
    """
    # I think this works, not sure if it is good practice.
    # It will terminate the script completely.
    if not os.path.exists("./config.ini"):
        print("FileNotFoundError: config.ini must be the same dir as twitter_bot.py")
        sys.exit()
    else:
        ini = ConfigParser()
        ini.read("config.ini")
        config = {}
        for key in ["api_key", "api_secret_key", "access_token", "access_token_secret"]:
            config[key] = ini.get("twitter_credentials", key)
        return config


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

    # Getting the average T for the past day
    weather_stats = {
        "mean": weather["tl"].mean(),
        "max": weather["tl"].max(),
        "min": weather["tl"].min(),
        # TODO: handle NaN-values in 'tl', which are set to -99.9
    }

    # compare to df climate with ["mean", "p95", "p05"] and months as index [1,2, .. 12]
    this_month = weather["time"][0].month
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    # if weather_stats["max"] >= climate["p95"][this_month]:
    if weather_stats["max"] >= climate["p95"][this_month]:
        message = (
            f"The maximum temperature the past day in Innsbruck at {weather_stats['max']}°C is in the 95% quantile"
            f" for {months[this_month]}."
        )
        return message

    # if there are no interesting data, return None
    else:
        return None


def main():
    """Runs weather and climate comparison, makes a message and post to twitter."""
    station = "innsbruck"  # could also support "ellboegen", "obergurgl", "sattelberg", if we get climate data there.
    config = get_config()
    climate = get_climate_data(station)
    weather = get_weather_data(station)
    message = detect_anomaly(weather, climate)

    if message is not None:
        # TODO: remove the dummy_ for actually posting to Twitter:
        dummy_update_twitter(config, message)


if __name__ == "__main__":
    """Scheduler, i.e. running main() in an interval"""
    main()

    sys.exit()

    # # # # # # Below is old code for a scheduled run
    #
    # # NOTE: the following schedules the script to run every day at 21:00 Vienna
    # # time.
    # scheduler = sched.scheduler(time.time, time.sleep)
    # # Now we create a list of timestamps and schedule an execution of main()
    # # every evening:
    # date_range = (
    #     pd.date_range(
    #         pd.to_datetime("2019-10-24 21:00"), periods=10000, tz="Europe/Vienna"
    #     )
    #     .to_pydatetime()
    #     .tolist()
    # )
    # timestamps = [d.timestamp() for d in date_range]
    # for date in timestamps:
    #     scheduler.enterabs(date, 1, main, (config, climate))
    # scheduler.run()
