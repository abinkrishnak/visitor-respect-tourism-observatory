from pathlib import Path
import json

import streamlit as st

st.set_page_config(
    page_title="Methods & Sources | Tourism Observatory",
    page_icon="📘",
    layout="wide",
)

QUALITY_FILE = Path("data/processed/arrivals_quality_report.json")


@st.cache_data
def load_quality_report() -> dict:
    """Load the quality report created by the data-processing pipeline."""
    if not QUALITY_FILE.exists():
        return {}

    with QUALITY_FILE.open(encoding="utf-8") as file:
        return json.load(file)


quality_report = load_quality_report()

st.title("Methods, Sources & Responsible Use")

st.markdown(
    """
This page explains how the Visitor Respect & Sustainable Tourism Observatory
uses data. We separate official statistics, our own transparent calculations,
future AI-derived signals, and hypothetical scenarios.

The goal is to support learning and better questions—not to judge nationalities,
make visa decisions, or claim that one indicator proves a tourism problem.
"""
)

st.divider()

st.header("Evidence labels")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.success("Official statistic")
    st.caption(
        "Published by an official authority. Example: monthly visitor arrivals "
        "from the Singapore Tourism Board."
    )

with col2:
    st.info("Derived indicator")
    st.caption(
        "A transparent calculation based on documented source fields. "
        "Example: year-on-year percentage change."
    )

with col3:
    st.warning("Model-derived signal")
    st.caption(
        "A future, validated AI output from a defined public-discussion sample. "
        "It is not currently shown on this website."
    )

with col4:
    st.error("Scenario / pilot")
    st.caption(
        "A hypothetical calculation or voluntary learning-pilot result. "
        "It is not a prediction or policy recommendation."
    )

st.divider()

st.header("Current official dataset")

st.markdown(
    """
**Dataset:** International Visitor Arrivals by Place of Residence  
**Table ID:** `M550001`  
**Source agency:** Singapore Tourism Board (STB)  
**Publishing platform:** SingStat Table Builder  
**Frequency:** Monthly  
**Geographic scope:** Singapore  
**Source link:** https://tablebuilder.singstat.gov.sg/table/TS/M550001
"""
)

st.markdown(
    """
### What this dataset measures

It measures international visitor arrivals recorded in Singapore, broken down by
place of residence.

### Important interpretation notes

- An arrival is an entry/visit, not necessarily one unique person.
- Place of residence is not the same as nationality.
- Arrival counts do not directly measure resident wellbeing, crowding at a
  particular attraction, cultural respect, environmental impact, or sentiment.
- A year-on-year percentage compares a month with the same month in the prior
  year. It helps account for seasonality, but COVID-era comparisons can be
  unusually large because the earlier value was very low.
"""
)

st.divider()

st.header("Data processing")

st.markdown(
    """
The original SingStat table is received in a wide format: one row per place of
residence and one column per month. For the tourism-pulse chart, the project:

1. Preserves the original downloaded source file without editing it.
2. Selects the official `Total International Visitor Arrivals` series.
3. Converts monthly columns into one row per month.
4. Checks for missing values, duplicate dates, and negative values.
5. Calculates year-on-year percentage change using a 12-month comparison.
6. Saves a processed dataset for this website.
"""
)

if quality_report:
    st.subheader("Latest automated data-quality report")
    st.json(quality_report)
else:
    st.info(
        "The automated quality report will appear after the arrivals "
        "processing script has been run."
    )

st.divider()

st.header("Privacy, fairness and future AI")

st.markdown(
    """
The current website uses only official aggregate tourism statistics.

A future NLP component may analyse a lawful, defined sample of public online
discussion. Before that happens, this project will publish a collection
protocol, annotation guide, model card, held-out model evaluation, limitations,
and privacy safeguards.

The project will not:

- rank nationalities, ethnicities, countries, or individuals;
- make visa, immigration, policing, or enforcement decisions;
- publish usernames or raw social-media posts;
- treat social-media discussion as representative of all visitors or residents;
- claim that online-discussion patterns prove causation.
"""
)

st.divider()

st.header("Project documents")

st.markdown(
    """
The detailed project documents are maintained in the public GitHub repository:

- `docs/data_dictionary.md`
- `docs/methodology.md`
- `docs/ethics_and_privacy.md`
- `src/transform/prepare_arrivals.py`

Repository: https://github.com/abinkrishnak/visitor-respect-tourism-observatory
"""
)

st.caption(
    "Last website data update is shown in the Tourism Pulse page. "
    "Always check the original source for the latest official release."
)