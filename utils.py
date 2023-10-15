import base64
from io import BytesIO
import base64




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


def get_pdf_download_link(pdf_path, file_label):
    """Generate a link to download the pdf at `pdf_path`."""
    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()
    b64 = base64.b64encode(pdf_data).decode()
    download_link = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_label}.pdf">Download PDF تحميل الملف</a>'
    return download_link
