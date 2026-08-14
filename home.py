from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_FILE = Path("data/processed/singapore_monthly_arrivals.csv")


@st.cache_data
def load_arrivals_data() -> pd.DataFrame:
    """Load processed official Singapore visitor-arrival data."""
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


st.markdown(
    """
    <style>
        .story-label {
            color: #0F766E;
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .story-card {
            background-color: rgba(15, 118, 110, 0.10);
            border-left: 4px solid #0F766E;
            border-radius: 8px;
            padding: 1.1rem;
            min-height: 190px;
            margin-bottom: 1rem;
        }

        .quiet-card {
            background-color: rgba(30, 64, 175, 0.10);
            border-left: 4px solid #1E40AF;
            border-radius: 8px;
            padding: 1.1rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

df = load_arrivals_data()
latest = df.iloc[-1]
latest_date = latest["date"]
latest_arrivals = int(latest["arrivals"])
latest_yoy = latest["arrivals_yoy_pct"]

# Opening scene
st.markdown('<p class="story-label">Singapore-first public prototype</p>', unsafe_allow_html=True)

st.title("What does a good trip leave behind?")

st.subheader("Tourism works best when visitors, communities, and places thrive together.")

st.write(
    """
    Tourism creates memorable experiences and supports destination economies.
    As visitor demand changes, thoughtful planning and respectful choices become
    more important. This project turns official Singapore tourism data into a
    simple learning journey—not a judgement about people.
    """
)

st.info(
    "This website does not rank nationalities, identify individual behaviour, "
    "make visa decisions, or treat visitor-arrival data as evidence of respect "
    "or disrespect."
)

st.divider()

# Story map
st.markdown('<p class="story-label">The story</p>', unsafe_allow_html=True)
st.header("Three questions guide this project")

question_1, question_2, question_3 = st.columns(3)

with question_1:
    st.markdown(
        """
        <div class="story-card">
        <h3>1. What does tourism make possible?</h3>
        <p>Official arrival and hotel indicators help us understand the scale
        and rhythm of tourism activity in Singapore.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(
        "pages/1_Tourism_Activity.py",
        label="Explore tourism activity →",
    )

with question_2:
    st.markdown(
        """
        <div class="story-card">
        <h3>2. When does a destination need to prepare?</h3>
        <p>Visitor-arrival patterns show when demand is changing. They do not,
        by themselves, prove crowding or harm.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(
        "pages/2_Understanding_Visitor_Demand.py",
        label="Understand visitor demand →",
    )

with question_3:
    st.markdown(
        """
        <div class="story-card">
        <h3>3. What can a visitor do?</h3>
        <p>Respectful travel begins before arrival: learn local expectations,
        follow site rules, and make informed choices.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(
        "pages/3_Travel_Respectfully.py",
        label="Try the learning module →",
    )

st.divider()

# Evidence scene
st.markdown('<p class="story-label">Scene one: the tourism pulse</p>', unsafe_allow_html=True)
st.header("How has visitor demand changed over time?")

st.write(
    "The chart below uses Singapore’s official monthly international visitor-arrival data. "
    "It gives context for planning; it does not measure visitor behaviour."
)

metric_1, metric_2 = st.columns(2)

with metric_1:
    st.metric(
        label=f"Latest official arrivals — {latest_date.strftime('%B %Y')}",
        value=f"{latest_arrivals:,}",
    )

with metric_2:
    if pd.notna(latest_yoy):
        st.metric(
            label="Change from the same month a year earlier",
            value=f"{latest_yoy:+.1f}%",
            help="This comparison accounts for normal seasonal travel patterns.",
        )
    else:
        st.metric(label="Year-on-year change", value="Not available")

st.caption(
    f"Data coverage: {df['date'].min().strftime('%B %Y')} to "
    f"{df['date'].max().strftime('%B %Y')}."
)

recent_start_year = max(int(df["year"].min()), int(latest_date.year) - 6)
recent_df = df[df["year"] >= recent_start_year].copy()

chart = px.line(
    recent_df,
    x="date",
    y="arrivals",
    labels={
        "date": "Month",
        "arrivals": "International visitor arrivals",
    },
)

chart.update_traces(
    line_color="#0F766E",
    line_width=3,
    hovertemplate=(
        "<b>%{x|%B %Y}</b><br>"
        "Arrivals: %{y:,.0f}<extra></extra>"
    ),
)

chart.update_layout(
    height=380,
    hovermode="x unified",
    yaxis_tickformat=",",
    margin=dict(l=10, r=10, t=20, b=10),
    plot_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(
    chart,
    use_container_width=True,
    config={"displayModeBar": False, "responsive": True},
)

st.markdown(
    """
    <div class="quiet-card">
    <strong>Read this carefully.</strong><br>
    Visitor arrivals are recorded entries or visits, not necessarily unique
    people. Place of residence is not the same as nationality. Higher or lower
    arrivals do not tell us whether visitors behaved respectfully.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# Closing scene
st.markdown('<p class="story-label">What comes next?</p>', unsafe_allow_html=True)
st.header("Can data and AI help people prepare—without judging people?")

st.write(
    """
    The final part of this project tests whether past arrival patterns can help
    estimate future visitor demand. It is a planning aid for analysts, not a
    tool for judging visitors.
    """
)

st.page_link(
    "pages/4_Planning_Ahead.py",
    label="Continue to Planning Ahead →",
)

with st.expander("Source, method, and limits"):
    st.markdown(
        f"""
**Official source:** Singapore Tourism Board (STB), published through SingStat
Table Builder, *International Visitor Arrivals by Place of Residence* (`M550001`).

**Data through:** {latest_date.strftime('%B %Y')}.

**Processing:** The source table was transformed from a wide monthly format into
one record per month. The processing script checks for missing values, duplicate
dates, and negative values.

**What this data cannot measure:** individual visitor behaviour, cultural
respect, resident wellbeing, environmental impact, site-level crowding, or
visitor sentiment.
"""
    )

st.caption(
    "Version 1.1 in progress — Story-first redesign using official Singapore tourism data."
)