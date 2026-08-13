from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Hotel Performance | Tourism Observatory",
    page_icon="🏨",
    layout="wide",
)

DATA_FILE = Path("data/processed/singapore_annual_hotel_statistics.csv")


@st.cache_data
def load_hotel_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Hotel dataset not found. Run: "
            "python src/transform/prepare_hotel_statistics.py"
        )

    data = pd.read_csv(DATA_FILE)

    required_columns = {
        "year",
        "gazetted_hotels",
        "occupancy_rate_pct",
        "available_room_nights",
        "average_room_rate_sgd",
        "room_revenue_thousand_sgd",
    }

    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_columns)}"
        )

    return data.sort_values("year").reset_index(drop=True)


df = load_hotel_data()
latest = df.iloc[-1]
latest_year = int(latest["year"])

st.title("Singapore Hotel Performance")

st.markdown(
    """
This page provides official annual hotel-performance context alongside visitor
arrivals. It helps show tourism-sector operations, but hotel data alone cannot
measure resident wellbeing, site-level crowding, visitor behaviour, or
sustainability.
"""
)

st.caption(
    "Evidence label: Official statistic | "
    "Source: Singapore Tourism Board via SingStat, Table M550111"
)

st.divider()

metric_1, metric_2, metric_3 = st.columns(3)

with metric_1:
    st.metric(
        label=f"Average occupancy rate — {latest_year}",
        value=f"{latest['occupancy_rate_pct']:.1f}%",
        help="Percentage of available rooms sold during the year.",
    )

with metric_2:
    st.metric(
        label=f"Average room rate — {latest_year}",
        value=f"S${latest['average_room_rate_sgd']:,.1f}",
        help=(
            "Average rate paid for rooms sold, excluding service charge "
            "and government taxes."
        ),
    )

with metric_3:
    st.metric(
        label=f"Room revenue — {latest_year}",
        value=f"S${latest['room_revenue_thousand_sgd'] / 1_000:,.2f} billion",
        help=(
            "Displayed in billions of Singapore dollars. "
            "The source series is reported in thousand dollars."
        ),
    )

st.divider()

selected_years = st.slider(
    "Choose a year range",
    min_value=int(df["year"].min()),
    max_value=int(df["year"].max()),
    value=(2019, int(df["year"].max())),
)

filtered_df = df[
    df["year"].between(selected_years[0], selected_years[1])
].copy()

occupancy_chart = px.line(
    filtered_df,
    x="year",
    y="occupancy_rate_pct",
    markers=True,
    title="Average Hotel Occupancy Rate",
    labels={
        "year": "Year",
        "occupancy_rate_pct": "Average occupancy rate (%)",
    },
)

occupancy_chart.update_traces(
    line_color="#0F766E",
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Occupancy rate: %{y:.1f}%<extra></extra>"
    ),
)

occupancy_chart.update_layout(
    title_x=0,
    yaxis_ticksuffix="%",
    margin=dict(l=10, r=10, t=60, b=10),
)

st.plotly_chart(occupancy_chart, use_container_width=True)

left_chart, right_chart = st.columns(2)

with left_chart:
    room_rate_chart = px.line(
        filtered_df,
        x="year",
        y="average_room_rate_sgd",
        markers=True,
        title="Average Room Rate",
        labels={
            "year": "Year",
            "average_room_rate_sgd": "Average room rate (S$)",
        },
    )

    room_rate_chart.update_traces(
        line_color="#2563EB",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average room rate: S$%{y:,.1f}<extra></extra>"
        ),
    )

    room_rate_chart.update_layout(
        title_x=0,
        yaxis_tickprefix="S$",
        margin=dict(l=10, r=10, t=60, b=10),
    )

    st.plotly_chart(room_rate_chart, use_container_width=True)

with right_chart:
    revenue_chart = px.bar(
        filtered_df,
        x="year",
        y="room_revenue_thousand_sgd",
        title="Hotel Room Revenue",
        labels={
            "year": "Year",
            "room_revenue_thousand_sgd": "Room revenue (thousand S$)",
        },
        color="room_revenue_thousand_sgd",
        color_continuous_scale="Teal",
    )

    revenue_chart.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Room revenue: S$%{y / 1000:,.2f} billion<extra></extra>"
        ),
    )

    revenue_chart.update_layout(
        title_x=0,
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=60, b=10),
    )

    st.plotly_chart(revenue_chart, use_container_width=True)

st.warning(
    "Interpret carefully: figures refer to gazetted hotels. Hotel occupancy, "
    "room rates, and room revenue are operational tourism indicators; they do "
    "not by themselves measure resident experience, environmental impact, "
    "visitor conduct, or a destination's carrying capacity."
)

with st.expander("Source and definitions"):
    st.markdown(
        """
**Dataset:** Hotel Statistics (`M550111`)  
**Source:** Singapore Tourism Board, published through SingStat Table Builder.  
**Frequency:** Annual.

**Average occupancy rate:** percentage of available rooms sold.  
**Average room rate:** average rate paid for rooms sold, excluding service
charge and government taxes.  
**Room revenue:** reported by the source in thousand Singapore dollars.  
**Coverage:** gazetted hotels—licensed hotels specified under Singapore tourism
legislation.
"""
    )