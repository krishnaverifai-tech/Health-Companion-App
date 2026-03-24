import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- DB SETUP ---
conn = sqlite3.connect("health.db", check_same_thread=False)
c = conn.cursor()

# Users table
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

# Records table
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

# --- AUTH MODE ---
menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

# ---------------- REGISTER ----------------
if menu == "Register":
    st.subheader("Create Account")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Register"):
        c.execute("SELECT * FROM users WHERE username=?", (new_user,))
        if c.fetchone():
            st.error("User already exists")
        else:
            c.execute("INSERT INTO users VALUES (?, ?)", (new_user, new_pass))
            conn.commit()
            st.success("Account created successfully")

# ---------------- LOGIN ----------------
elif menu == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()

        if result:
            st.success(f"Welcome {username}")

            # --- APP FEATURES ---
            weight = st.number_input("Weight (kg)", 30.0, 150.0)
            height = st.number_input("Height (cm)", 120.0, 220.0)
            goal = st.selectbox("Goal", ["Gain Muscle", "Lose Weight", "Maintain"])

            if st.button("Save Data"):

                c.execute("INSERT INTO records VALUES (?, ?, ?, ?)",
                          (username, weight, goal, str(datetime.now())))
                conn.commit()

                bmi = weight / ((height/100) ** 2)

                st.write(f"BMI: {bmi:.1f}")

            # --- USER HISTORY ---
            st.markdown("## 📈 Your Progress")

            df = pd.read_sql_query(
                f"SELECT * FROM records WHERE username='{username}'", conn)

            if not df.empty:
                st.line_chart(df["weight"])
                st.dataframe(df)

        else:
            st.error("Invalid username or password")
