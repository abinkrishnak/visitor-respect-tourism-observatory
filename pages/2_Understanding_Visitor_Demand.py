from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st



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
    '<p class="question-label">The demand question</p>',
    unsafe_allow_html=True,
)

st.title("How does visitor demand reach Singapore?")

st.subheader(
    "Understanding visitor flows helps destinations prepare—but it must never become a judgement about people."
)

st.write(
    """
This page shows Singapore’s official visitor-arrival records by **place of
residence**. It gives a high-level picture of visitor-flow composition and can
support planning for changing demand.
"""
)

st.info(
    "A place of residence is not the same as nationality. This data does not "
    "measure culture, behaviour, respect, spending, impact, or risk."
)

st.divider()

st.markdown(
    '<p class="question-label">Choose a moment in the story</p>',
    unsafe_allow_html=True,
)
st.header("Which month would you like to explore?")

available_dates = sorted(df["date"].dropna().unique())
latest_date = max(available_dates)

selected_date = st.selectbox(
    "Select a month",
    options=available_dates,
    index=available_dates.index(latest_date),
    format_func=lambda date: pd.Timestamp(date).strftime("%B %Y"),
    help="The latest available month is selected by default.",
)

selected_df = df[df["date"].eq(selected_date)].copy()
top_10 = selected_df.nlargest(10, "arrivals").sort_values("arrivals")

named_place_count = selected_df["place_of_residence"].nunique()
arrivals_across_named_places = int(selected_df["arrivals"].sum())

st.caption(
    "Evidence label: Official statistic | Source: Singapore Tourism Board via "
    "SingStat, Table M550001"
)

metric_1, metric_2 = st.columns(2)

with metric_1:
    st.metric(
        label=(
            "Named places included — "
            f"{pd.Timestamp(selected_date).strftime('%B %Y')}"
        ),
        value=f"{named_place_count}",
        help="Only named places of residence are included after processing.",
    )

with metric_2:
    st.metric(
        label="Arrivals across named places shown",
        value=f"{arrivals_across_named_places:,}",
        help=(
            "This excludes regional totals and non-specific 'Other Markets' "
            "categories. It is not Singapore's national visitor-arrival total."
        ),
    )

st.markdown(
    """
    <div class="meaning-card">
    <strong>Why this view matters:</strong><br>
    Visitor demand is not evenly distributed. Seeing broad arrival patterns can
    help organisations prepare for changing needs in accommodation, transport,
    visitor information, and services. It does not tell us anything about the
    character or behaviour of any individual or group.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

st.markdown(
    '<p class="question-label">The flow picture</p>',
    unsafe_allow_html=True,
)
st.header(
    "Which named places of residence had the largest recorded arrival flows?"
)

chart = px.bar(
    top_10,
    x="arrivals",
    y="place_of_residence",
    orientation="h",
    labels={
        "arrivals": "International visitor arrivals",
        "place_of_residence": "Named place of residence",
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
    height=480,
    coloraxis_showscale=False,
    xaxis_tickformat=",",
    margin=dict(l=10, r=10, t=20, b=10),
    plot_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(
    chart,
    use_container_width=True,
    config={"displayModeBar": False, "responsive": True},
)

st.warning(
    "Interpret carefully: this is place of residence, not nationality. The "
    "chart excludes regional aggregate rows and 'Other Markets' buckets, so "
    "its displayed total is not Singapore's national visitor-arrival total. "
    "It does not measure visitor behaviour, tourism impact, or risk."
)

st.divider()

st.markdown(
    '<p class="question-label">Continue the story</p>',
    unsafe_allow_html=True,
)
st.header("What can a visitor do with this understanding?")

st.write(
    """
Data can help destinations prepare, but respectful tourism also depends on
individual choices. The next page is a short voluntary learning module about
shared spaces, local guidance, and responsible travel.
"""
)

st.page_link(
    "pages/3_Travel_Respectfully.py",
    label="Continue to Travel Respectfully →",
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