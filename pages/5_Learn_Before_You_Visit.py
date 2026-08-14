import streamlit as st

st.set_page_config(
    page_title="Learn Before You Visit | Tourism Observatory",
    page_icon="🧭",
    layout="wide",
)

st.title("Learn Before You Visit")

st.subheader("A short visitor-respect learning prototype")

st.markdown(
    """
This voluntary learning prototype encourages respectful behaviour in shared,
cultural, and public spaces.

It is **not** a visa exam, immigration requirement, enforcement tool, or
assessment of any person's identity. No answers are stored.
"""
)

st.info(
    "Prototype status: These general scenarios are intended for educational "
    "demonstration. Destination-specific content should be reviewed by "
    "appropriate local tourism, cultural, heritage, or community partners "
    "before public-policy use."
)

questions = [
    {
        "question": (
            "You arrive at a busy public attraction and see that a walkway "
            "is becoming blocked. What is the most respectful action?"
        ),
        "options": [
            "Stand in the walkway to take more photos",
            "Move to a safe open area and avoid blocking access",
            "Ask others to move away so your group has more space",
        ],
        "answer": "Move to a safe open area and avoid blocking access",
        "explanation": (
            "Shared pathways should remain accessible for residents, workers, "
            "visitors, and emergency access."
        ),
    },
    {
        "question": (
            "A heritage or cultural site displays visitor guidance. "
            "What should you do?"
        ),
        "options": [
            "Follow the posted guidance even if it differs from your usual habits",
            "Ignore it because you are only visiting briefly",
            "Ask another visitor to explain it instead of reading it",
        ],
        "answer": (
            "Follow the posted guidance even if it differs from your usual habits"
        ),
        "explanation": (
            "Posted guidance helps protect places, visitors, staff, and local "
            "communities."
        ),
    },
    {
        "question": (
            "You finish food or drinks in a public area and cannot immediately "
            "find a bin. What is the best choice?"
        ),
        "options": [
            "Leave the items nearby for cleaning staff",
            "Carry the items until you can dispose of them responsibly",
            "Place the items behind a bench so they are less visible",
        ],
        "answer": "Carry the items until you can dispose of them responsibly",
        "explanation": (
            "Responsible disposal helps protect public spaces and reduces the "
            "burden on local communities."
        ),
    },
    {
        "question": (
            "You are unsure whether photography, clothing, noise, or behaviour "
            "is appropriate in a particular place. What should you do?"
        ),
        "options": [
            "Check official guidance or ask authorised staff respectfully",
            "Assume the rules are the same as at home",
            "Copy whatever another visitor is doing",
        ],
        "answer": "Check official guidance or ask authorised staff respectfully",
        "explanation": (
            "Asking respectfully and using official guidance is the safest way "
            "to understand local expectations."
        ),
    },
]

with st.form("visitor_respect_quiz"):
    user_answers = []

    for number, item in enumerate(questions, start=1):
        st.markdown(f"### Question {number}")
        answer = st.radio(
            item["question"],
            item["options"],
            key=f"question_{number}",
        )
        user_answers.append(answer)

    submitted = st.form_submit_button("Check my answers")

if submitted:
    score = sum(
        selected_answer == item["answer"]
        for selected_answer, item in zip(user_answers, questions)
    )

    st.divider()
    st.success(f"Your learning score: {score} out of {len(questions)}")

    for number, (selected_answer, item) in enumerate(
        zip(user_answers, questions),
        start=1,
    ):
        if selected_answer == item["answer"]:
            st.success(f"Question {number}: Correct. {item['explanation']}")
        else:
            st.warning(
                f"Question {number}: Suggested answer — "
                f"{item['answer']}. {item['explanation']}"
            )

    st.caption(
        "Your answers are used only in this browser session and are not stored."
    )

st.divider()

st.header("Why this matters")

st.markdown(
    """
Respectful travel is not about labelling visitors as good or bad. It is about
helping people make informed choices that protect shared spaces, local
communities, and cultural places.
"""
)