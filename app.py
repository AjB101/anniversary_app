import streamlit as st
import pandas as pd
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Our First Year Anniversary 💖", layout="centered")

# -----------------------------
# LOGIN
# -----------------------------
st.sidebar.title("Login 💖")

user_name = st.sidebar.text_input("Enter your name")

if not user_name:
    st.warning("Please enter your name to continue")
    st.stop()

# -----------------------------
# TITLE
# -----------------------------
st.title("💖 Our First Year Together")

st.markdown(f"""
Welcome **{user_name}** 💕

Answer honestly and let’s see how well you both know each other 😄
""")

# -----------------------------
# QUESTIONS
# -----------------------------
questions = [
    "Where did we first meet?",
    "What’s my favorite food?",
    "What’s my dream vacation?",
    "What’s one thing I always say?",
    "What makes me happiest?",
    "What’s my biggest goal right now?"
]

# -----------------------------
# DATA STORAGE
# -----------------------------
DATA_FILE = "answers.csv"

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["user", "question", "answer"])
    df_init.to_csv(DATA_FILE, index=False)

# -----------------------------
# INPUT SECTION
# -----------------------------
st.header(f"💬 {user_name}, answer these questions")

answers = {}

for q in questions:
    key = f"{user_name}_{q}"

    # initialize state if not exists
    if key not in st.session_state:
        st.session_state[key] = ""

    answers[q] = st.text_input(q, key=key)

# -----------------------------
# SAVE ANSWERS
# -----------------------------
if st.button("💾 Save My Answers"):
    df = pd.read_csv(DATA_FILE)

    # Remove old answers for this user
    df = df[df["user"] != user_name]

    # Add new answers
    new_rows = []
    for q, a in answers.items():
        new_rows.append({
            "user": user_name,
            "question": q,
            "answer": a
        })

    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    st.success("Answers saved! 💖")

    # ✅ CLEAR INPUTS AFTER SAVE
    for q in questions:
        st.session_state[f"{user_name}_{q}"] = ""

# -----------------------------
# RESET BUTTON
# -----------------------------
if st.button("🔄 Reset My Answers"):
    df = pd.read_csv(DATA_FILE)

    df = df[df["user"] != user_name]
    df.to_csv(DATA_FILE, index=False)

    for q in questions:
        st.session_state[f"{user_name}_{q}"] = ""

    st.success("Your answers have been cleared! 🧹")

# -----------------------------
# SHOW SAVED ANSWERS
# -----------------------------
st.subheader("📋 Your Saved Answers")

df_current = pd.read_csv(DATA_FILE)
df_user = df_current[df_current["user"] == user_name]

if not df_user.empty:
    st.dataframe(df_user)
else:
    st.info("No saved answers yet.")

# -----------------------------
# COMPARE
# -----------------------------
if st.button("💖 See Our Match"):
    df = pd.read_csv(DATA_FILE)

    users = df["user"].unique()

    if len(users) < 2:
        st.warning("Waiting for both of you to answer...")
    else:
        user1, user2 = users[:2]

        results = []
        score = 0

        for q in questions:
            a1 = df[(df["user"] == user1) & (df["question"] == q)]["answer"].values
            a2 = df[(df["user"] == user2) & (df["question"] == q)]["answer"].values

            a1 = a1[0].strip().lower() if len(a1) else ""
            a2 = a2[0].strip().lower() if len(a2) else ""

            match = a1 == a2 and a1 != ""

            if match:
                score += 1

            results.append({
                "Question": q,
                user1: a1,
                user2: a2,
                "Match": "✅" if match else "❌"
            })

        st.subheader(f"💯 Match Score: {score} / {len(questions)}")

        df_results = pd.DataFrame(results)
        st.dataframe(df_results)

        # -----------------------------
        # FEEDBACK
        # -----------------------------
        if score == len(questions):
            st.success("🔥 Perfect Match! Soulmates!")
        elif score > len(questions) // 2:
            st.info("💛 Strong connection!")
        else:
            st.warning("😂 Keep learning each other!")

        st.balloons()