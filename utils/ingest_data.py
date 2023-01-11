import pandas as pd
import os
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError
import datetime

from path_mgmt import add_corteva_to_path
add_corteva_to_path()

from corteva_app.app import db
from corteva_app.database.models import Weather, Yield, WeatherStats
from corteva_app.database.mgmt import engine, db_session

def ingest_weather(dir_path: str) -> None:
    """
    dir_path: relative or absolute path to the directory containing weather .txt files

    raises: general Exception if unknown behavior occurs with sqlalchemy
    """
    os.chdir(dir_path)
    # add dataframes into a giant list so we can use .concat to join them all into a single dataframe at once
    # this could be memory intensive, but significantly faster than using .append in a for loop

    dfs: List[pd.DataFrame] = []

    for file in os.listdir():
        df_weather_one_station = pd.read_csv(file, sep="\t", header=None)
        # rename columns so concat can match them up
        df_weather_one_station.columns = ["date", "max_temp_tenth_c", "min_temp_tenth_c", "precip_tenth_mm"]
        # station id is not contained within files so we will label it manually
        station_id = file.split(".")[0]
        df_weather_one_station["station_id"] = station_id
        dfs.append(df_weather_one_station)

    df_weather = pd.concat(dfs)
    # transform temps into degrees C and precip into centimeters following our data model
    df_weather["max_temp_c"] = df_weather["max_temp_tenth_c"] / 10
    df_weather["min_temp_c"] = df_weather["min_temp_tenth_c"] / 10
    df_weather["precip_cm"] = df_weather["precip_tenth_mm"] / 100

    # interpret date string as a datetime object
    df_weather["date"] = pd.to_datetime(df_weather["date"], format="%Y%m%d")

    # drop extra columns
    df_weather.drop(columns=["max_temp_tenth_c", "min_temp_tenth_c", "precip_tenth_mm"], inplace=True)
    # rename cleaned columns to match our database column names
    df_weather.rename(columns={
        "max_temp_c": "max_temp",
        "min_temp_c": "min_temp",
        "precip_cm": "precip"
    }, inplace=True)

    write_to_postgres(df=df_weather, table_name="weather", table_model=Weather)


def ingest_yield(dir_path: str) -> None:
    """
    dir_path: relative or absolute path to the directory containing yield .txt file
    """
    os.chdir(dir_path)

    df_yield = pd.read_csv(os.listdir()[0], sep="\t", header=None)
    df_yield.columns = ["year", "total_grain_yield"]

    write_to_postgres(df=df_yield, table_name="yield", table_model=Yield)


def write_to_postgres(df: pd.DataFrame, table_name: str, table_model: db.Model) -> None:
    """
    df: clean dataframe ready for ingestion into the postgres table
    table_name: name of the postgres table
    table_model: model object that will be used to count number of records after ingestion is complete
    """
    start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{table_name} ingestion start: {start}")

    # write cleaned data into our database
    # note - this will error if a single duplicate is detected... I don't know of a way to use INSERT IGNORE instead of just INSERT with the pandas API

    try:
        df.to_sql(name=table_name, con=engine, if_exists="append", index=False)
        num_rows = db_session.query(table_model).count()
        print(f"Inserted {num_rows} rows")
    except IntegrityError:
        print(f"Duplicate rows detected in {table_name} table - stopping ingestion")
        print(f"Inserted 0 rows into {table_name} table")
    finally:
        end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{table_name} ingestion end: {end}")
        num_rows = db_session.query(table_model).count()
        print(f"There are currently {num_rows} rows in the {table_name} table\n")


if __name__ == "__main__":
    ingest_weather("../wx_data")
    ingest_yield("../yld_data")