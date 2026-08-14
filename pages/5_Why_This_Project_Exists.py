import streamlit as st



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

        .choice-card {
            background-color: rgba(15, 118, 110, 0.10);
            border-left: 4px solid #0F766E;
            border-radius: 8px;
            padding: 1.1rem;
            min-height: 180px;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="question-label">The purpose</p>',
    unsafe_allow_html=True,
)

st.title("Why build a tourism project about respect?")

st.subheader(
    "Because a destination is more than a place to visit—it is also a home, a workplace, and a shared culture."
)

st.write(
    """
This project began with a personal observation. While following tourism news
and public discussions, I noticed stories about visitors sometimes ignoring
local guidance, damaging shared spaces, or treating cultural places without
care. At the same time, tourism clearly creates economic activity, employment,
and meaningful cultural exchange.

That tension led to one question: how can data and AI support more thoughtful
tourism without unfairly judging people?
"""
)

st.divider()

st.markdown(
    '<p class="question-label">A responsible redesign</p>',
    unsafe_allow_html=True,
)
st.header("What changed from the original idea?")

st.write(
    """
The first concept considered analysing news and online discussion to identify
tourism concerns. During the rebuild, the project was deliberately redesigned:
isolated news reports and social-media posts cannot represent all visitors,
residents, or communities fairly.

Instead, this prototype starts with transparent official data, states what the
data cannot show, and treats respectful travel as voluntary learning—not
enforcement.
"""
)

choice_1, choice_2, choice_3 = st.columns(3)

with choice_1:
    st.markdown(
        """
        <div class="choice-card">
        <h3>Use trustworthy evidence</h3>
        <p>Official tourism statistics provide a clear, reproducible starting point for understanding demand and tourism activity.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with choice_2:
    st.markdown(
        """
        <div class="choice-card">
        <h3>Use AI only when it adds value</h3>
        <p>The planning page tests a machine-learning method against a simple baseline instead of assuming that a complex model is better.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with choice_3:
    st.markdown(
        """
        <div class="choice-card">
        <h3>Encourage, do not punish</h3>
        <p>The visitor-learning module is voluntary, does not store answers, and is not connected to visa or immigration decisions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    '<p class="question-label">What this prototype does today</p>',
    unsafe_allow_html=True,
)
st.header("A simple journey from information to action")

st.markdown(
    """
1. **Shows tourism activity** using official Singapore hotel indicators.  
2. **Explains visitor demand** using official monthly arrivals by place of residence.  
3. **Encourages respectful choices** through a voluntary learning module.  
4. **Tests planning estimates honestly** by comparing a simple seasonal method with an AI model.  
5. **Explains sources and limitations** so visitors can understand what the figures mean.
"""
)

st.divider()

st.markdown(
    '<p class="question-label">What this project does not do</p>',
    unsafe_allow_html=True,
)

st.error(
    """
This project does not rank nationalities, label people as good or bad tourists,
infer behaviour from place of residence, make visa decisions, make immigration
or law-enforcement decisions, or claim that visitor-arrival data proves tourism
harm or cultural disrespect.
"""
)

st.divider()

st.markdown(
    '<p class="question-label">Who is this for?</p>',
    unsafe_allow_html=True,
)
st.header("A public prototype for better questions")

st.markdown(
    """
- **Visitors:** to reflect on respectful travel and local guidance.
- **Tourism planners:** to explore transparent demand indicators and planning limits.
- **Students and researchers:** to see a reproducible, responsible AI workflow.
- **Employers:** to see how data engineering, visualisation, model evaluation,
  ethics, and product design can work together.
"""
)

st.divider()

st.markdown(
    '<p class="question-label">Trust comes from transparency</p>',
    unsafe_allow_html=True,
)
st.header("What should a reader inspect before trusting this project?")

st.write(
    """
The source tables, data transformations, quality checks, model evaluation, and
model card are available in the repository. A reader should be able to see
where the data came from, how it was processed, how the model was tested, and
where its limits begin.
"""
)

st.page_link(
    "pages/6_Methods_and_Limitations.py",
    label="Continue to Methods and Limitations →",
)

st.caption(
    "Project lead: Abin Krishna | MSc Enterprise AI student, "
    "Nanyang Technological University"
)