from pathlib import Path
import json

import streamlit as st


QUALITY_FILE = Path("data/processed/arrivals_quality_report.json")


@st.cache_data
def load_quality_report() -> dict:
    """Load the automated arrivals data-quality report."""
    if not QUALITY_FILE.exists():
        return {}

    with QUALITY_FILE.open(encoding="utf-8") as file:
        return json.load(file)


quality_report = load_quality_report()

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

        .evidence-card {
            background-color: rgba(15, 118, 110, 0.10);
            border-left: 4px solid #0F766E;
            border-radius: 8px;
            padding: 1rem;
            min-height: 160px;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="question-label">The trust question</p>',
    unsafe_allow_html=True,
)

st.title("How do we know what to trust?")

st.subheader(
    "Trust does not mean that data is perfect. It means the source, method, and limitations are visible."
)

st.write(
    """
This project separates official facts, transparent calculations, tested model
outputs, and voluntary learning content. Each has a different purpose and
should be interpreted differently.
"""
)

st.divider()

st.markdown(
    '<p class="question-label">Four kinds of information</p>',
    unsafe_allow_html=True,
)
st.header("What are you looking at on this website?")

left_1, right_1 = st.columns(2)
left_2, right_2 = st.columns(2)

with left_1:
    st.markdown(
        """
        <div class="evidence-card">
        <h3>Official statistic</h3>
        <p>Published by an official authority. Example: Singapore monthly visitor arrivals and annual hotel statistics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_1:
    st.markdown(
        """
        <div class="evidence-card">
        <h3>Derived calculation</h3>
        <p>A transparent calculation from official data. Example: year-on-year change in visitor arrivals.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with left_2:
    st.markdown(
        """
        <div class="evidence-card">
        <h3>Tested planning estimate</h3>
        <p>A model comparison based on historical arrivals. It is exploratory and is not an official forecast.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_2:
    st.markdown(
        """
        <div class="evidence-card">
        <h3>Voluntary learning content</h3>
        <p>General respectful-travel scenarios. They are educational, not a legal rule, score of identity, or enforcement tool.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    '<p class="question-label">Official data sources</p>',
    unsafe_allow_html=True,
)
st.header("Where does the data come from?")

st.markdown(
    """
### 1. Monthly visitor arrivals

- **Dataset:** International Visitor Arrivals by Place of Residence  
- **Table ID:** `M550001`  
- **Source agency:** Singapore Tourism Board, published through SingStat  
- **Frequency:** Monthly  
- **Used for:** Tourism Pulse, Visitor Demand, and Planning Ahead  
- **Source:** https://tablebuilder.singstat.gov.sg/table/TS/M550001  

### 2. Annual hotel statistics

- **Dataset:** Hotel Statistics  
- **Table ID:** `M550111`  
- **Source agency:** Singapore Tourism Board, published through SingStat  
- **Frequency:** Annual  
- **Used for:** Tourism Activity  
- **Source:** https://tablebuilder.singstat.gov.sg/table/TS/M550111
"""
)

st.info(
    "Official statistics are the most appropriate starting point for this "
    "prototype because their publisher, definitions, frequency, and source "
    "tables are visible to the public."
)

st.divider()

st.markdown(
    '<p class="question-label">From raw table to website</p>',
    unsafe_allow_html=True,
)
st.header("What happens to the official data before you see it?")

st.markdown(
    """
1. The project preserves the original downloaded source file.  
2. It converts wide monthly tables into one record per month.  
3. It selects the documented official series required for each page.  
4. It checks for missing values, duplicate dates, and negative arrival values.  
5. It creates transparent derived fields, such as year-on-year change.  
6. It saves processed data used by the Streamlit website.  
"""
)

if quality_report:
    st.subheader("Latest automated arrivals data-quality check")

    check_1, check_2, check_3, check_4 = st.columns(4)

    with check_1:
        st.metric("Monthly records", quality_report.get("record_count", "—"))

    with check_2:
        st.metric("Missing arrival values", quality_report.get("missing_arrivals", "—"))

    with check_3:
        st.metric("Duplicate dates", quality_report.get("duplicate_dates", "—"))

    with check_4:
        st.metric(
            "Data coverage",
            (
                f"{quality_report.get('start_date', '—')[:7]} to "
                f"{quality_report.get('end_date', '—')[:7]}"
            ),
        )

st.divider()

st.markdown(
    '<p class="question-label">How AI is used responsibly</p>',
    unsafe_allow_html=True,
)
st.header("The model is tested against a simpler method")

st.write(
    """
The Planning Ahead page compares a simple “same month last year” estimate with
a Random Forest machine-learning model. Both methods are tested on six months
that were hidden before evaluation.

The website keeps the method with lower error. In the current evaluation, the
simpler seasonal method performed better. This is intentional: a more complex
model should not be preferred unless it demonstrates a real improvement.
"""
)

st.warning(
    "The planning estimate cannot establish causes, identify visitor behaviour, "
    "predict policy effects, or replace official tourism forecasts. It is a "
    "learning and planning prototype only."
)

st.divider()

st.markdown(
    '<p class="question-label">Limits and boundaries</p>',
    unsafe_allow_html=True,
)
st.header("What this project cannot claim")

st.error(
    """
This project cannot rank nationalities, infer behaviour from place of residence,
identify “good” or “bad” tourists, measure resident wellbeing, prove crowding,
measure cultural respect, make visa decisions, or make immigration,
law-enforcement, or policy decisions.
"""
)

st.write(
    """
A visitor-arrival count is useful for understanding tourism demand. It is not
evidence that a particular group caused a problem, nor is it evidence that a
destination is experiencing harm.
"""
)

st.divider()

st.markdown(
    '<p class="question-label">Audit the work</p>',
    unsafe_allow_html=True,
)
st.header("Where can you inspect the project?")

st.markdown(
    """
The public repository contains the source code, data documentation, processing
scripts, and model documentation:

- `docs/data_dictionary.md`
- `docs/model_card.md`
- `src/transform/prepare_arrivals.py`
- `src/transform/prepare_residence_arrivals.py`
- `src/transform/prepare_hotel_statistics.py`
- `src/ml/train_arrival_forecast.py`

Repository:  
https://github.com/abinkrishnak/visitor-respect-tourism-observatory
"""
)

st.caption(
    "Always check the original SingStat/STB tables for the latest official release."
)