import streamlit as st
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import datetime

from translations.translations import TEXTS



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
language = st.selectbox('Choose your language / اختر لغتك', ['en', 'ar'])
# If the selected language is Arabic, apply right-to-left text direction
if language == 'ar':
    st.markdown("""
        <style>
            * {
                direction: rtl;
            }
        </style>
    """, unsafe_allow_html=True)
texts = TEXTS[language]
st.title(texts['title'])

if(st.button(texts['next'])):
    st.session_state.step += 1
    if(st.session_state.step == 2):
        st.session_state.last_next_was_clicked = True

if st.session_state.step:
    if st.button(texts['back']):
        st.session_state.step -= 1
progress_bar = st.progress(st.session_state.step / 3)



if st.session_state.step == 0:
    st.header(texts['welcome_header'])
    st.write(texts['click_start'])

        

elif st.session_state.step == 1:

    st.header(texts['basic_info_header'])
    st.session_state.weight = st.number_input(texts['enter_weight'], value=st.session_state.weight, min_value=0.0)
    st.session_state.body_fat_percentage = st.number_input(texts['enter_body_fat'], value=st.session_state.body_fat_percentage, min_value=0.0, max_value=100.0)
    lbm = calculate_lbm(st.session_state.weight, st.session_state.body_fat_percentage)
    st.write(f"{texts['your_lbm']} {lbm:.2f} kg")
    

elif st.session_state.step == 2:
    st.header(texts['calculate_energy_header'])
    st.session_state.has_smartwatch = st.radio(texts['have_smartwatch'], ["Yes", "No"], index=0 if st.session_state.has_smartwatch == "Yes" else 1)

    if st.session_state.has_smartwatch == "Yes":
        st.session_state.resting_energy = st.number_input(texts['enter_resting_energy'], value=st.session_state.resting_energy, min_value=0.0)
        st.session_state.active_energy = st.number_input(texts['enter_active_energy'], value=st.session_state.active_energy, min_value=0.0)
    else:
        st.session_state.height = st.number_input(texts['enter_height'], value=st.session_state.height, min_value=0.0)
        st.session_state.age = st.number_input(texts['enter_age'], value=st.session_state.age, min_value=0)
        st.session_state.sex = st.radio(texts['select_sex'], ["Male", "Female"], index=0 if st.session_state.sex == "Male" else 1)
        st.session_state.activity_level = st.selectbox(texts['select_activity_level'], [
            'Sedentary (little to no exercise)',
            'Lightly active (light exercise/sports 1-3 days/week)',
            'Moderately active (moderate exercise/sports 3-5 days/week)',
            'Very active (hard exercise/sports 6-7 days a week)',
            'Super active (very hard exercise, physical job, or training twice a day)'
        ], index=['Sedentary (little to no exercise)', 'Lightly active (light exercise/sports 1-3 days/week)', 'Moderately active (moderate exercise/sports 3-5 days/week)', 'Very active (hard exercise/sports 6-7 days a week)', 'Super active (very hard exercise, physical job, or training twice a day)'].index(st.session_state.activity_level))



elif st.session_state.step == 3:
    st.header(texts["macronutrient_distribution_header"])
    st.session_state.calorie_deficit = st.slider(texts['reduce_daily_intake'], value=st.session_state.calorie_deficit, min_value=0, max_value=500)
    st.session_state.protein_factor = st.slider(texts['include_protein'], value=st.session_state.protein_factor, min_value=1.6, max_value=3.4)
    if st.button(texts['hint_protein_intake']):
        st.write(texts['protein_hint_text'])
    st.session_state.fat_factor = st.slider(texts['daily_intake_fat'], value=int(st.session_state.fat_factor), min_value=20, max_value=35)
    

    if st.session_state.has_smartwatch == "Yes":
        tdee = st.session_state.resting_energy + st.session_state.active_energy
    else:
        tdee = calculate_tdee(st.session_state.height, st.session_state.weight, st.session_state.age, st.session_state.sex, st.session_state.activity_level)
    
    lbm = calculate_lbm(st.session_state.weight, st.session_state.body_fat_percentage)
    adjusted_tdee = tdee - st.session_state.calorie_deficit

    protein = lbm * st.session_state.protein_factor
    fat = tdee * st.session_state.fat_factor / 100 / 9
    carbs = (adjusted_tdee - (protein * 4 + fat * 9)) / 4

    st.write(f"{texts['consume_daily']} {adjusted_tdee:.2f} {texts['kcal_daily']}.")
    st.write(f"{texts['protein']}: {protein:.2f} {texts['g']}") 
    st.write(f"{texts['fat']} {fat:.2f} {texts['g']}")
    st.write(f"{texts['carbohydrates']} {carbs:.2f} {texts['g']}")

    fig, ax = plt.subplots()
    ax.axis('off')
    ax.text(0.5, 0.8, f"Recommended Daily Intake: {adjusted_tdee:.2f} kcal", ha='center')
    ax.text(0.5, 0.6, f"Protein: {protein:.2f} g", ha='center')
    ax.text(0.5, 0.4, f"Fat: {fat:.2f} g", ha='center')
    ax.text(0.5, 0.2, f"Carbohydrates: {carbs:.2f} g", ha='center')
    st.pyplot(fig)
    
    # Add an "Export as PNG" button
    if st.button(texts['export_as_png']):
        # add the data of today as Wed 09/09/2020
        todayDate = datetime.date.today().strftime("%a %d/%m/%Y")
        fig.text(0.5, 0.05, f"Generated on {todayDate}", ha='center')
        fileName = f"calorie_info_{todayDate}.png"
        st.markdown(get_image_download_link(fig, fileName, texts['click_here_to_download']), unsafe_allow_html=True)
        st.write(texts['macronutrient_info_saved'])
    


progress_bar.progress(st.session_state.step / 3)

