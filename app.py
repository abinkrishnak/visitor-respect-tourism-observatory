import streamlit as st

st.set_page_config(
    page_title="Visitor Respect & Sustainable Tourism Observatory",
    page_icon="🌏",
    layout="wide",
)

pages = {
    "Start Here": [
        st.Page(
            "home.py",
            title="Start Here",
            icon="🏠",
            default=True,
        ),
    ],
    "The Tourism Story": [
        st.Page(
            "pages/1_Tourism_Activity.py",
            title="Tourism Activity",
            icon="🏨",
        ),
        st.Page(
            "pages/2_Understanding_Visitor_Demand.py",
            title="Understanding Visitor Demand",
            icon="🗺️",
        ),
        st.Page(
            "pages/3_Travel_Respectfully.py",
            title="Travel Respectfully",
            icon="🧭",
        ),
        st.Page(
            "pages/4_Planning_Ahead.py",
            title="Planning Ahead",
            icon="📈",
        ),
    ],
    "Trust and Context": [
        st.Page(
            "pages/5_Why_This_Project_Exists.py",
            title="Why This Project Exists",
            icon="🌏",
        ),
        st.Page(
            "pages/6_Methods_and_Limitations.py",
            title="Methods and Limitations",
            icon="📘",
        ),
    ],
}

selected_page = st.navigation(pages, position="sidebar")
selected_page.run()