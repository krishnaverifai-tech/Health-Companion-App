import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- DB SETUP ---
conn = sqlite3.connect("health.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS records (
    username TEXT,
    weight REAL,
    goal TEXT,
    date TEXT
)
""")

conn.commit()

st.set_page_config(page_title="Health Companion", layout="centered")

st.title("🧠 Personal Health Companion")

# --- LOGIN ---
st.sidebar.header("Login")
username = st.sidebar.text_input("Enter Username")

if username:

    st.sidebar.success(f"Logged in as {username}")

    # --- INPUT ---
    weight = st.number_input("Weight (kg)", 30.0, 150.0)
    height = st.number_input("Height (cm)", 120.0, 220.0)
    goal = st.selectbox("Goal", ["Gain Muscle", "Lose Weight", "Maintain"])

    if st.button("Save & Generate Plan"):

        # Save data
        c.execute("INSERT INTO records VALUES (?, ?, ?, ?)",
                  (username, weight, goal, str(datetime.now())))
        conn.commit()

        # BMI
        bmi = weight / ((height/100) ** 2)

        st.subheader("📊 Health Report")
        st.write(f"BMI: {bmi:.1f}")

        if bmi < 18.5:
            st.warning("Underweight")
        elif bmi < 25:
            st.success("Normal")
        else:
            st.error("Overweight")

        # Protein
        protein = weight * 1.5
        st.write(f"Protein Needed: {protein:.1f}g")

    # --- USER HISTORY ---
    st.markdown("## 📈 Your Progress")

    df = pd.read_sql_query(
        f"SELECT * FROM records WHERE username='{username}'", conn)

    if not df.empty:
        st.line_chart(df["weight"])
        st.dataframe(df)

else:
    st.warning("Please enter a username to continue")
