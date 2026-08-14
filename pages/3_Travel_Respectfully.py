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

        .principle-card {
            background-color: rgba(15, 118, 110, 0.10);
            border-left: 4px solid #0F766E;
            border-radius: 8px;
            padding: 1rem;
            min-height: 145px;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="question-label">The visitor question</p>',
    unsafe_allow_html=True,
)

st.title("How can a visitor leave a place better than they found it?")

st.subheader(
    "Respectful travel begins with curiosity, care, and a willingness to follow local guidance."
)

st.write(
    """
Tourism is made of everyday choices: how we use shared spaces, respond to local
rules, manage waste, take photographs, and treat people around us. This short
learning module is an invitation to reflect—not a way to label people as good
or bad visitors.
"""
)

st.info(
    "This is a voluntary educational prototype. It is not a visa exam, "
    "immigration requirement, enforcement tool, or assessment of identity. "
    "No answers are stored."
)

st.divider()

st.markdown(
    '<p class="question-label">Four simple principles</p>',
    unsafe_allow_html=True,
)
st.header("Before visiting somewhere new, pause and ask:")

principle_1, principle_2, principle_3, principle_4 = st.columns(4)

with principle_1:
    st.markdown(
        """
        <div class="principle-card">
        <h4>1. Am I making space for others?</h4>
        <p>Keep walkways, entrances, transport, and shared areas accessible.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with principle_2:
    st.markdown(
        """
        <div class="principle-card">
        <h4>2. Have I checked local guidance?</h4>
        <p>Rules around clothing, photography, noise, food, and access can differ by place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with principle_3:
    st.markdown(
        """
        <div class="principle-card">
        <h4>3. Am I caring for the place?</h4>
        <p>Dispose of waste responsibly and avoid damaging cultural or public spaces.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with principle_4:
    st.markdown(
        """
        <div class="principle-card">
        <h4>4. Am I willing to learn?</h4>
        <p>When unsure, ask authorised staff or check an official source respectfully.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    '<p class="question-label">Try four everyday choices</p>',
    unsafe_allow_html=True,
)
st.header("What would you do?")

st.write(
    "Choose the response that best protects shared spaces, local guidance, "
    "and other people’s experience."
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
            "Checking official guidance or asking authorised staff is the "
            "safest way to understand local expectations."
        ),
    },
]

with st.form("visitor_respect_quiz"):
    user_answers = []

    for number, item in enumerate(questions, start=1):
        st.markdown(f"### Everyday choice {number}")
        answer = st.radio(
            item["question"],
            item["options"],
            key=f"question_{number}",
        )
        user_answers.append(answer)

    submitted = st.form_submit_button("Reflect on my choices")

if submitted:
    score = sum(
        selected_answer == item["answer"]
        for selected_answer, item in zip(user_answers, questions)
    )

    st.divider()
    st.success(
        f"You selected the suggested response in {score} out of "
        f"{len(questions)} situations."
    )

    for number, (selected_answer, item) in enumerate(
        zip(user_answers, questions),
        start=1,
    ):
        if selected_answer == item["answer"]:
            st.success(f"Everyday choice {number}: {item['explanation']}")
        else:
            st.warning(
                f"Everyday choice {number}: Suggested response — "
                f"{item['answer']}. {item['explanation']}"
            )

    st.caption(
        "Your answers are used only in this browser session and are not stored."
    )

st.divider()

st.markdown(
    '<p class="question-label">Respect is personal; planning is shared</p>',
    unsafe_allow_html=True,
)
st.header("What can destinations do alongside visitor education?")

st.write(
    """
Visitors can make respectful choices, while destinations can use transparent
data to prepare for changing demand. The next page shows a carefully tested
planning prototype based on official monthly visitor-arrival data.
"""
)

st.page_link(
    "pages/4_Planning_Ahead.py",
    label="Continue to Planning Ahead →",
)

with st.expander("Important prototype boundary"):
    st.markdown(
        """
These are general educational scenarios. They are not destination-specific
cultural rules. Any future Singapore-specific guidance should be reviewed with
appropriate tourism, cultural, heritage, and community partners before use.
"""
    )