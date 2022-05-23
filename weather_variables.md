# The weather df from the station have the following variables

check out https://acinn-data.uibk.ac.at/innsbruck/1

column 'time' is added in get_weather_data in get_data.py

- rr
  - rain? [mm?]
  - float64
  - invalid value: -599.xx
- dd
  - wind direction [°]
  - float64
  - invalid value: ?
- tp
    - what is it?
    - float64
    - invalid value: -99.9
- p
  - pressure [mBar]
  - float64
  - invalid value: ?
- tl
  - temperature [°C]
  - float64
  - invalid value: -99.9
- so
  - insolation? [not in W/m**2 ?]
  - float64
  - invalid value: ?
- ff
  - wind speed [m/s]
  - float64
  - invalid value: ?
- datumsec
  - seconds since 1970 [s]
  - float64
- time
  - time every 10 minutes
  - ex: "Timestamp('2022-05-22 08:50:00')"
  - object, pandas._libs.tslibs.timestamps.Timestamp