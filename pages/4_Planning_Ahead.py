from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st



BACKTEST_FILE = Path("data/processed/arrival_forecast_backtest.csv")
REPORT_FILE = Path("data/processed/arrival_forecast_model_report.json")


@st.cache_data
def load_backtest() -> pd.DataFrame:
    """Load the six-month model evaluation results."""
    if not BACKTEST_FILE.exists():
        raise FileNotFoundError(
            "Forecast backtest file not found. Run: "
            "python src/ml/train_arrival_forecast.py"
        )

    return pd.read_csv(BACKTEST_FILE, parse_dates=["date"])


@st.cache_data
def load_model_report() -> dict:
    """Load the saved model-evaluation report."""
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

st.markdown(
    """
    <style>
        .question-label {
            color: #0F766E;
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .step-card {
            background-color: rgba(15, 118, 110, 0.10);
            border-left: 4px solid #0F766E;
            border-radius: 8px;
            padding: 1rem;
            min-height: 145px;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="question-label">The planning question</p>',
    unsafe_allow_html=True,
)

st.title("Can data help a destination prepare for changing visitor demand?")

st.subheader(
    "Yes—but a good planning tool must be tested honestly before it is trusted."
)

st.write(
    """
This page tests whether past official visitor-arrival patterns can estimate
arrivals in months the methods have not seen before. It is a planning exercise,
not an official forecast and not a judgement about visitors.
"""
)

st.info(
    "This project estimates monthly visitor-arrival demand only. It cannot "
    "identify individual behaviour, explain why people travel, prove crowding, "
    "or decide who should be allowed to visit."
)

st.divider()

st.markdown(
    '<p class="question-label">How we tested it</p>',
    unsafe_allow_html=True,
)
st.header("We made the methods prove themselves")

step_1, step_2, step_3, step_4 = st.columns(4)

with step_1:
    st.markdown(
        """
        <div class="step-card">
        <h4>1. Start with official data</h4>
        <p>We used monthly Singapore visitor-arrival data published by STB through SingStat.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with step_2:
    st.markdown(
        """
        <div class="step-card">
        <h4>2. Hide six known months</h4>
        <p>The methods were not allowed to see the most recent six months before testing.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with step_3:
    st.markdown(
        """
        <div class="step-card">
        <h4>3. Compare two approaches</h4>
        <p>We compared a simple seasonal estimate with a Random Forest AI model.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with step_4:
    st.markdown(
        """
        <div class="step-card">
        <h4>4. Keep the more accurate method</h4>
        <p>We selected the method with lower error on the unseen months.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    '<p class="question-label">What did we learn?</p>',
    unsafe_allow_html=True,
)
st.header("The simpler method performed better in this test")

left_metric, right_metric = st.columns(2)

with left_metric:
    st.metric(
        label="Same month last year",
        value=f"{baseline_metrics['wape_pct']:.2f}% error",
        help=(
            "This method estimates a month using the arrival count from the "
            "same month in the previous year. Lower error is better."
        ),
    )

with right_metric:
    st.metric(
        label="Random Forest AI model",
        value=f"{ml_metrics['wape_pct']:.2f}% error",
        help=(
            "This model used recent arrival patterns, earlier months, and "
            "calendar seasonality. Lower error is better."
        ),
    )

st.success(
    "Responsible AI decision: the project currently prefers the simpler "
    "'same month last year' method because it was more accurate in the "
    "six-month test. AI should add value—not be used only because it is AI."
)

st.write(
    """
This is a useful lesson for organisations: a simpler, explainable method can
sometimes be the better planning choice. The purpose of evaluation is to find
the most reliable approach, not to make the most technical approach win.
"""
)

st.divider()

st.markdown(
    '<p class="question-label">See the test</p>',
    unsafe_allow_html=True,
)
st.header("How close were the estimates to official arrivals?")

chart = go.Figure()

chart.add_trace(
    go.Scatter(
        x=backtest_df["date"],
        y=backtest_df["actual_arrivals"],
        mode="lines+markers",
        name="Actual official arrivals",
        line=dict(color="#0F766E", width=4),
    )
)

chart.add_trace(
    go.Scatter(
        x=backtest_df["date"],
        y=backtest_df["baseline_prediction"],
        mode="lines+markers",
        name="Simple seasonal estimate",
        line=dict(color="#F59E0B", width=3, dash="dash"),
    )
)

chart.add_trace(
    go.Scatter(
        x=backtest_df["date"],
        y=backtest_df["ml_prediction"],
        mode="lines+markers",
        name="AI estimate",
        line=dict(color="#2563EB", width=3, dash="dot"),
    )
)

chart.update_layout(
    height=400,
    hovermode="x unified",
    xaxis_title="Month",
    yaxis_title="International visitor arrivals",
    yaxis_tickformat=",",
    margin=dict(l=10, r=10, t=20, b=10),
    plot_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(
    chart,
    use_container_width=True,
    config={"displayModeBar": False, "responsive": True},
)

st.caption(
    "The chart shows a historical six-month evaluation. It is not a published "
    "forecast for future visitor arrivals."
)

st.warning(
    "Interpret carefully: historical arrivals cannot establish causes, measure "
    "visitor respect, predict policy effects, or replace official tourism "
    "forecasts. COVID-era disruption can also make normal seasonal patterns "
    "less reliable."
)

with st.expander("For analysts: model method and accuracy details"):
    st.markdown(
        """
### Plain-language definitions

- **Backtest:** Hide known recent months, make estimates, and compare them with
  the official values.
- **WAPE:** Overall prediction error as a percentage of total actual arrivals.
  Lower is better.
- **MAE:** Average size of the monthly error.
- **RMSE:** A measure that gives more weight to larger errors.
- **Random Forest:** A machine-learning method that combines many decision trees
  to find patterns in historical data.
"""
    )

    comparison_df = pd.DataFrame(
        {
            "Method": ["Same month last year", "Random Forest"],
            "MAE": [baseline_metrics["mae"], ml_metrics["mae"]],
            "RMSE": [baseline_metrics["rmse"], ml_metrics["rmse"]],
            "WAPE (%)": [
                baseline_metrics["wape_pct"],
                ml_metrics["wape_pct"],
            ],
        }
    )

    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

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
        labels={
            "Importance": "Relative importance within the Random Forest",
            "Feature": "Input feature",
        },
        color="Importance",
        color_continuous_scale="Blues",
    )

    importance_chart.update_layout(
        height=350,
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=20, b=10),
    )

    st.plotly_chart(
        importance_chart,
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )

    st.markdown(
        f"""
**Training data ended:** {report["training_end_date"]}  
**Held-out test period:** {report["test_start_date"]} to {report["test_end_date"]}  
**Test months:** {report["test_months"]}  
**Baseline method:** {report["baseline_method"]}  
**Machine-learning method:** {report["machine_learning_method"]}
"""
    )

with st.expander("Data source and responsible-use limits"):
    st.markdown(
        """
**Input source:** Singapore Tourism Board, published through SingStat Table
Builder, *International Visitor Arrivals by Place of Residence* (`M550001`).

**Responsible-use boundary:** This exploratory model is not an official tourism
forecast. It should be used only as a transparent learning and planning
prototype, alongside domain expertise and official operational information.
"""
    )