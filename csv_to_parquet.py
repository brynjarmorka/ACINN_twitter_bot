import pandas as pd


def get_climate_data(station="innsbruck"):
    """
    Read the csv, filter on innsbruck and then save the data into a parquet file.
    This code creates the parquet file, which is compressed as gzip.
    The gzip file will be on github, and thus this function only needs to run if we change the csv file.

    Funfact: the .gzip file is half the size of the original .csv file.

    OBS: You need wither 'pyarrow' or 'fastparqued' to run this one.
    """
    df = pd.read_csv("./2mtemp_19900101_20200101.csv")
    # some formatting
    df.index = pd.to_datetime(df["time"], format="%Y-%m-%d")
    # select location
    if station == "innsbruck":
        stat_id = 11803.0
    else:
        raise ValueError(f"station {station} not implemented")

    df_ibk = df[df["station"] == stat_id]  # filter out other stations

    df_ibk.to_parquet("df_ibk.parquet.gzip", compression="gzip")
