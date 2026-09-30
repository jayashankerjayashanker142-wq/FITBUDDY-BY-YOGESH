"""
FitBuddy - AI Fitness Plan Generator
Generative AI with Google | Powered by Gemini models
Run:  streamlit run app.py
"""

import os
import streamlit as st
from google import genai

# ---------------------------------------------------------------- CONFIG
MODEL_NAME = "gemini-3.5-flash-lite"   # fast + free-tier friendly

st.set_page_config(page_title="FitBuddy - AI Fitness Planner", page_icon="💪", layout="wide")


# ---------------------------------------------------------------- HELPERS
def get_client(api_key: str):
    return genai.Client(api_key=api_key)


def calc_bmi(weight_kg: float, height_cm: float) -> float:
    return weight_kg / ((height_cm / 100) ** 2)


def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def calc_bmr(gender: str, weight: float, height: float, age: int) -> float:
    """Mifflin-St Jeor equation."""
    base = 10 * weight + 6.25 * height - 5 * age
    return base + 5 if gender == "Male" else base - 161


ACTIVITY_FACTORS = {
    "Sedentary (little/no exercise)": 1.2,
    "Lightly active (1-3 days/week)": 1.375,
    "Moderately active (3-5 days/week)": 1.55,
    "Very active (6-7 days/week)": 1.725,
}


def build_prompt(d: dict) -> str:
    return f"""
You are FitBuddy, a certified-style AI fitness and nutrition coach.
Create a personalised, SAFE and realistic {d['weeks']}-week fitness plan.

USER PROFILE
- Name: {d['name']}
- Age: {d['age']}, Gender: {d['gender']}
- Height: {d['height']} cm, Weight: {d['weight']} kg
- BMI: {d['bmi']:.1f} ({d['bmi_cat']})
- Estimated maintenance calories (TDEE): {d['tdee']:.0f} kcal/day
- Goal: {d['goal']}
- Fitness level: {d['level']}
- Workout days per week: {d['days']}
- Equipment available: {d['equipment']}
- Diet preference: {d['diet']}
- Health issues / injuries: {d['health'] or 'None'}

OUTPUT FORMAT (use clean Markdown):
1. **Profile Summary** - 3-4 lines, including calorie target and macro split (protein/carbs/fat in grams).
2. **Weekly Workout Schedule** - a table: Day | Focus | Exercises (sets x reps) | Duration.
3. **Warm-up & Cool-down** routine.
4. **Sample 1-Day Meal Plan** matching the diet preference (Breakfast, Lunch, Snack, Dinner) with approx calories.
5. **Weekly Progression** - how to increase difficulty across the {d['weeks']} weeks.
6. **Hydration, Sleep & Recovery tips**.
7. **Safety notes** - mention to consult a doctor if the user has any health issue.

RULES
- Never suggest extreme diets or calorie targets below safe limits.
- Adapt exercises to the equipment and injuries listed.
- Keep the tone motivating and friendly. Address the user by name.
""".strip()


def generate_plan(client, prompt: str) -> str:
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return response.text


# ---------------------------------------------------------------- SIDEBAR
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Get a free key at https://aistudio.google.com/apikey",
    )
    st.caption(f"Model: `{MODEL_NAME}`")
    st.markdown("---")
    st.info("⚠️ FitBuddy gives general guidance only. Consult a doctor/trainer before starting any program.")

# ---------------------------------------------------------------- MAIN UI
st.title("💪 FitBuddy – AI Fitness Plan Generator")
st.caption("Generative AI with Google • Powered by Gemini")

with st.form("profile_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.text_input("Name", "Friend")
        age = st.number_input("Age", 13, 80, 20)
        gender = st.selectbox("Gender", ["Male", "Female"])
    with c2:
        height = st.number_input("Height (cm)", 120, 220, 170)
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 65.0)
        activity = st.selectbox("Current activity level", list(ACTIVITY_FACTORS))
    with c3:
        goal = st.selectbox("Goal", ["Weight loss", "Muscle gain", "Maintain fitness",
                                     "Improve stamina / endurance", "Flexibility & mobility"])
        level = st.selectbox("Fitness level", ["Beginner", "Intermediate", "Advanced"])
        days = st.slider("Workout days / week", 2, 7, 4)

    c4, c5 = st.columns(2)
    with c4:
        equipment = st.selectbox("Equipment", ["No equipment (home)", "Dumbbells / resistance bands", "Full gym"])
        diet = st.selectbox("Diet preference", ["Vegetarian", "Non-vegetarian", "Vegan", "Eggetarian"])
    with c5:
        weeks = st.selectbox("Plan duration (weeks)", [4, 8, 12], index=0)
        health = st.text_area("Health issues / injuries (optional)", placeholder="e.g. knee pain, asthma")

    submitted = st.form_submit_button("🚀 Generate My Plan")

if submitted:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
        st.stop()

    bmi = calc_bmi(weight, height)
    bmr = calc_bmr(gender, weight, height, age)
    tdee = bmr * ACTIVITY_FACTORS[activity]

    m1, m2, m3 = st.columns(3)
    m1.metric("BMI", f"{bmi:.1f}", bmi_category(bmi))
    m2.metric("BMR (kcal)", f"{bmr:.0f}")
    m3.metric("TDEE (kcal)", f"{tdee:.0f}")

    data = dict(name=name, age=age, gender=gender, height=height, weight=weight,
                bmi=bmi, bmi_cat=bmi_category(bmi), tdee=tdee, goal=goal, level=level,
                days=days, equipment=equipment, diet=diet, health=health, weeks=weeks)

    try:
        with st.spinner("FitBuddy is creating your plan..."):
            client = get_client(api_key)
            plan = generate_plan(client, build_prompt(data))
        st.session_state["plan"] = plan
        st.session_state["client_key"] = api_key
    except Exception as e:
        st.error(f"Error while calling Gemini: {e}")

if "plan" in st.session_state:
    st.markdown("---")
    st.subheader("📋 Your Personalised Plan")
    st.markdown(st.session_state["plan"])

    st.download_button("⬇️ Download Plan (.md)", st.session_state["plan"],
                       file_name="fitbuddy_plan.md", mime="text/markdown")

    st.markdown("---")
    st.subheader("💬 Ask FitBuddy to tweak it")
    tweak = st.text_input("e.g. 'Make it 30 minutes per day' or 'Replace paneer with tofu'")
    if st.button("Update Plan") and tweak:
        try:
            client = get_client(st.session_state["client_key"])
            new_prompt = (f"Here is an existing fitness plan:\n\n{st.session_state['plan']}\n\n"
                          f"Modify it as per this request: {tweak}\n"
                          "Return the full updated plan in the same Markdown format and keep it safe.")
            with st.spinner("Updating..."):
                st.session_state["plan"] = generate_plan(client, new_prompt)
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
