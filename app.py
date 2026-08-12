from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Visitor Respect & Sustainable Tourism Observatory",
    page_icon="🌏",
    layout="wide",
)

DATA_FILE = Path("data/processed/singapore_monthly_arrivals.csv")


@st.cache_data
def load_arrivals_data() -> pd.DataFrame:
    """Load the processed official Singapore arrivals dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Processed data file not found. "
            "Run: python src/transform/prepare_arrivals.py"
        )

    data = pd.read_csv(DATA_FILE, parse_dates=["date"])

    required_columns = {
        "date",
        "arrivals",
        "year",
        "month",
        "month_name",
        "arrivals_yoy_pct",
    }

    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(
            f"The processed dataset is missing: {sorted(missing_columns)}"
        )

    return data.sort_values("date").reset_index(drop=True)


df = load_arrivals_data()

latest = df.iloc[-1]
latest_date = latest["date"]
latest_arrivals = int(latest["arrivals"])
latest_yoy = latest["arrivals_yoy_pct"]

st.title("Visitor Respect & Sustainable Tourism Observatory")

st.subheader(
    "Tourism can thrive when visitors, residents, and places thrive together."
)

st.markdown(
    """
This public prototype uses official tourism statistics to help users understand
visitor trends in Singapore. Future versions will add carefully validated,
privacy-conscious AI discussion signals and a voluntary visitor-respect
learning module.

**This website does not rank nationalities, make visa decisions, or treat
online discussion as representative of all visitors or residents.**
"""
)

st.divider()

st.header("Singapore Tourism Pulse")

st.caption(
    "Evidence label: Official statistic | "
    "Source: Singapore Tourism Board via SingStat, Table M550001"
)

metric_1, metric_2, metric_3 = st.columns(3)

with metric_1:
    st.metric(
        label=f"International visitor arrivals — {latest_date.strftime('%B %Y')}",
        value=f"{latest_arrivals:,}",
    )

with metric_2:
    if pd.notna(latest_yoy):
        st.metric(
            label="Year-on-year change",
            value=f"{latest_yoy:+.1f}%",
            help=(
                "Compares the latest month with the same month in the "
                "previous year. This helps account for seasonal travel patterns."
            ),
        )
    else:
        st.metric(
            label="Year-on-year change",
            value="Not available",
        )

with metric_3:
    st.metric(
        label="Data coverage",
        value=(
            f"{df['date'].min().strftime('%b %Y')} – "
            f"{df['date'].max().strftime('%b %Y')}"
        ),
    )

chart = px.line(
    df,
    x="date",
    y="arrivals",
    title="Monthly International Visitor Arrivals in Singapore",
    labels={
        "date": "Month",
        "arrivals": "International visitor arrivals",
    },
)

chart.update_traces(
    line_color="#0F766E",
    hovertemplate=(
        "<b>%{x|%B %Y}</b><br>"
        "Arrivals: %{y:,.0f}<extra></extra>"
    ),
)

chart.update_layout(
    hovermode="x unified",
    yaxis_tickformat=",",
    title_x=0,
    margin=dict(l=10, r=10, t=60, b=10),
)

st.plotly_chart(chart, use_container_width=True)

st.info(
    "How to read this chart: arrivals are entries/visits recorded by the "
    "tourism system. They are not necessarily unique people, and place of "
    "residence is not the same as nationality."
)

with st.expander("Data source, method, and limitations"):
    st.markdown(
        f"""
**Source:** Singapore Tourism Board (STB), published through SingStat Table
Builder, *International Visitor Arrivals by Place of Residence* (`M550001`).

**Data through:** {latest_date.strftime('%B %Y')}.

**Transformation:** The website uses the official national-total series,
converted from the original wide monthly table into one record per month.
The processing script checks for missing values, duplicate dates, and negative
arrival values.

**Limitations:** This indicator does not measure unique visitors, resident
wellbeing, site-level crowding, cultural respect, environmental impact, or
visitor sentiment. Those questions require other evidence and must not be
inferred from arrivals alone.
"""
    )

st.divider()

st.caption(
    "Project status: Version 0.2 — Official Singapore tourism-data dashboard. "
    "See `docs/data_dictionary.md` in the GitHub repository for definitions."
)