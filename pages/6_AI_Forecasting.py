from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="AI Forecasting | Tourism Observatory",
    page_icon="🤖",
    layout="wide",
)

BACKTEST_FILE = Path("data/processed/arrival_forecast_backtest.csv")
REPORT_FILE = Path("data/processed/arrival_forecast_model_report.json")


@st.cache_data
def load_backtest() -> pd.DataFrame:
    if not BACKTEST_FILE.exists():
        raise FileNotFoundError(
            "Forecast backtest file not found. Run: "
            "python src/ml/train_arrival_forecast.py"
        )

    return pd.read_csv(BACKTEST_FILE, parse_dates=["date"])


@st.cache_data
def load_model_report() -> dict:
    if not REPORT_FILE.exists():
        raise FileNotFoundError(
            "Model report file not found. Run: "
            "python src/ml/train_arrival_forecast.py"
        )

    with REPORT_FILE.open(encoding="utf-8") as file:
        return json.load(file)


backtest_df = load_backtest()
report = load_model_report()

baseline_metrics = report["baseline_metrics"]
ml_metrics = report["machine_learning_metrics"]
preferred_method = report["preferred_method"]

st.title("AI Forecasting Model Evaluation")

st.markdown(
    """
This page evaluates two methods for forecasting Singapore monthly international
visitor arrivals using official historical data.

The model is tested on six months it did not see during training. This is called
a **held-out backtest**. It is an evaluation of forecasting accuracy, not an
official tourism forecast or a claim about what causes visitor arrivals.
"""
)

st.caption(
    "Evidence label: Model-derived signal | "
    "Input data: Singapore Tourism Board via SingStat, Table M550001"
)

st.divider()

st.header("Methods compared")

left, right = st.columns(2)

with left:
    st.info("Baseline: Same month last year")
    st.caption(
        "A simple benchmark that predicts each month using the arrival count "
        "from the same month in the previous year."
    )

with right:
    st.success("Machine learning: Random forest")
    st.caption(
        "Uses past official arrivals, recent trends, 12-month lag values, "
        "and calendar seasonality features."
    )

st.divider()

st.header("Held-out test results")

metric_1, metric_2, metric_3 = st.columns(3)

with metric_1:
    st.metric(
        label="Preferred method",
        value=(
            "Random forest"
            if preferred_method == "random_forest"
            else "Same month last year"
        ),
        help="The method with the lower WAPE on the held-out test period.",
    )

with metric_2:
    st.metric(
        label="Baseline WAPE",
        value=f"{baseline_metrics['wape_pct']:.2f}%",
        help="Lower is better. WAPE measures total absolute error relative to total actual arrivals.",
    )

with metric_3:
    st.metric(
        label="Machine-learning WAPE",
        value=f"{ml_metrics['wape_pct']:.2f}%",
        help="Lower is better. This is the random-forest model's held-out test error.",
    )

comparison_df = pd.DataFrame(
    {
        "Method": ["Same month last year", "Random forest"],
        "MAE": [baseline_metrics["mae"], ml_metrics["mae"]],
        "RMSE": [baseline_metrics["rmse"], ml_metrics["rmse"]],
        "WAPE (%)": [
            baseline_metrics["wape_pct"],
            ml_metrics["wape_pct"],
        ],
    }
)

st.dataframe(comparison_df, use_container_width=True, hide_index=True)

st.divider()

st.header("Actual arrivals versus model predictions")

chart = go.Figure()

chart.add_trace(
    go.Scatter(
        x=backtest_df["date"],
        y=backtest_df["actual_arrivals"],
        mode="lines+markers",
        name="Actual official arrivals",
        line=dict(color="#0F766E", width=3),
    )
)

chart.add_trace(
    go.Scatter(
        x=backtest_df["date"],
        y=backtest_df["baseline_prediction"],
        mode="lines+markers",
        name="Baseline prediction",
        line=dict(color="#F59E0B", dash="dash"),
    )
)

chart.add_trace(
    go.Scatter(
        x=backtest_df["date"],
        y=backtest_df["ml_prediction"],
        mode="lines+markers",
        name="Random forest prediction",
        line=dict(color="#2563EB", dash="dot"),
    )
)

chart.update_layout(
    title="Six-Month Held-Out Backtest",
    title_x=0,
    xaxis_title="Month",
    yaxis_title="International visitor arrivals",
    yaxis_tickformat=",",
    hovermode="x unified",
    margin=dict(l=10, r=10, t=60, b=10),
)

st.plotly_chart(chart, use_container_width=True)

st.divider()

st.header("Feature importance")

importance_df = pd.DataFrame(
    {
        "Feature": list(report["feature_importance"].keys()),
        "Importance": list(report["feature_importance"].values()),
    }
).sort_values("Importance")

importance_chart = px.bar(
    importance_df,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Random Forest Feature Importance",
    color="Importance",
    color_continuous_scale="Blues",
)

importance_chart.update_layout(
    title_x=0,
    coloraxis_showscale=False,
    margin=dict(l=10, r=10, t=60, b=10),
)

st.plotly_chart(importance_chart, use_container_width=True)

st.warning(
    "Interpret carefully: this model uses historical arrival patterns only. "
    "It cannot establish causes, measure visitor behaviour, predict policy "
    "impact, or replace official tourism forecasts. COVID-era disruption can "
    "reduce the reliability of normal seasonal patterns."
)

with st.expander("Model limitations and evaluation details"):
    st.markdown(
        f"""
**Training data ended:** {report["training_end_date"]}  
**Held-out test period:** {report["test_start_date"]} to {report["test_end_date"]}  
**Test months:** {report["test_months"]}  
**Baseline:** {report["baseline_method"]}  
**Machine-learning method:** {report["machine_learning_method"]}

A lower WAPE, MAE, or RMSE indicates lower forecast error. The preferred method
is selected only from this held-out test comparison.
"""
    )