import streamlit as st

st.set_page_config(
    page_title="About | Tourism Observatory",
    page_icon="🌏",
    layout="wide",
)

st.title("About the Project")

st.subheader(
    "A responsible AI and data-product prototype for sustainable tourism."
)

st.markdown(
    """
Tourism can create jobs, economic value, and cultural exchange. It can also put
pressure on public spaces, heritage, the environment, and residents if growth
is not managed responsibly.

The Visitor Respect & Sustainable Tourism Observatory is a public project that
helps people understand tourism trends, learn respectful visitor behaviour,
and see how evidence can inform better questions for tourism planning.
"""
)

st.divider()

st.header("What the website does today")

col1, col2 = st.columns(2)

with col1:
    st.success("Uses official data")
    st.markdown(
        """
- Shows Singapore monthly international visitor arrivals.
- Shows year-on-year change.
- Explains source definitions and data limitations.
- Makes the data-processing approach visible.
"""
    )

with col2:
    st.info("Supports transparent interpretation")
    st.markdown(
        """
- Distinguishes official statistics from derived calculations.
- Explains why arrivals do not measure visitor behaviour or resident wellbeing.
- Warns against overinterpreting COVID-era percentage changes.
- Links visitors to the project methodology.
"""
    )

st.divider()

st.header("What the website will do next")

st.markdown(
    """
### 1. Add further official tourism indicators

Future dashboard versions may include tourism receipts, accommodation indicators,
and visitor-profile data, provided that each source and definition is documented.

### 2. Add validated AI discussion signals

A future NLP component will classify neutral tourism-discussion themes such as
crowding, visitor etiquette, cleanliness, and positive coexistence. It will use
a lawful public-data sample, human labels, model evaluation, and privacy
safeguards.

### 3. Add voluntary visitor-respect learning

A future micro-learning module will help visitors understand respectful behaviour
in shared and cultural spaces. It will be educational and voluntary—not a visa,
immigration, or enforcement system.
"""
)

st.divider()

st.header("What this project does not do")

st.error(
    """
This project does not rank nationalities, label people as good or bad tourists,
make visa decisions, make immigration or law-enforcement decisions, or treat
online discussion as representative of all visitors or residents.
"""
)

st.divider()

st.header("Who this project is for")

st.markdown(
    """
- **Visitors:** to learn how tourism can be more respectful and sustainable.
- **Residents and communities:** to see that wellbeing and local context matter.
- **Tourism planners:** to explore transparent data and limitations.
- **Researchers and employers:** to see an end-to-end responsible AI and data-product workflow.
"""
)

st.caption(
    "Project lead: Abin Krishna | MSc Enterprise AI student, Nanyang Technological University"
)