import pandas as pd


def create_time_features(df):
    df["hour"] = df["DATE_TIME"].dt.hour
    df["month"] = df["DATE_TIME"].dt.month
    df["day_of_week"] = df["DATE_TIME"].dt.dayofweek

    return df