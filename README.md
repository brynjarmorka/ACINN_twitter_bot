This is a twitter bot for interesting weather events from ACINN. Forked from 
https://github.com/stefanstoeckl/ACINN_twitter_bot.

# Usage:
- add twitter credentials (requires developer account and a created twitter app) to a file called "config.ini" 
- run "twitter_bot.py" using Python and keep it running!

# Requirements:
- Python
- numpy
- pandas
- tweepy 
- configparser

Please use black to follow to PEP8

# The bot
- Loads the past 24h data from https://acinn-data.uibk.ac.at/innsbruck/1
- Checks if there are deviations from the climate on a certain threshold
- Tweets the deviation in a nice way

# Further possible improvements
- Update the climatology comparison file for Innsbruck