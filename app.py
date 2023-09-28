import streamlit as st
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import datetime



# Utility function to manage session state
def _get_state():
    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.weight = 0.0
        st.session_state.body_fat_percentage = 0.0
        st.session_state.has_smartwatch = "No"
        st.session_state.resting_energy = 0.0
        st.session_state.active_energy = 0.0
        st.session_state.height = 0.0
        st.session_state.age = 0
        st.session_state.sex = "Male"
        st.session_state.activity_level = 'Sedentary (little to no exercise)'
        st.session_state.calorie_deficit = 0
        st.session_state.protein_factor = 1.6
        st.session_state.fat_factor = 20.0


def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.savefig(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Function to calculate Lean Body Mass
def calculate_lbm(weight, body_fat_percentage):
    return weight * (1 - body_fat_percentage / 100)

# Function to calculate Total Daily Energy Expenditure
def calculate_tdee(height, weight, age, sex, activity_level):
    if sex == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    activity_multipliers = {
        'Sedentary (little to no exercise)': 1.2,
        'Lightly active (light exercise/sports 1-3 days/week)': 1.375,
        'Moderately active (moderate exercise/sports 3-5 days/week)': 1.55,
        'Very active (hard exercise/sports 6-7 days a week)': 1.725,
        'Super active (very hard exercise, physical job, or training twice a day)': 1.9
    }
    
    return bmr * activity_multipliers[activity_level]

# Main app
_get_state()

st.title("Calories and Macros Calculator")
progress_bar = st.progress(st.session_state.step / 4)

if st.session_state.step == 0:
    st.header("Welcome to the Calorie and Macronutrient Calculator!")
    st.write("Click 'Start' to begin.")
    if st.button("Start"):
        st.session_state.step = 1
        

elif st.session_state.step == 1:
    st.header("Basic Information")
    st.session_state.weight = st.number_input("Enter your weight (kg)", value=st.session_state.weight, min_value=0.0)
    st.session_state.body_fat_percentage = st.number_input("Enter your body fat percentage (%)", value=st.session_state.body_fat_percentage, min_value=0.0, max_value=100.0)
    lbm = calculate_lbm(st.session_state.weight, st.session_state.body_fat_percentage)
    st.write(f"Your lean body mass is {lbm:.2f} kg")
    if st.button("Next_1"):
        st.session_state.step += 1
    if st.session_state.step > 0 and st.button("Back_1"):
        st.session_state.step -= 1

elif st.session_state.step == 2:
    st.header("Calculate Your Energy Expenditure")
    st.session_state.has_smartwatch = st.radio("Do you have a smartwatch?", ["Yes", "No"], index=0 if st.session_state.has_smartwatch == "Yes" else 1)

    if st.session_state.has_smartwatch == "Yes":
        st.session_state.resting_energy = st.number_input("Enter your Resting Energy (kcal)", value=st.session_state.resting_energy, min_value=0.0)
        st.session_state.active_energy = st.number_input("Enter your Active Energy (kcal)", value=st.session_state.active_energy, min_value=0.0)
    else:
        st.session_state.height = st.number_input("Enter your height (cm)", value=st.session_state.height, min_value=0.0)
        st.session_state.age = st.number_input("Enter your age", value=st.session_state.age, min_value=0)
        st.session_state.sex = st.radio("Select your sex", ["Male", "Female"], index=0 if st.session_state.sex == "Male" else 1)
        st.session_state.activity_level = st.selectbox("Select your activity level", [
            'Sedentary (little to no exercise)',
            'Lightly active (light exercise/sports 1-3 days/week)',
            'Moderately active (moderate exercise/sports 3-5 days/week)',
            'Very active (hard exercise/sports 6-7 days a week)',
            'Super active (very hard exercise, physical job, or training twice a day)'
        ], index=['Sedentary (little to no exercise)', 'Lightly active (light exercise/sports 1-3 days/week)', 'Moderately active (moderate exercise/sports 3-5 days/week)', 'Very active (hard exercise/sports 6-7 days a week)', 'Super active (very hard exercise, physical job, or training twice a day)'].index(st.session_state.activity_level))

    if st.button("Next_2"):
        st.session_state.step += 1
    if st.session_state.step > 0 and st.button("Back_2"):
        st.session_state.step -= 1

elif st.session_state.step == 3:
    st.header("Macronutrient Distribution")
    st.session_state.calorie_deficit = st.slider("How much do you want to reduce your daily intake? (kcal)", value=st.session_state.calorie_deficit, min_value=0, max_value=500)
    st.session_state.protein_factor = st.slider("How much protein do you want to include? (g per kg of LBM)", value=st.session_state.protein_factor, min_value=1.6, max_value=3.4)
    if st.button("Need a hint for protein intake?"):
        st.write("""
        - Maintenance or moderate activity: 1.6 to 2.2 g/kg of LBM
        - High-intensity training or muscle gain goals: 2.2 to 3.4 g/kg of LBM
        """)
    st.session_state.fat_factor = st.slider("What percentage of your daily intake should be fat?", value=int(st.session_state.fat_factor), min_value=20, max_value=35)
    

    if st.session_state.has_smartwatch == "Yes":
        tdee = st.session_state.resting_energy + st.session_state.active_energy
    else:
        tdee = calculate_tdee(st.session_state.height, st.session_state.weight, st.session_state.age, st.session_state.sex, st.session_state.activity_level)
    
    lbm = calculate_lbm(st.session_state.weight, st.session_state.body_fat_percentage)
    adjusted_tdee = tdee - st.session_state.calorie_deficit

    protein = lbm * st.session_state.protein_factor
    fat = tdee * st.session_state.fat_factor / 100 / 9
    carbs = (adjusted_tdee - (protein * 4 + fat * 9)) / 4

    st.write(f"You should consume {adjusted_tdee:.2f} kcal daily.")
    st.write(f"Protein: {protein:.2f} g")
    st.write(f"Fat: {fat:.2f} g")
    st.write(f"Carbohydrates: {carbs:.2f} g")

    fig, ax = plt.subplots()
    ax.axis('off')
    ax.text(0.5, 0.8, f"Recommended Daily Intake: {adjusted_tdee:.2f} kcal", ha='center')
    ax.text(0.5, 0.6, f"Protein: {protein:.2f} g", ha='center')
    ax.text(0.5, 0.4, f"Fat: {fat:.2f} g", ha='center')
    ax.text(0.5, 0.2, f"Carbohydrates: {carbs:.2f} g", ha='center')
    st.pyplot(fig)
    
    # Add an "Export as PNG" button
    if st.button("Export as PNG"):
        # add the data of today as Wed 09/09/2020
        todayDate = datetime.date.today().strftime("%a %d/%m/%Y")
        fig.text(0.5, 0.05, f"Generated on {todayDate}", ha='center')
        fileName = f"calorie_info_{todayDate}.png"
        st.markdown(get_image_download_link(fig, fileName, "Click here to download"), unsafe_allow_html=True)
        st.write("Macronutrient information has been saved as 'macronutrient_info.png'")
    
    if st.button("Finish"):
        st.session_state.step = 0
    if st.session_state.step > 0 and st.button("Back_3"):
        st.session_state.step -= 1

progress_bar.progress(st.session_state.step / 4)
