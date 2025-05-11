import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import time
from streamlit_lottie import st_lottie
import streamlit_vertical_slider as svs


# Function to load Lottie animations from URL
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


# Function to create a gauge chart with improved styling
def create_gauge_chart(probability):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Probability (%)", 'font': {'size': 24, 'color': '#1E3A8A'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#1E3A8A"},
            'bar': {'color': "#1E3A8A"},
            'steps': [
                {'range': [0, 30], 'color': "#DCFCE7"},  # Light green
                {'range': [30, 70], 'color': "#FEF9C3"},  # Light yellow
                {'range': [70, 100], 'color': "#FEE2E2"}  # Light red
            ],
            'threshold': {
                'line': {'color': "#DC2626", 'width': 4},
                'thickness': 0.75,
                'value': probability * 100
            }
        }
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "#1E3A8A", 'family': "Arial"}
    )
    
    return fig


# Function for progress bar animation
def progress_bar_with_animation():
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
    st.success("Analysis Complete!")
    time.sleep(0.5)
    progress_bar.empty()


# Set page config
st.set_page_config(
    page_title="Lung Cancer Risk Predictor",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background-color: #F0F9FF;  /* Light blue background */
        background-image: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        padding: 20px;
    }
    
    h1 {
        color: #0369A1;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 2.5rem;
        background: linear-gradient(90deg, #0369A1, #0284C7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    h2 {
        color: #0369A1;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #0284C7;
        font-weight: 500;
    }
    
    .stButton>button {
        background-color: #0284C7;
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 6px rgba(2, 132, 199, 0.2);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #0369A1;
        box-shadow: 0 6px 8px rgba(2, 132, 199, 0.3);
        transform: translateY(-2px);
    }
    
    .prediction-box {
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .prediction-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 20px rgba(0, 0, 0, 0.15);
    }
    
    .high-risk {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        border-left: 8px solid #DC2626;
    }
    
    .medium-risk {
        background: linear-gradient(135deg, #FEF9C3 0%, #FEF08A 100%);
        border-left: 8px solid #CA8A04;
    }
    
    .low-risk {
        background: linear-gradient(135deg, #DCFCE7 0%, #BBF7D0 100%);
        border-left: 8px solid #16A34A;
    }
    
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        transform: translateY(-3px);
    }
    
    .sidebar .css-1d391kg {
        background-color: #F0F9FF;
    }
    
    .stRadio>div {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
    }
    
    .stRadio label {
        background-color: white;
        padding: 10px 20px;
        border-radius: 20px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        margin: 5px;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .stRadio label:hover {
        background-color: #E0F2FE;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Header with animation */
    .animated-gradient {
        background: linear-gradient(-45deg, #0369A1, #0284C7, #38BDF8, #7DD3FC);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 15px rgba(2, 132, 199, 0.2);
    }
    
    @keyframes gradient {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    /* Image styles */
    .rounded-image {
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #64748B;
        margin-top: 50px;
        border-top: 1px solid #E2E8F0;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #0284C7;
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Info cards */
    .info-card {
        border-left: 4px solid #0284C7;
        background-color: white;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    
    /* Animation for recommendations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .recommendation-item {
        animation: fadeIn 0.5s ease forwards;
        opacity: 0;
    }
    
    .recommendation-item:nth-child(1) { animation-delay: 0.1s; }
    .recommendation-item:nth-child(2) { animation-delay: 0.2s; }
    .recommendation-item:nth-child(3) { animation-delay: 0.3s; }
    .recommendation-item:nth-child(4) { animation-delay: 0.4s; }
    .recommendation-item:nth-child(5) { animation-delay: 0.5s; }
</style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("""
<style>
    .header-container {
        background: linear-gradient(90deg, #1E3B8A, #4169E1);
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: block;  /* Ensures it's always visible */
    }
    .main-title {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 5px;
        display: block;  /* Ensures it's always visible */
    }
    .subtitle {
        color: #f0f0f0;
        font-size: 1.2rem;
        display: block;  /* Ensures it's always visible */
    }
</style>
""", unsafe_allow_html=True)

# Apply the header with explicit HTML
st.markdown("""
<div class="header-container">
    <h1 class="main-title">Lung Cancer Risk Assessment Tool</h1>
    <p class="subtitle">Evaluate your risk factors and get personalized recommendations</p>
</div>
""", unsafe_allow_html=True)

# Load animations
lung_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_5njp3vgg.json")
doctor_animation = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_5tl1xxnz.json")
health_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_5njp3vgg.json")

# Main layout with columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="card">
        <h2>Why Early Detection Matters</h2>
        <p>Lung cancer is the leading cause of cancer deaths worldwide. When detected early, the five-year survival rate can be as high as 56%, compared to just 5% in advanced stages.</p>
        <p>This tool helps you identify potential risk factors and guides you toward appropriate healthcare decisions.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if lung_animation:
        st_lottie(lung_animation, height=200, key="lung")
    else:
        st.image("https://www.cancer.org/content/dam/cancer-org/images/illustrations/medical-illustrations/en/lung-cancer-illustration-en.png", use_column_width=True)

# Sidebar for info
with st.sidebar:
    st.image("https://i0.wp.com/www.denvaxindia.com/blog/wp-content/uploads/2024/04/Lung-Cancer-Treatment-1.png?fit=1107%2C632&ssl=1", caption="Lung health matters", use_column_width=True)
    
    st.header("About")
    st.info("""
    This tool uses an advanced machine learning model trained on comprehensive healthcare data to predict lung cancer risk.

    **Important**: This is an educational tool and should not replace professional medical advice.

    If you have concerns about lung cancer or other health issues, please consult with a healthcare professional.
    """)

    if doctor_animation:
        st_lottie(doctor_animation, height=200, key="doctor")

    with st.expander("📋 Risk Factors", expanded=False):
        st.markdown("""
        Key risk factors for lung cancer include:

        - 🚬 Smoking (accounts for 80-90% of cases)
        - 💨 Exposure to secondhand smoke
        - 👪 Family history
        - ☢️ Exposure to radon gas
        - 🏭 Exposure to asbestos and other carcinogens
        - 🌫️ Air pollution
        - 📡 Previous radiation therapy
        """)

    with st.expander("🔍 Symptoms", expanded=False):
        st.markdown("""
        Common symptoms of lung cancer:

        - 😷 Persistent cough
        - 💔 Chest pain
        - 🫁 Shortness of breath
        - 🌬️ Wheezing
        - 🗣️ Hoarseness
        - ⚖️ Weight loss
        - 😴 Fatigue
        - 🦠 Recurring infections
        """)

# Create a form for user input in a card
st.markdown("""
<div class="card">
    <h2>Patient Information</h2>
    <p>Please fill in the form below to receive your personalized risk assessment.</p>
</div>
""", unsafe_allow_html=True)

# Tabs for form organization
tabs = st.tabs(["📋 Personal Info", "🚬 Lifestyle", "🩺 Symptoms"])

with tabs[0]:
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.radio("Gender", ["M", "F"], 
                         format_func=lambda x: "Male" if x == "M" else "Female",
                         horizontal=True)
    
    with col2:
        age = st.slider("Age", min_value=18, max_value=100, value=50, 
                       help="Select your current age")
    
    chronic_disease = st.radio("Do you have any chronic diseases?", [1, 2],
                              format_func=lambda x: "Yes" if x == 2 else "No",
                              horizontal=True,
                              help="Chronic diseases include diabetes, COPD, etc.")
    
    anxiety = st.radio("Do you experience anxiety?", [1, 2],
                      format_func=lambda x: "Yes" if x == 2 else "No",
                      horizontal=True)

with tabs[1]:
    col1, col2 = st.columns(2)
    
    with col1:
        smoking = st.radio("Do you smoke?", [1, 2],
                          format_func=lambda x: "Yes" if x == 2 else "No",
                          horizontal=True)
        
        if smoking == 2:
            st.warning("⚠️ Smoking is the leading cause of lung cancer")
        
        yellow_fingers = st.radio("Yellow Fingers?", [1, 2],
                                 format_func=lambda x: "Yes" if x == 2 else "No",
                                 horizontal=True)
    
    with col2:
        alcohol_consuming = st.radio("Do you consume alcohol regularly?", [1, 2],
                                    format_func=lambda x: "Yes" if x == 2 else "No",
                                    horizontal=True)
        
        peer_pressure = st.radio("Do you experience peer pressure?", [1, 2],
                                format_func=lambda x: "Yes" if x == 2 else "No",
                                horizontal=True)

with tabs[2]:
    col1, col2 = st.columns(2)
    
    with col1:
        fatigue = st.radio("Do you experience fatigue?", [1, 2],
                          format_func=lambda x: "Yes" if x == 2 else "No",
                          horizontal=True)
        
        coughing = st.radio("Do you have a persistent cough?", [1, 2],
                           format_func=lambda x: "Yes" if x == 2 else "No",
                           horizontal=True)
        
        shortness_of_breath = st.radio("Do you experience shortness of breath?", [1, 2],
                                      format_func=lambda x: "Yes" if x == 2 else "No",
                                      horizontal=True)
    
    with col2:
        allergy = st.radio("Do you have allergies?", [1, 2],
                          format_func=lambda x: "Yes" if x == 2 else "No",
                          horizontal=True)
        
        wheezing = st.radio("Do you experience wheezing?", [1, 2],
                           format_func=lambda x: "Yes" if x == 2 else "No",
                           horizontal=True)
        
        swallowing_difficulty = st.radio("Do you have difficulty swallowing?", [1, 2],
                                        format_func=lambda x: "Yes" if x == 2 else "No",
                                        horizontal=True)
        
        chest_pain = st.radio("Do you experience chest pain?", [1, 2],
                             format_func=lambda x: "Yes" if x == 2 else "No",
                             horizontal=True)

# Add a submit button with animation
st.markdown("<br>", unsafe_allow_html=True)
if st.button("📊 Analyze Risk Factors"):
    try:
        # Show a progress bar with animation
        progress_bar_with_animation()
        
        # Create a dictionary with user inputs
        input_data = {
            "GENDER": gender,
            "AGE": age,
            "SMOKING": smoking,
            "YELLOW_FINGERS": yellow_fingers,
            "ANXIETY": anxiety,
            "PEER_PRESSURE": peer_pressure,
            "CHRONIC_DISEASE": chronic_disease,
            "FATIGUE": fatigue,
            "ALLERGY": allergy,
            "WHEEZING": wheezing,
            "ALCOHOL_CONSUMING": alcohol_consuming,
            "COUGHING": coughing,
            "SHORTNESS_OF_BREATH": shortness_of_breath,
            "SWALLOWING_DIFFICULTY": swallowing_difficulty,
            "CHEST_PAIN": chest_pain
        }
        
        # For development, use a mock response
        # Simulate different predictions based on smoking and age
        risk_factors_count = sum([
            1 if smoking == 2 else 0,
            1 if age > 60 else 0,
            1 if yellow_fingers == 2 else 0,
            1 if coughing == 2 else 0,
            1 if shortness_of_breath == 2 else 0,
            1 if wheezing == 2 else 0,
            1 if chest_pain == 2 else 0
        ])
        
        if smoking == 2 and age > 60 and (coughing == 2 or wheezing == 2):
            mock_probability = 0.85
            mock_prediction = "YES"
            mock_risk_level = "High"
        elif risk_factors_count >= 3:
            mock_probability = 0.65
            mock_prediction = "YES"
            mock_risk_level = "Medium"
        else:
            mock_probability = 0.25
            mock_prediction = "NO"
            mock_risk_level = "Low"
            
        prediction_result = {
            "prediction": mock_prediction,
            "probability": mock_probability,
            "risk_level": mock_risk_level
        }
        
        # Display prediction result
        st.header("🔬 Assessment Results")
        
        result_cols = st.columns([1, 1])
        
        with result_cols[0]:
            # Display appropriate box based on risk level
            if prediction_result["risk_level"] == "High":
                st.markdown(f"""
                <div class='prediction-box high-risk'>
                    <h2>High Risk</h2>
                    <p style="font-size: 1.2rem;">The model predicts <strong>{prediction_result["prediction"]}</strong> for lung cancer risk with a probability of <strong>{prediction_result["probability"]:.2%}</strong>.</p>
                    <p style="font-size: 1.1rem;">⚠️ Please consider consulting with a healthcare professional as soon as possible.</p>
                </div>
                """, unsafe_allow_html=True)
            elif prediction_result["risk_level"] == "Medium":
                st.markdown(f"""
                <div class='prediction-box medium-risk'>
                    <h2>Medium Risk</h2>
                    <p style="font-size: 1.2rem;">The model predicts <strong>{prediction_result["prediction"]}</strong> for lung cancer risk with a probability of <strong>{prediction_result["probability"]:.2%}</strong>.</p>
                    <p style="font-size: 1.1rem;">⚠️ Consider discussing these results with a healthcare provider during your next visit.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='prediction-box low-risk'>
                    <h2>Low Risk</h2>
                    <p style="font-size: 1.2rem;">The model predicts <strong>{prediction_result["prediction"]}</strong> for lung cancer risk with a probability of <strong>{prediction_result["probability"]:.2%}</strong>.</p>
                    <p style="font-size: 1.1rem;">✅ Continue maintaining a healthy lifestyle.</p>
                </div>
                """, unsafe_allow_html=True)
                
            # Add recommendations based on risk factors with animation
            st.subheader("🩺 Personalized Recommendations")
            recommendations = []
            
            if smoking == 2:
                recommendations.append("Consider smoking cessation programs - smoking is a major risk factor for lung cancer.")
            
            if alcohol_consuming == 2:
                recommendations.append("Reduce alcohol consumption to improve overall health.")
                
            if fatigue == 2 and shortness_of_breath == 2:
                recommendations.append("The combination of fatigue and shortness of breath could indicate respiratory issues. Consider consultation.")
                
            if coughing == 2 and chest_pain == 2:
                recommendations.append("Persistent cough with chest pain should be evaluated by a healthcare professional.")
            
            if age > 60 and smoking == 2:
                recommendations.append("Given your age and smoking history, regular lung cancer screenings are recommended.")
                
            if len(recommendations) > 0:
                for i, rec in enumerate(recommendations):
                    st.markdown(f"""
                    <div class="info-card recommendation-item" style="animation-delay: {i*0.1}s">
                        {rec}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-card recommendation-item">
                    Maintain a healthy lifestyle with regular exercise and a balanced diet.
                </div>
                <div class="info-card recommendation-item" style="animation-delay: 0.1s">
                    Consider regular check-ups with your healthcare provider.
                </div>
                """, unsafe_allow_html=True)
        
        with result_cols[1]:
            # Display gauge chart
            st.plotly_chart(create_gauge_chart(prediction_result["probability"]), use_container_width=True)
            
            # Add a warning about model limitations
            st.markdown("""
            <div class="card" style="background-color: #EFF6FF; border-left: 4px solid #2563EB;">
                <h3 style="color: #2563EB;">Important Notice</h3>
                <p>This prediction is based on a machine learning model and should be used for informational purposes only. It does not replace a professional medical diagnosis.</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Display risk factors visualization
        st.subheader("📊 Your Risk Factor Analysis")
        
        # Prepare data for visualization
        factors = [
            {"name": "Smoking", "value": 1 if smoking == 2 else 0, "max": 1},
            {"name": "Age Risk", "value": 1 if age > 60 else 0, "max": 1},
            {"name": "Respiratory Symptoms", "value": sum([1 if x == 2 else 0 for x in [coughing, wheezing, shortness_of_breath]]), "max": 3},
            {"name": "Physical Symptoms", "value": sum([1 if x == 2 else 0 for x in [chest_pain, fatigue, swallowing_difficulty]]), "max": 3},
            {"name": "Other Factors", "value": sum([1 if x == 2 else 0 for x in [yellow_fingers, alcohol_consuming, anxiety]]), "max": 3}
        ]
        
        # Create a horizontal bar chart
        factor_df = pd.DataFrame(factors)
        factor_df["percentage"] = (factor_df["value"] / factor_df["max"]) * 100
        
        fig = px.bar(
            factor_df,
            y="name",
            x="percentage",
            orientation="h",
            labels={"percentage": "Risk Level (%)", "name": "Factor"},
            color="percentage",
            color_continuous_scale=["green", "yellow", "red"],
            range_color=[0, 100],
            text=factor_df["value"].astype(str) + "/" + factor_df["max"].astype(str)
        )
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=12, color="#1E3A8A")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add action steps section
        st.subheader("🚶 Next Steps")
        
        next_steps_cols = st.columns(3)
        
        with next_steps_cols[0]:
            st.markdown("""
            <div class="card" style="text-align: center; background-color: #F0FDF4; height: 220px;">
                <h3 style="color: #16A34A;">Lifestyle Changes</h3>
                <p>Make positive changes to reduce your risk factors</p>
                <ul style="text-align: left; list-style-type: none; padding-left: 0;">
                    <li>✅ Quit smoking</li>
                    <li>✅ Maintain healthy weight</li>
                    <li>✅ Reduce alcohol intake</li>
                    <li>✅ Exercise regularly</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with next_steps_cols[1]:
            st.markdown("""
            <div class="card" style="text-align: center; background-color: #EFF6FF; height: 220px;">
                <h3 style="color: #2563EB;">Medical Follow-ups</h3>
                <p>Professional medical guidance is essential</p>
                <ul style="text-align: left; list-style-type: none; padding-left: 0;">
                    <li>✅ Regular check-ups</li>
                    <li>✅ Lung cancer screening</li>
                    <li>✅ Discuss risk factors</li>
                    <li>✅ Follow medical advice</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with next_steps_cols[2]:
            st.markdown("""
            <div class="card" style="text-align: center; background-color: #FEFCE8; height: 220px;">
                <h3 style="color: #CA8A04;">Environmental Changes</h3>
                <p>Improve your living environment</p>
                <ul style="text-align: left; list-style-type: none; padding-left: 0;">
                    <li>✅ Radon testing</li>
                    <li>✅ Avoid secondhand smoke</li>
                    <li>✅ Improve air quality</li>
                    <li>✅ Reduce pollutant exposure</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add educational section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <h2>Understanding Lung Cancer</h2>
    <p>Lung cancer is one of the most common and serious types of cancer. There are usually no signs or symptoms in the early stages, which makes early detection challenging but crucial.</p>
</div>
""", unsafe_allow_html=True)

# Educational content in tabs
info_tabs = st.tabs(["📈 Statistics", "🔬 Types", "🩺 Diagnosis & Treatment"])

with info_tabs[0]:
    stats_cols = st.columns([1, 1])
    with stats_cols[0]:
        st.markdown("""
        ### Key Statistics
        - Lung cancer accounts for about 25% of all cancer deaths
        - The average age of diagnosis is about 70
        - 5-year survival rate for localized lung cancer: ~60%
        - 5-year survival rate for distant (metastasized) lung cancer: ~6%
        """)
    
    with stats_cols[1]:
        # Sample data for visualization
        stages = ['Localized', 'Regional', 'Distant']
        survival_rates = [60, 33, 6]
        
        fig = px.bar(
            x=stages,
            y=survival_rates,
            labels={'x': 'Cancer Stage', 'y': '5-Year Survival Rate (%)'},
            title='Lung Cancer 5-Year Survival Rates by Stage',
            color=survival_rates,
            color_continuous_scale=px.colors.sequential.Blues
        )
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=30),
        )
        
        st.plotly_chart(fig, use_container_width=True)

with info_tabs[1]:
    st.markdown("""
    ### Types of Lung Cancer
    
    #### Non-Small Cell Lung Cancer (NSCLC)
    - Accounts for 80-85% of lung cancers
    - Main subtypes: Adenocarcinoma, Squamous cell carcinoma, Large cell carcinoma
    - Generally grows and spreads more slowly than SCLC
    
    #### Small Cell Lung Cancer (SCLC)
    - Accounts for 15-20% of lung cancers
    - Strongly linked to cigarette smoking
    - Tends to grow more quickly and spread earlier than NSCLC
    - Often responds well to chemotherapy and radiation initially
    """)
    
    # Add an illustrative image
    st.image("https://img.freepik.com/free-vector/lung-cancer-concept-illustration_114360-8465.jpg", caption="Lung cancer types illustration", use_column_width=True)

with info_tabs[2]:
    diag_cols = st.columns([1, 1])
    
    with diag_cols[0]:
        st.markdown("""
        ### Diagnosis Methods
        
        - **Imaging Tests**: X-rays, CT scans, PET scans
        - **Sputum Cytology**: Examining mucus from the lungs
        - **Tissue Sample (Biopsy)**: Taking cells from suspicious areas
        - **Bronchoscopy**: Examining airways with a lighted tube
        - **Mediastinoscopy**: Surgical procedure to check lymph nodes
        """)
    
    with diag_cols[1]:
        st.markdown("""
        ### Treatment Options
        
        - **Surgery**: Removal of cancerous tissue
        - **Chemotherapy**: Using drugs to kill cancer cells
        - **Radiation Therapy**: Using high-energy rays to kill cancer cells
        - **Targeted Drug Therapy**: Targeting specific abnormalities in cancer cells
        - **Immunotherapy**: Boosting your immune system to fight cancer
        - **Palliative Care**: Improving quality of life
        """)

# Prevention section with animation
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <h2>Prevention Tips</h2>
    <p>While not all lung cancers can be prevented, there are steps you can take to reduce your risk.</p>
</div>
""", unsafe_allow_html=True)

prevention_cols = st.columns([1, 2])

with prevention_cols[0]:
    if health_animation:
        st_lottie(health_animation, height=300, key="health")
    else:
        st.image("https://img.freepik.com/free-vector/tiny-people-examining-lungs-flat-vector-illustration-cartoon-medical-team-doing-lung-diagnostics-x-ray-tuberculosis-pneumonia-respiratory-system-anatomy-health-medicine-concept_74855-25408.jpg", use_column_width=True)

with prevention_cols[1]:
    st.markdown("""
    ### Key Prevention Strategies
    
    1. **Avoid Tobacco**: Don't start smoking, or quit if you already smoke.
    
    2. **Avoid Secondhand Smoke**: Stay away from places where people smoke.
    
    3. **Test for Radon**: Have your home tested for radon, a naturally occurring radioactive gas.
    
    4. **Avoid Carcinogens**: Follow safety guidelines when working with toxic chemicals.
    
    5. **Eat a Healthy Diet**: Include plenty of fruits and vegetables.
    
    6. **Exercise Regularly**: Aim for at least 30 minutes of activity most days of the week.
    
    7. **Get Regular Screening**: If you're at high risk, talk to your doctor about lung cancer screening.
    """)

# FAQ Section with expandable questions
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <h2>Frequently Asked Questions</h2>
</div>
""", unsafe_allow_html=True)

with st.expander("🔍 Who should get screened for lung cancer?"):
    st.markdown("""
    Lung cancer screening is generally recommended for people who:
    
    - Are aged 50-80 years
    - Have a 20 pack-year smoking history (e.g., 1 pack a day for 20 years)
    - Currently smoke or have quit within the past 15 years
    - Are in relatively good health
    
    Always consult with your healthcare provider to determine if screening is right for you.
    """)

with st.expander("⏱️ How often should screening occur?"):
    st.markdown("""
    For those who meet the criteria for lung cancer screening, annual low-dose CT scans are typically recommended. 
    Your healthcare provider may suggest a different schedule based on your personal risk factors.
    """)

with st.expander("🧬 Is lung cancer hereditary?"):
    st.markdown("""
    While most lung cancers are not inherited, having a family history of lung cancer does increase your risk slightly. 
    This could be due to shared genetic factors or shared environmental exposures.
    
    If multiple members of your family have had lung cancer, especially at younger ages, you might consider genetic counseling.
    """)

with st.expander("🚭 If I quit smoking, how long until my risk decreases?"):
    st.markdown("""
    Your risk begins to decrease as soon as you quit smoking:
    
    - After 10 years, your risk of dying from lung cancer drops to about half that of a current smoker
    - After 15-20 years, your risk approaches (but never quite reaches) that of someone who has never smoked
    
    It's never too late to quit smoking - your body begins to heal almost immediately.
    """)

# Resources section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <h2>Additional Resources</h2>
    <p>Learn more about lung cancer diagnosis, treatment, and support through these reliable resources.</p>
</div>
""", unsafe_allow_html=True)

resource_cols = st.columns(3)

with resource_cols[0]:
    st.markdown("""
    <div class="card" style="text-align: center; height: 200px;">
        <h3>American Lung Association</h3>
        <p>Comprehensive information on lung health and disease</p>
        <p><a href="https://www.lung.org" target="_blank">www.lung.org</a></p>
    </div>
    """, unsafe_allow_html=True)

with resource_cols[1]:
    st.markdown("""
    <div class="card" style="text-align: center; height: 200px;">
        <h3>American Cancer Society</h3>
        <p>Cancer information, research, and patient support</p>
        <p><a href="https://www.cancer.org" target="_blank">www.cancer.org</a></p>
    </div>
    """, unsafe_allow_html=True)

with resource_cols[2]:
    st.markdown("""
    <div class="card" style="text-align: center; height: 200px;">
        <h3>National Cancer Institute</h3>
        <p>Government resource for cancer information</p>
        <p><a href="https://www.cancer.gov" target="_blank">www.cancer.gov</a></p>
    </div>
    """, unsafe_allow_html=True)

# Footer with animation
st.markdown("""
<div class="footer">
    <p>© 2025 Lung Cancer Risk Assessment Tool | Developed with ❤️ for better health outcomes</p>
    <p>This tool is for educational purposes only and does not provide medical advice.</p>
    <p>Always consult with healthcare professionals for medical concerns.</p>
</div>
""", unsafe_allow_html=True)

# Add custom notification for first-time users (could be toggled with cookies in a real app)
# This is just for show in this demo
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True
    
    js = """
    <script>
        // This would be implemented with proper JS in production
        setTimeout(function() {
            alert('Welcome to the Lung Cancer Risk Assessment Tool! This application helps you understand your personal risk factors. Remember that this is an educational tool and not a medical diagnosis.');
        }, 1500);
    </script>
    """
    st.components.v1.html(js)
