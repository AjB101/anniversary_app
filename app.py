import streamlit as st
import pandas as pd

st.set_page_config(page_title="Our First Year Annivesary 💖", layout="centered")

st.title("💖 Our First Year Together")
st.write("Answer these questions about each other and see how well we know each other 😄")

# Questions
questions = [
    "Where did we first meet?",
    "What’s my favorite food?",
    "What’s my dream vacation?",
    "What’s one thing I always say?",
    "What makes me happiest?",
    "What’s my biggest goal right now?"
]

# Initialize session state
if "answers_you" not in st.session_state:
    st.session_state.answers_you = {}
if "answers_bae" not in st.session_state:
    st.session_state.answers_bae = {}

st.header("👤 Your Answers About Your Partner")

for q in questions:
    st.session_state.answers_you[q] = st.text_input(f"You: {q}", key=f"you_{q}")

st.header("💑 Your Partner's Answers About You")

for q in questions:
    st.session_state.answers_bae[q] = st.text_input(f"Partner: {q}", key=f"bae_{q}")

# Compare answers
if st.button("💖 See Our Match Score"):
    score = 0

    results = []

    for q in questions:
        a1 = st.session_state.answers_you[q].strip().lower()
        a2 = st.session_state.answers_bae[q].strip().lower()

        match = a1 == a2 and a1 != ""

        if match:
            score += 1

        results.append({
            "Question": q,
            "You": a1,
            "Partner": a2,
            "Match": "✅" if match else "❌"
        })

    st.subheader(f"💯 Match Score: {score} / {len(questions)}")

    df = pd.DataFrame(results)
    st.dataframe(df)

    # Fun message
    if score == len(questions):
        st.success("🔥 Perfect Match! Y’all locked in!")
    elif score > len(questions) // 2:
        st.info("💛 Pretty solid! You know each other well.")
    else:
        st.warning("😂 Time to learn more about each other!")

    # Download results
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results", csv, "anniversary_results.csv", "text/csv")