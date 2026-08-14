from pathlib import Path
import json

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

INPUT_FILE = Path("data/processed/singapore_monthly_arrivals.csv")
OUTPUT_FILE = Path("data/processed/arrival_forecast_backtest.csv")
REPORT_FILE = Path("data/processed/arrival_forecast_model_report.json")

FEATURE_COLUMNS = [
    "trend_index",
    "month_sin",
    "month_cos",
    "lag_1",
    "lag_3",
    "lag_12",
    "rolling_mean_3",
]


def wape(actual: pd.Series, predicted: pd.Series) -> float:
    """Weighted Absolute Percentage Error."""
    denominator = actual.abs().sum()

    if denominator == 0:
        return float("nan")

    return float((actual - predicted).abs().sum() / denominator * 100)


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create time-series features using only past official arrivals."""
    data = df.copy().sort_values("date").reset_index(drop=True)

    data["trend_index"] = np.arange(len(data))
    data["month_sin"] = np.sin(2 * np.pi * data["month"] / 12)
    data["month_cos"] = np.cos(2 * np.pi * data["month"] / 12)

    data["lag_1"] = data["arrivals"].shift(1)
    data["lag_3"] = data["arrivals"].shift(3)
    data["lag_12"] = data["arrivals"].shift(12)

    data["rolling_mean_3"] = (
        data["arrivals"]
        .shift(1)
        .rolling(window=3)
        .mean()
    )

    return data.dropna(subset=FEATURE_COLUMNS).copy()


def calculate_metrics(actual: pd.Series, predicted: pd.Series) -> dict:
    """Calculate understandable forecast-error measures."""
    return {
        "mae": round(float(mean_absolute_error(actual, predicted)), 2),
        "rmse": round(float(np.sqrt(mean_squared_error(actual, predicted))), 2),
        "wape_pct": round(wape(actual, predicted), 2),
    }


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "Processed arrivals file not found. Run the arrivals pipeline first."
        )

    df = pd.read_csv(INPUT_FILE, parse_dates=["date"])

    required_columns = {"date", "arrivals", "month"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_columns)}"
        )

    model_df = create_features(df)

    # Hold out the latest six months. The model never sees these during training.
    test_months = 6
    train_df = model_df.iloc[:-test_months].copy()
    test_df = model_df.iloc[-test_months:].copy()

    if len(train_df) < 36:
        raise ValueError("Not enough training data after feature creation.")

    # Baseline: same month in the previous year.
    test_df["baseline_prediction"] = test_df["lag_12"]

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(train_df[FEATURE_COLUMNS], train_df["arrivals"])

    test_df["ml_prediction"] = model.predict(test_df[FEATURE_COLUMNS])

    baseline_metrics = calculate_metrics(
        test_df["arrivals"],
        test_df["baseline_prediction"],
    )

    ml_metrics = calculate_metrics(
        test_df["arrivals"],
        test_df["ml_prediction"],
    )

    preferred_method = (
        "random_forest"
        if ml_metrics["wape_pct"] < baseline_metrics["wape_pct"]
        else "seasonal_naive_baseline"
    )

    output_df = test_df[
        [
            "date",
            "arrivals",
            "baseline_prediction",
            "ml_prediction",
        ]
    ].rename(columns={"arrivals": "actual_arrivals"})

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(OUTPUT_FILE, index=False)

    feature_importance = dict(
        sorted(
            zip(FEATURE_COLUMNS, model.feature_importances_),
            key=lambda item: item[1],
            reverse=True,
        )
    )

    report = {
        "dataset": "Singapore monthly international visitor arrivals",
        "source_table_id": "M550001",
        "source_agency": "Singapore Tourism Board via SingStat",
        "task": "Six-month held-out backtest of monthly arrival forecasts",
        "training_end_date": str(train_df["date"].max().date()),
        "test_start_date": str(test_df["date"].min().date()),
        "test_end_date": str(test_df["date"].max().date()),
        "test_months": test_months,
        "baseline_method": "Same month in previous year",
        "machine_learning_method": "Random forest regression",
        "baseline_metrics": baseline_metrics,
        "machine_learning_metrics": ml_metrics,
        "preferred_method": preferred_method,
        "feature_importance": {
            name: round(float(value), 4)
            for name, value in feature_importance.items()
        },
        "limitations": [
            "Forecasts use historical official arrivals and calendar features only.",
            "Forecasts do not establish causes or policy effects.",
            "COVID-era disruption can reduce the reliability of normal seasonal patterns.",
            "This model is exploratory and not an official tourism forecast.",
        ],
    }

    with REPORT_FILE.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print("Forecast backtest created:", OUTPUT_FILE)
    print("Model report created:", REPORT_FILE)
    print("\nBaseline metrics:")
    print(json.dumps(baseline_metrics, indent=2))
    print("\nMachine-learning metrics:")
    print(json.dumps(ml_metrics, indent=2))
    print(f"\nPreferred method: {preferred_method}")


if __name__ == "__main__":
    main()