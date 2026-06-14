import sys
import os
# Add project root to sys.path dynamically
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from src.config import load_config, get_absolute_path

config = load_config()
model_rel_path = config.get("model", {}).get("save_path", "models/crop_disease_model.h5")
model_path = get_absolute_path(model_rel_path)
model_exists = os.path.exists(model_path)

# Hero Section
st.markdown("""<div class="hero-container">
<div class="hero-title">AgriVision AI</div>
<div class="hero-subtitle">AI-Powered Crop Disease Detection & Treatment Recommendation System. Protect your fields, increase yields, and make diagnostic decisions instantly.</div>
</div>""", unsafe_allow_html=True)

# Core Capabilities
st.markdown("<h2 style='text-align: center; color: #1E293B; margin-bottom: 2rem;'>Core Capabilities</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""<div class="feature-card">
<div class="feature-icon">🔬</div>
<div class="feature-title">Disease Detection</div>
<div class="feature-text">Analyze leaf anomalies using transfer learning with deep convolutional neural networks.</div>
</div>""", unsafe_allow_html=True)
    
with col2:
    st.markdown("""<div class="feature-card">
<div class="feature-icon">🛡️</div>
<div class="feature-title">Treatment Guidance</div>
<div class="feature-text">Receive immediate, actionable chemical and organic treatment recommendation workflows.</div>
</div>""", unsafe_allow_html=True)
    
with col3:
    st.markdown("""<div class="feature-card">
<div class="feature-icon">📋</div>
<div class="feature-title">Prevention Tips</div>
<div class="feature-text">Implement crop rotation schemes and sanitary precautions to prevent future reoccurrences.</div>
</div>""", unsafe_allow_html=True)
    
with col4:
    st.markdown("""<div class="feature-card">
<div class="feature-icon">⚡</div>
<div class="feature-title">Fast AI Analysis</div>
<div class="feature-text">Get sub-second classification outputs with clear visual confidence progress reports.</div>
</div>""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# How It Works
st.markdown("### How It Works")
col_step1, col_step2, col_step3 = st.columns(3)
with col_step1:
    st.info("**Step 1: Upload leaf image**\nCapture a clear, top-down photo of the infected crop leaf and upload it to the scanner.")
with col_step2:
    st.info("**Step 2: Neural processing**\nThe system automatically normalizes the image and runs inference on our fine-tuned MobileNetV2 model.")
with col_step3:
    st.info("**Step 3: Access diagnostic data**\nReview the diagnosed disease description, confidence scores, symptoms, and prevention instructions.")
    
if not model_exists:
    st.warning("⚠️ **ML Model Warning**: The neural network model `models/crop_disease_model.h5` is not trained yet. The scanner page will not work until you run `python train.py` in your terminal to train the model.")
