This is a twitter bot for interesting weather events from ACINN. Forked from 
https://github.com/stefanstoeckl/ACINN_twitter_bot.

# The account looks like that:

![](twitter_profile.png)

# And it can be embeded like this:


<div class="card">
  <div class="widget-header">
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns" width="28" height="24" viewBox="0 0 20 20" version="1.1">
      <g><path fill="#55acee" d="M19.53 5.13C19.54 5.25 19.54 5.44 19.54 5.69 19.54 6.85 19.37 8.01 19.03 9.17 18.69 10.32 18.18 11.43 17.48 12.5 16.79 13.56 15.97 14.5 15.01 15.31 14.06 16.13 12.91 16.78 11.56 17.27 10.21 17.76 8.77 18 7.23 18 4.81 18 2.6 17.35 0.59 16.06 0.9 16.09 1.25 16.11 1.63 16.11 3.64 16.11 5.43 15.5 7 14.26 6.07 14.25 5.23 13.96 4.49 13.4 3.75 12.84 3.24 12.13 2.96 11.26 3.25 11.31 3.53 11.33 3.78 11.33 4.16 11.33 4.54 11.28 4.92 11.18 3.92 10.98 3.09 10.48 2.43 9.69 1.77 8.9 1.45 7.98 1.45 6.94L1.45 6.88C2.05 7.22 2.71 7.41 3.4 7.43 2.81 7.04 2.34 6.53 2 5.89 1.65 5.26 1.47 4.57 1.47 3.83 1.47 3.04 1.67 2.32 2.06 1.65 3.14 2.98 4.46 4.04 6.01 4.84 7.56 5.64 9.21 6.08 10.98 6.17 10.91 5.83 10.88 5.5 10.88 5.18 10.88 3.99 11.3 2.97 12.14 2.12 12.98 1.28 14 0.86 15.2 0.86 16.45 0.86 17.5 1.31 18.36 2.22 19.33 2.04 20.25 1.69 21.11 1.18 20.78 2.21 20.14 3 19.21 3.56 20.04 3.47 20.87 3.25 21.7 2.89 21.1 3.77 20.38 4.51 19.53 5.13Z"/></g>
    </svg>
    <h1>Get the scoop on Twitter</h1>
  </div>
  
    <!-- Widget #1 User Timeline -->
  <div class="widget">
      <a class="twitter-timeline" href="https://twitter.com/DunkinDonuts" data-widget-id="727935311226015744" data-chrome="nofooter noborders" data-tweet-limit="1" data-aria-polite="assertive">Tweets by @DunkinDonuts</a><script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
  </div>

  <!-- Widget #2 Search Timeline -->
  <div class="widget">
      <a class="twitter-timeline" href="https://twitter.com/hashtag/yext" data-widget-id="606644267499560961" data-chrome="nofooter noborders" data-tweet-limit="1" data-aria-polite="assertive">#yext Tweets</a><script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
  </div>
  
  <!-- Widget #3 Favorite Tweets Timeline -->
  <div class="widget">
      <a class="twitter-timeline" href="https://twitter.com/yext/favorites" data-widget-id="606917456163151872" data-chrome="nofooter noborders" data-tweet-limit="1" data-aria-polite="assertive">Favorite Tweets by @yext</a><script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
  </div>
  <button class="tweet-button">Send us a tweet!</button>
</div>

</a>


# Usage:
- add twitter credentials (requires developer account and a created twitter app) to a file called "config.ini" 
- run "twitter_bot.py".

# Requirements:
- Python
- numpy
- pandas
- tweepy 
- configparser
- pyarrow

Please use black to follow to PEP8

# The bot
- Loads the past 24h data from https://acinn-data.uibk.ac.at/innsbruck/1
- If there is any interesting data to be reported, a tweet is issued:
    - Interesting data can be:
        - last 24h mean temperature above 95th percentile or below 5th percentile
        - Special cases for extremes out of climatology (24htemp>tmax or 24htemp<tmin)
        - Precipitation above some threshold (for now hardcoded to 5mm/24h)
- If noticeable temperature and precipitation occur both during the last 24h a single tweet containing both data is published
- Needs to be put in some scheduler. In our case we use crontab, from linux. It is meant to run once a day, preferebly in the evening. 

# Further possible improvements
- Update the climatology comparison file for Innsbruck

# Improvements form last version:
- Crontab scheduler avoids having always-runing python session in the background.
- Weather data is compared to climate in case of temperature.   

# Weaknesses:
- Climatology is not updated automatically. The temperature distribution is going to change in the folowing years.

# Data sources:
- 10-min data from ACINN weather station. see data_license.txt for weather data from ACINN
- Daily 2m temperature mean data from 01011990-01012020 https://dataset.api.hub.zamg.ac.at/app/station-new/historical/klima-v1-1d?anonymous=true
