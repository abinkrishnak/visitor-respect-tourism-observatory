from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Tourism Activity | Tourism Observatory",
    page_icon="🏨",
    layout="wide",
)

DATA_FILE = Path("data/processed/singapore_annual_hotel_statistics.csv")


@st.cache_data
def load_hotel_data() -> pd.DataFrame:
    """Load processed annual Singapore hotel statistics."""
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

# The source is in thousand Singapore dollars.
latest_room_revenue_billion = (
    latest["room_revenue_thousand_sgd"] / 1_000_000
)

recent_df = df[df["year"] >= 2019].copy()
recent_df["room_revenue_billion_sgd"] = (
    recent_df["room_revenue_thousand_sgd"] / 1_000_000
)

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

        .meaning-card {
            background-color: rgba(15, 118, 110, 0.10);
            border-left: 4px solid #0F766E;
            border-radius: 8px;
            padding: 1.1rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="question-label">The benefit question</p>',
    unsafe_allow_html=True,
)

st.title("What does tourism make possible?")

st.subheader(
    "Tourism creates demand for places to stay, services to use, and experiences to enjoy."
)

st.write(
    """
Hotel statistics provide one official view of tourism-sector activity in
Singapore. They help us understand accommodation demand and hotel operations,
but they are not a complete measure of tourism’s total economic value.
"""
)

st.info(
    "This page reports figures for gazetted hotels only. Hotel activity is not "
    "the same as visitor behaviour, resident wellbeing, environmental impact, "
    "or the total value created by tourism."
)

st.divider()

st.markdown(
    '<p class="question-label">A recent snapshot</p>',
    unsafe_allow_html=True,
)
st.header(f"What did hotel activity look like in {latest_year}?")

metric_1, metric_2 = st.columns(2)

with metric_1:
    st.metric(
        label=f"Hotel room revenue — {latest_year}",
        value=f"S${latest_room_revenue_billion:,.2f} billion",
        help=(
            "Hotel room revenue for gazetted hotels. "
            "The official source reports this series in thousand Singapore dollars."
        ),
    )

with metric_2:
    st.metric(
        label=f"Average occupancy rate — {latest_year}",
        value=f"{latest['occupancy_rate_pct']:.1f}%",
        help="Percentage of available rooms sold during the year.",
    )

st.caption(
    f"{int(latest['gazetted_hotels'])} gazetted hotels were recorded in "
    f"{latest_year}, with an average room rate of "
    f"S${latest['average_room_rate_sgd']:,.1f}."
)

st.markdown(
    """
    <div class="meaning-card">
    <strong>What this suggests:</strong><br>
    When visitors stay in Singapore, accommodation demand supports hotel
    operations. These figures are useful context for tourism planning, but they
    do not tell us how benefits are distributed or whether tourism outcomes are
    positive for every community.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

st.markdown(
    '<p class="question-label">The recent journey</p>',
    unsafe_allow_html=True,
)
st.header("How did hotel activity change from disruption to recovery?")

st.write(
    "The charts begin in 2019 to make the COVID-19 disruption and subsequent "
    "recovery easier to see. Use the source notes before drawing conclusions "
    "from any single year."
)

occupancy_chart = px.line(
    recent_df,
    x="year",
    y="occupancy_rate_pct",
    markers=True,
    labels={
        "year": "Year",
        "occupancy_rate_pct": "Average occupancy rate (%)",
    },
)

occupancy_chart.update_traces(
    line_color="#0F766E",
    line_width=3,
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Occupancy rate: %{y:.1f}%<extra></extra>"
    ),
)

occupancy_chart.update_layout(
    height=360,
    yaxis_ticksuffix="%",
    margin=dict(l=10, r=10, t=20, b=10),
    plot_bgcolor="rgba(0,0,0,0)",
)

st.subheader("How fully were hotel rooms used?")
st.plotly_chart(
    occupancy_chart,
    use_container_width=True,
    config={"displayModeBar": False, "responsive": True},
)

revenue_chart = px.bar(
    recent_df,
    x="year",
    y="room_revenue_billion_sgd",
    labels={
        "year": "Year",
        "room_revenue_billion_sgd": "Hotel room revenue (S$ billion)",
    },
    color="room_revenue_billion_sgd",
    color_continuous_scale="Teal",
)

revenue_chart.update_traces(
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Room revenue: S$%{y:,.2f} billion<extra></extra>"
    ),
)

revenue_chart.update_layout(
    height=360,
    coloraxis_showscale=False,
    margin=dict(l=10, r=10, t=20, b=10),
    plot_bgcolor="rgba(0,0,0,0)",
)

st.subheader("How much hotel-room revenue was recorded?")
st.plotly_chart(
    revenue_chart,
    use_container_width=True,
    config={"displayModeBar": False, "responsive": True},
)

st.warning(
    "Interpret carefully: these official indicators cover gazetted hotels. "
    "They do not measure total visitor spending, employment, resident "
    "experience, site-level crowding, environmental impact, or visitor conduct."
)

st.divider()

st.markdown(
    '<p class="question-label">Continue the story</p>',
    unsafe_allow_html=True,
)
st.header("Where does visitor demand come from?")

st.write(
    """
Tourism activity is only one part of the picture. The next section explores
visitor-arrival patterns by place of residence—without treating place of
residence as nationality or a measure of behaviour.
"""
)

st.page_link(
    "pages/2_Understanding_Visitor_Demand.py",
    label="Continue to Understanding Visitor Demand →",
)

with st.expander("Source and definitions"):
    st.markdown(
        """
**Dataset:** Hotel Statistics (`M550111`)  
**Source:** Singapore Tourism Board, published through SingStat Table Builder.  
**Frequency:** Annual.

**Gazetted hotels:** licensed hotels specified under Singapore tourism
legislation.

**Average occupancy rate:** percentage of available rooms sold.

**Average room rate:** average rate paid for rooms sold, excluding service
charge and government taxes.

**Room revenue:** reported by the source in thousand Singapore dollars and
displayed on this website in billion Singapore dollars.
"""
    )