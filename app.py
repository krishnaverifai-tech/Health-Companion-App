import streamlit as st

st.title("Personal Health Companion")

name = st.text_input("Enter your name")
weight = st.number_input("Enter your weight (kg)", 30.0, 150.0)
goal = st.selectbox("Goal", ["Gain Muscle", "Lose Weight"])

if st.button("Generate Plan"):

    protein = weight * 1.5

    st.subheader(f"Hello {name}")

    st.write(f"Daily Protein Needed: {protein:.1f} grams")

    if goal == "Gain Muscle":
        st.write("Eat: Eggs, Chicken, Rice, Milk")
        st.write("Workout: Strength training")
    else:
        st.write("Eat: Vegetables, Fruits, Oats")
        st.write("Workout: Cardio + Light weights")
