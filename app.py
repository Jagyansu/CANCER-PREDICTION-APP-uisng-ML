import streamlit as st
import sklearn
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import KNeighborsClassifier
import pickle

# Load model
model = pickle.load(open('canpre.pkl', 'rb'))

# Page configuration
st.set_page_config(page_title="Cancer Prediction App", page_icon="🩺", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        body { background-color: #f4f4f4; }
        .title-container { display: flex; justify-content: center; align-items: center; flex-direction: column; width: 100%; }
        .title { text-align: center; color: #4CAF50; font-size: 4em; font-weight: bold; }
        .subtext { text-align: center; font-size: 1.2em; color: #555; }
        .stButton>button { background-color: #4CAF50; color: white; font-size: 1.2em; padding: 10px 24px; border-radius: 12px; }
        .stButton>button:hover { background-color: #45a049; }
        .footer { text-align: center; padding: 10px; margin-top: 20px; color: #555; }
        .red-text { color: red; }
        .logo-container { display: flex; justify-content: center; align-items: center; width: 100%; }
        .logo-container img { border: 3px solid black; border-radius: 12px; padding: 5px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3); margin: auto; display: block; }
        .input-section { border: 2px solid #ddd; border-radius: 12px; padding: 20px; margin: 10px; background-color: #fff; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); }
    </style>
    """,
    unsafe_allow_html=True
)

# Header section
st.markdown("<div class='title-container'>", unsafe_allow_html=True)
st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
st.image(r"innomatics_logo.png", width=700)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='title'><span class='red-text'>Cancer</span> Prediction</div>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Fill out the form below to predict cancer likelihood</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Input sections without sidebar
col1, col2 = st.columns(2)

with col1:
    st.header("🩺 Medical History")
    Tumor_Size = st.number_input('🧬 Tumor Size (cm):', min_value=0.1, max_value=100.0, step=0.1)
    Tumor_Grade = st.selectbox('🏷️ Tumor Grade', ['High', 'Low', 'Medium'])      
    Symptoms_Severity = st.selectbox('📊 Symptoms Severity', ['Mild', 'Moderate', 'Severe'])
    Family_History = st.selectbox('👪 Family History of Cancer', ['Yes', 'No'])

    
with col2:

    st.header("🧑 Personal Information")
    def get_Age_color(age):
        if age <= 12:
            return "#00FF00", "Inborn/Child"
        elif age <= 30:
            return "#33CC33", "Young Adult"
        elif age <= 50:
            return "#FFFF00", "Adult"
        elif age <= 70:
            return "#FF9900", "Middle Age"
        else:
            return "#FF0000", "Old Age"

    Age = st.slider("Age", min_value=1, max_value=120, value=25)
    age_color, age_group = get_Age_color(Age)
    st.markdown(
        f'<div style="background-color:{age_color}; color:black; padding:10px; text-align:center; border-radius:12px;">'
        f'<b>Age Group: {age_group} ({Age} years)</b></div>',
        unsafe_allow_html=True
)
    Gender_options = {
        "♂️ Male": ("Male", "#4CAF50"),
        "♀️ Female": ("Female", "#FF69B4")
    }
    Gender = st.radio(
        "⚧️ Gender",
        list(Gender_options.keys()),
        horizontal=True
    )
    Smoking_History = st.selectbox('🚬 Smoking History', ['Former Smoker', 'Current Smoker', 'Non-Smoker'])
    Alcohol_Consumption = st.selectbox('🍷 Alcohol Consumption', ['Moderate', 'High', 'Low'])
    Exercise_Frequency = st.selectbox('🏃 Exercise Frequency', ['Regularly', 'Rarely', 'Occasionally', 'Never'])

    
# Submit button
if st.button("Predict 🧑‍⚕️"):
    prediction = model.predict([[Age, Gender, Tumor_Size, Tumor_Grade, Symptoms_Severity, Family_History, Smoking_History, Alcohol_Consumption, Exercise_Frequency]])[0]
    st.markdown("<hr>", unsafe_allow_html=True)

    if prediction == 0:
        st.success("🎉Cancer is NOT detected. Stay healthy and take care! 🥳", icon="✅")
    elif prediction == 1:
        st.error("⚠️ Cancer is detected. Please consult a medical professional immediately. 🙏", icon="❌")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Powered by Jagyansu Padhy 🚀</p>", unsafe_allow_html=True)
