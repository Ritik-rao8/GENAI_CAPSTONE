import pandas as pd


def merge_data():
    # Load data
    generation_df = pd.read_csv("data/Plant_1_Generation_Data.csv")
    weather_df = pd.read_csv("data/Plant_1_Weather_Sensor_Data.csv")

    # Convert datetime
    generation_df["DATE_TIME"] = pd.to_datetime(generation_df["DATE_TIME"],format="%d-%m-%Y %H:%M")
    weather_df["DATE_TIME"] = pd.to_datetime(weather_df["DATE_TIME"],format="%Y-%m-%d %H:%M:%S")

    # Merge datasets
    plant1_df = pd.merge(
        generation_df,
        weather_df,
        on=["DATE_TIME", "PLANT_ID"],
        how="inner"
    )

    # Drop duplicate source columns
    plant1_df = plant1_df.drop(
        columns=["SOURCE_KEY_x", "SOURCE_KEY_y"],
        errors="ignore"
    )

    return plant1_df

df = merge_data()
print(df.shape)
print(df.columns)