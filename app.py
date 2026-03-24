import streamlit as st

st.set_page_config(page_title="Health Companion", layout="centered")

st.title("🧠 Personal Health Companion")
st.markdown("### Your Smart Fitness & Health Assistant")

# --- INPUT SECTION ---
st.sidebar.header("User Profile")

name = st.sidebar.text_input("Name")
age = st.sidebar.number_input("Age", 10, 80)
weight = st.sidebar.number_input("Weight (kg)", 30.0, 150.0)
height = st.sidebar.number_input("Height (cm)", 120.0, 220.0)
goal = st.sidebar.selectbox("Goal", ["Gain Muscle", "Lose Weight", "Maintain"])

# --- BUTTON ---
if st.sidebar.button("Generate Plan"):

    # --- BMI ---
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    # --- PROTEIN ---
    if goal == "Gain Muscle":
        protein = weight * 1.6
    elif goal == "Lose Weight":
        protein = weight * 1.2
    else:
        protein = weight * 1.3

    # --- UI SECTIONS ---
    st.subheader(f"Hello {name}, here is your plan 👇")

    # --- BMI Section ---
    st.markdown("## 📊 Health Analysis")

    if bmi < 18.5:
        status = "Underweight"
        st.warning(f"BMI: {bmi:.1f} ({status})")
    elif bmi < 25:
        status = "Normal"
        st.success(f"BMI: {bmi:.1f} ({status})")
    elif bmi < 30:
        status = "Overweight"
        st.warning(f"BMI: {bmi:.1f} ({status})")
    else:
        status = "Obese"
        st.error(f"BMI: {bmi:.1f} ({status})")

    # --- Nutrition ---
    st.markdown("## 🍗 Nutrition Plan")
    st.write(f"Daily Protein Needed: **{protein:.1f} grams**")

    if goal == "Gain Muscle":
        st.write("• Eggs, Chicken, Paneer, Milk, Rice")
    elif goal == "Lose Weight":
        st.write("• Vegetables, Fruits, Oats, Lean Protein")
    else:
        st.write("• Balanced diet with protein, carbs, fats")

    # --- Workout ---
    st.markdown("## 🏋️ Workout Plan")

    if goal == "Gain Muscle":
        st.write("• Strength training (4 days/week)")
        st.write("• Focus: Chest, Back, Legs")
    elif goal == "Lose Weight":
        st.write("• Cardio (5 days/week)")
        st.write("• Light strength training")
    else:
        st.write("• Mix of cardio + strength")

    # --- Health Score ---
    st.markdown("## 🧠 Health Score")

    score = 100

    if bmi < 18.5 or bmi > 30:
        score -= 20
    if protein < weight:
        score -= 10

    st.progress(score)
    st.write(f"Health Score: {score}/100")

    # --- Smart Tip ---
    st.markdown("## 💡 Smart Recommendation")

    if bmi < 18.5:
        st.info("Focus on calorie surplus and strength training.")
    elif bmi > 25:
        st.info("Focus on fat loss with cardio + clean diet.")
    else:
        st.info("Maintain your current lifestyle with consistency.")

# --- Footer ---
st.markdown("---")
st.caption("Future: Lab Tests | Grocery | Insurance | AI Health Assistant")
