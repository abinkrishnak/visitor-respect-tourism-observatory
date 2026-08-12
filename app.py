import streamlit as st

st.set_page_config(
    page_title="Visitor Respect & Sustainable Tourism Observatory",
    page_icon="🌏",
    layout="wide",
)

st.title("Visitor Respect & Sustainable Tourism Observatory")

st.subheader("Tourism can thrive when visitors, residents, and places thrive together.")

st.markdown(
    """
This public prototype combines trusted tourism statistics with transparent,
carefully validated AI-derived discussion signals.

Its purpose is to support respectful travel and better tourism planning.

**This website does not rank nationalities, make visa decisions, or treat
online discussion as representative of all visitors or residents.**
"""
)

st.info(
    "Version 0.1: Website foundation. Official Singapore tourism data and "
    "validated AI analysis will be added in later phases."
)

st.header("Our evidence labels")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.success("Official statistic")
    st.caption("Published by an official authority, such as STB or SingStat.")

with col2:
    st.info("Derived indicator")
    st.caption("A transparent calculation using named official data fields.")

with col3:
    st.warning("Model-derived signal")
    st.caption("A validated AI output from a defined online-discussion sample.")

with col4:
    st.error("Scenario / pilot")
    st.caption("A hypothetical calculation or voluntary learning-pilot result.")