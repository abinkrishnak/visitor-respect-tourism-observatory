from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Visitor Origins | Tourism Observatory",
    page_icon="🗺️",
    layout="wide",
)

DATA_FILE = Path("data/processed/singapore_arrivals_by_residence.csv")


@st.cache_data
def load_residence_data() -> pd.DataFrame:
    """Load processed arrivals by place of residence."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Processed residence dataset not found. Run: "
            "python src/transform/prepare_residence_arrivals.py"
        )

    data = pd.read_csv(DATA_FILE, parse_dates=["date"])

    required_columns = {"date", "place_of_residence", "arrivals"}
    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_columns)}"
        )

    return data.sort_values(["date", "arrivals"], ascending=[True, False])


df = load_residence_data()

st.title("Visitor Arrivals by Place of Residence")

st.markdown(
    """
This page shows the largest **named places of residence** in Singapore's
official monthly visitor-arrival data.

It is intended to show visitor-flow composition, not to judge or compare
people. A place of residence is not the same as nationality.
"""
)

st.caption(
    "Evidence label: Official statistic | "
    "Source: Singapore Tourism Board via SingStat, Table M550001"
)

available_dates = sorted(df["date"].dropna().unique())
latest_date = max(available_dates)

selected_date = st.select_slider(
    "Choose a month",
    options=available_dates,
    value=latest_date,
    format_func=lambda date: pd.Timestamp(date).strftime("%B %Y"),
)

selected_df = df[df["date"].eq(selected_date)].copy()
top_10 = selected_df.nlargest(10, "arrivals").sort_values("arrivals")

latest_total = int(selected_df["arrivals"].sum())

metric_1, metric_2 = st.columns(2)

with metric_1:
    st.metric(
        label=f"Named places included — {pd.Timestamp(selected_date).strftime('%B %Y')}",
        value=f"{selected_df['place_of_residence'].nunique()}",
    )

with metric_2:
    st.metric(
        label="Arrivals across named places shown",
        value=f"{latest_total:,}",
        help=(
            "This excludes regional totals and non-specific 'Other Markets' "
            "categories. It is not the national total."
        ),
    )

chart = px.bar(
    top_10,
    x="arrivals",
    y="place_of_residence",
    orientation="h",
    title=(
        "Top 10 Named Places of Residence — "
        f"{pd.Timestamp(selected_date).strftime('%B %Y')}"
    ),
    labels={
        "arrivals": "International visitor arrivals",
        "place_of_residence": "Place of residence",
    },
    color="arrivals",
    color_continuous_scale="Teal",
)

chart.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Arrivals: %{x:,.0f}<extra></extra>"
    )
)

chart.update_layout(
    title_x=0,
    coloraxis_showscale=False,
    xaxis_tickformat=",",
    margin=dict(l=10, r=10, t=60, b=10),
)

st.plotly_chart(chart, use_container_width=True)

st.warning(
    "Interpret carefully: this is place of residence, not nationality. "
    "The chart excludes regional aggregate rows and 'Other Markets' buckets, "
    "so its displayed total is not Singapore's national visitor-arrival total. "
    "It does not measure visitor behaviour, tourism impact, or risk."
)

with st.expander("Source and processing notes"):
    st.markdown(
        """
**Source:** Singapore Tourism Board (STB), published through SingStat Table
Builder, *International Visitor Arrivals by Place of Residence* (`M550001`).

**Processing:** The project excludes the national total, regional aggregate
rows, and non-specific `Other Markets` categories before ranking named places.

**Limitation:** This chart cannot be used to infer nationality, intent,
behaviour, cultural respect, or the effect of any country/group on Singapore.
"""
    )