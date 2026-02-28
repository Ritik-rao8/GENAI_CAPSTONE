import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from utils.preprocessing import merge_data
from utils.feature_engineering import create_time_features


def train_and_save_best_model():

    # Load and prepare data
    df = merge_data()
    df = create_time_features(df)
    df = df.sort_values("DATE_TIME")
    

    features = [
        "AMBIENT_TEMPERATURE",
        "MODULE_TEMPERATURE",
        "IRRADIATION",
        "hour",
        "month",
        "day_of_week"
    ]

    target = "DC_POWER"

    X = df[features]
    y = df[target]

    split_index = int(len(df) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
    }

    best_model = None
    best_r2 = -np.inf
    best_name = ""

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        r2 = r2_score(y_test, y_pred)

        print(f"{name} R2:", r2)

        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            best_name = name

    print("\nBest Model:", best_name)
    print("Best R2:", best_r2)

    # Create models folder if not exists
    import os
    os.makedirs("models", exist_ok=True)

    # Save best model
    joblib.dump(best_model, "models/plant1_model.pkl")

    print("\nModel saved successfully as models/plant1_model.pkl")