import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Health Companion", layout="centered")

st.title("🧠 Personal Health Companion")

# --- INPUT ---
name = st.text_input("Name")
weight = st.number_input("Weight (kg)", 30.0, 150.0)
height = st.number_input("Height (cm)", 120.0, 220.0)
goal = st.selectbox("Goal", ["Gain Muscle", "Lose Weight", "Maintain"])

file = "data.csv"

# --- BUTTON ---
if st.button("Save & Generate Plan"):

    # Save data
    new_data = pd.DataFrame([{
        "name": name,
        "weight": weight,
        "goal": goal,
        "date": datetime.now()
    }])

    new_data.to_csv(file, mode='a', header=False, index=False)

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

# --- HISTORY ---
st.markdown("## 📈 Progress Tracking")

if os.path.exists(file):
    df = pd.read_csv(file)

    if not df.empty:
        st.line_chart(df["weight"])
        st.dataframe(df)
