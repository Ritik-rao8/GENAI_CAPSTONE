# Version 1.0.1
# Minor documentation update for project submission

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from utils.preprocessing import merge_data
from utils.feature_engineering import create_time_features


st.set_page_config(page_title="Solar Forecasting Dashboard", layout="wide")

st.title("Solar Energy Forecasting Dashboard")
st.markdown("---")
# ---------------- SIDEBAR ---------------- #

st.sidebar.header("⚙️ Configuration")

data_option = st.sidebar.radio(
    "Select Dataset",
    ("Use Default Plant 1", "Upload Custom CSV")
)

df = None


if data_option == "Use Default Plant 1":
    df = merge_data()
else:
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

model_option = st.sidebar.selectbox(
    "Select Model",
    ("Linear Regression", "Random Forest", "Gradient Boosting")
)

train_button = st.sidebar.button("🚀 Train Model")

# Store model in session
if "model" not in st.session_state:
    st.session_state.model = None

# ---------------- MAIN ---------------- #
if df is None:
    st.info("Please select a dataset from the sidebar to begin.")
if df is not None:

    df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"], errors="coerce")
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

    required_columns = features + [target, "DATE_TIME"]

    missing_cols = [col for col in required_columns if col not in df.columns]

    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
        st.stop()

    tabs = st.tabs(["📘 About", "📂 Preview", "🚀 Train", "📊 Evaluate"])

    # ================= TAB 1: ABOUT ================= #
    with tabs[0]:

        st.subheader("Project Overview")

        st.markdown("""
        This project develops a **Machine Learning-based Solar Energy Forecasting System**
        to predict solar power generation (DC_POWER) using historical plant and weather data.

        ---
        ### 🎯 Objective
        To accurately forecast solar energy output for improved renewable energy planning
        and grid management.

        ---
        ### 🔍 Key Features
        - Data preprocessing and cleaning
        - Time-based feature engineering (hour, month, weekday)
        - Model training using:
            - Linear Regression
            - Random Forest
            - Gradient Boosting
        - Performance evaluation using:
            - MAE
            - RMSE
            - R² Score
        - Visualization of Actual vs Predicted output

        ---
        ### 📊 Input Features Used
        - Ambient Temperature
        - Module Temperature
        - Irradiation
        - Hour of Day
        - Month
        - Day of Week

        ---
        ### ⚡ Why This Matters
        Accurate solar forecasting helps in:
        - Grid stability
        - Energy scheduling
        - Renewable integration planning
        """)

    # ================= TAB 2: PREVIEW ================= #
    with tabs[1]:

        st.subheader("Dataset Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Target Variable", target)

        st.markdown("### Column Names")
        st.write(list(df.columns))

        st.markdown("### Data Preview")
        num_rows = st.slider("Rows to display", 5, 50, 10)
        st.dataframe(df.head(num_rows))

        st.markdown("### Summary Statistics")
        st.dataframe(df.describe())

    # ================= TAB 2: TRAIN ================= #
    with tabs[2]:

        X = df[features]
        y = df[target]

        split_index = int(len(df) * 0.8)

        X_train = X.iloc[:split_index]
        y_train = y.iloc[:split_index]

        if train_button:

            if model_option == "Linear Regression":
                model = LinearRegression()

            elif model_option == "Random Forest":
                model = RandomForestRegressor(
                    n_estimators=100,
                    max_depth=15,
                    random_state=42,
                    n_jobs=-1
                )

            elif model_option == "Gradient Boosting":
                model = GradientBoostingRegressor(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=5,
                    random_state=42
                )

            with st.spinner("Training model... Please wait"):
                model.fit(X_train, y_train)

            st.session_state.model = model

            st.success(f"{model_option} trained successfully!")

            st.subheader("📌 Model Details")

            test_size = len(df) - len(X_train)

            st.info(f"""
            Model Selected: {model_option}  
            Training Samples: {len(X_train)}  
            Testing Samples: {test_size}
            """)

    # ================= TAB 3: EVALUATE ================= #
    with tabs[3]:

        if st.session_state.model is not None:

            model = st.session_state.model

            X = df[features]
            y = df[target]

            split_index = int(len(df) * 0.8)

            X_test = X.iloc[split_index:]
            y_test = y.iloc[split_index:]

            predictions = model.predict(X_test)

            mae = mean_absolute_error(y_test, predictions)
            rmse = np.sqrt(mean_squared_error(y_test, predictions))
            r2 = r2_score(y_test, predictions)

            col1, col2, col3 = st.columns(3)
            col1.metric("MAE", round(mae, 2), help="Mean Absolute Error")
            col2.metric("RMSE", round(rmse, 2), help="Root Mean Squared Error")
            col3.metric("R² Score", round(r2, 4), help="Coefficient of Determination")

            st.markdown("### Actual vs Predicted")

            fig, ax = plt.subplots()
            ax.plot(y_test.values[:500], label="Actual")
            ax.plot(predictions[:500], label="Predicted")
            ax.legend()

            st.pyplot(fig)

        else:
            st.warning("Please train a model first.")
st.markdown("---")
st.caption("Solar Forecasting Dashboard | GENAI Capstone Project")