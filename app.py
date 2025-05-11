import streamlit as st
import plotly.graph_objects as go

# Function to create a gauge chart
def create_gauge_chart(probability):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Lung Cancer Risk (%)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#003f5c"},
            'steps': [
                {'range': [0, 30], 'color': "#2f4b7c"},
                {'range': [30, 70], 'color': "#f95d6a"},
                {'range': [70, 100], 'color': "#d45087"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': probability * 100
            }
        }
    ))
    return fig

# Set page config
st.set_page_config(page_title="🫁 Lung Cancer Risk Tool", layout="wide")

# Custom CSS styling
st.markdown("""
<style>
body, .main {
    background-color: #f9f9f9;
}
h1, h2, h3, h4 {
    color: #003f5c;
}
section {
    padding: 1rem;
}
.stRadio > div {
    gap: 1rem;
}
.stButton > button {
    background-color: #003f5c;
    color: white;
    padding: 0.6rem 1.2rem;
    font-size: 1rem;
    border: none;
    border-radius: 6px;
}
.stButton > button:hover {
    background-color: #2f4b7c;
}
.prediction-box {
    border-radius: 12px;
    padding: 1.5rem;
    color: #222;
    margin-top: 1rem;
}
.low-risk {
    background: #d4edda;
    border-left: 6px solid #28a745;
}
.medium-risk {
    background: #fff3cd;
    border-left: 6px solid #ffc107;
}
.high-risk {
    background: #f8d7da;
    border-left: 6px solid #dc3545;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🫁 Lung Cancer Risk Assessment Tool")
st.markdown("""
Use this interactive tool to estimate your risk of developing lung cancer based on health and lifestyle factors.
""")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About This Tool")
    st.info("""
    This tool uses a machine learning model trained on health survey data to estimate lung cancer risk.
    **Note**: This does not replace a medical diagnosis.
    """)
    st.markdown("---")
    st.header("🚩 Risk Factors")
    st.markdown("""
- Smoking  
- Family history  
- Air pollution  
- Exposure to carcinogens  
- Chronic illness  
- Age  
""")
    st.header("⚠️ Common Symptoms")
    st.markdown("""
- Persistent coughing  
- Chest pain  
- Shortness of breath  
- Unexplained fatigue  
""")

# Input Form
st.header("📝 Patient Information")
col1, col2, col3 = st.columns(3)

with col1:
    gender = st.radio("Gender", ["M", "F"])
    age = st.number_input("Age", min_value=1, max_value=100, value=50)
    smoking = st.radio("Smoking", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")
    yellow_fingers = st.radio("Yellow Fingers", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")
    anxiety = st.radio("Anxiety", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")

with col2:
    peer_pressure = st.radio("Peer Pressure", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")
    chronic_disease = st.radio("Chronic Disease", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")
    fatigue = st.radio("Fatigue", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")
    allergy = st.radio("Allergy", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")
    wheezing = st.radio("Wheezing", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")

with col3:
    alcohol = st.radio("Alcohol Consumption", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")
    coughing = st.radio("Coughing", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")
    shortness = st.radio("Shortness of Breath", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")
    swallowing = st.radio("Swallowing Difficulty", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")
    chest_pain = st.radio("Chest Pain", [1, 2], format_func=lambda x: "Yes" if x == 2 else "No")

# Submit
if st.button("🔍 Predict Lung Cancer Risk"):
    # Simulate prediction (replace with real API call)
    if smoking == 2 and age > 60:
        prob = 0.85
        pred = "YES"
        risk = "High"
    elif smoking == 2 or age > 60:
        prob = 0.60
        pred = "YES"
        risk = "Medium"
    else:
        prob = 0.20
        pred = "NO"
        risk = "Low"

    # Result
    st.subheader("📊 Prediction Result")

    result_class = {
        "Low": "low-risk",
        "Medium": "medium-risk",
        "High": "high-risk"
    }[risk]

    st.markdown(f"""
    <div class="prediction-box {result_class}">
        <h3>{risk} Risk</h3>
        <p>The prediction is <strong>{pred}</strong> with a probability of <strong>{prob*100:.2f}%</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

    # Recommendations
    st.subheader("🩺 Recommendations")
    tips = []
    if smoking == 2:
        tips.append("• Quit smoking to significantly reduce your risk.")
    if alcohol == 2:
        tips.append("• Reduce alcohol consumption.")
    if fatigue == 2 and shortness == 2:
        tips.append("• Fatigue and shortness of breath may indicate underlying issues.")
    if coughing == 2 and chest_pain == 2:
        tips.append("• Persistent coughing with chest pain should be medically evaluated.")

    if not tips:
        tips.append("• Maintain a healthy lifestyle with regular exercise and check-ups.")

    for t in tips:
        st.markdown(f"- {t}")

    # Gauge chart
    st.plotly_chart(create_gauge_chart(prob), use_container_width=True)

    st.info("This tool is for educational purposes and should not replace medical diagnosis.")

# Footer
st.markdown("---")
st.markdown("© 2025 Lung Cancer Risk Tool. All rights reserved.")
