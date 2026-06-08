import os
import json
import streamlit as st
from PIL import Image
import numpy as np

# Set page configuration first (must be the first Streamlit command)
st.set_page_config(
    page_title="AgriVision AI - Smart Crop Disease Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for SaaS aesthetics
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Apply globally */
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Clean layout changes */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Hero section styling */
    .hero-container {
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
        border-radius: 16px;
        padding: 3rem 2.5rem;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 25px rgba(46, 125, 50, 0.15);
        position: relative;
        overflow: hidden;
    }
    .hero-container::after {
        content: '';
        position: absolute;
        bottom: -50px;
        right: -50px;
        width: 200px;
        height: 200px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 300;
        opacity: 0.9;
        max-width: 700px;
        line-height: 1.5;
    }
    
    /* Modern card styles */
    .feature-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
        border-color: #2E7D32;
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-weight: 600;
        font-size: 1.15rem;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .feature-text {
        font-size: 0.95rem;
        color: #64748B;
        line-height: 1.4;
    }
    
    /* Dashboard Results card styles */
    .result-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .badge-healthy {
        background-color: #E8F5E9;
        color: #2E7D32;
    }
    .badge-diseased {
        background-color: #FFEBEE;
        color: #C62828;
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: #1E293B;
        line-height: 1.1;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #2E7D32;
    }
    
    /* Card details in results */
    .details-box {
        background: #F8FAF8;
        border-left: 4px solid #2E7D32;
        padding: 1.25rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 1rem;
    }
    .details-box-title {
        font-weight: 600;
        font-size: 1.05rem;
        color: #1E293B;
        margin-bottom: 0.4rem;
    }
    .details-box-content {
        font-size: 0.95rem;
        color: #475569;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# Imports from utils
from utils.preprocess import preprocess_image
from utils.predictor import CropDiseasePredictor
from utils.helpers import get_disease_details, load_knowledge_base

# Singleton patterns for lazy loading model
@st.cache_resource
def get_predictor():
    return CropDiseasePredictor()

# Sidebar Layout
with st.sidebar:
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=80)
    else:
        st.image("https://img.icons8.com/color/96/000000/sprout.png", width=80)
    st.markdown("<h2 style='margin-top:0;'>AgriVision AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 0.9rem;'>Smart Crop Health Intelligence</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation option
    page = st.radio(
        "Navigation",
        ["🏠 Home", "🔬 Scan Leaf", "📚 Disease Library", "📊 Model Analytics"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### Supported Crops")
    st.markdown("- 🍅 Tomato (11 classes)")
    st.markdown("- 🥔 Potato (3 classes)")
    st.markdown("- 🫑 Pepper Bell (2 classes)")
    
    st.markdown("<div style='position: fixed; bottom: 10px; font-size: 0.8rem; color: #94A3B8;'>Phase 1 - Release v1.0.0</div>", unsafe_allow_html=True)

# Check if model exists
model_path = os.path.join("models", "crop_disease_model.h5")
model_exists = os.path.exists(model_path)

# ----------------- PAGE: HOME -----------------
if page == "🏠 Home":
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">AgriVision AI</div>
        <div class="hero-subtitle">AI-Powered Crop Disease Detection & Treatment Recommendation System. Protect your fields, increase yields, and make diagnostic decisions instantly.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section Header
    st.markdown("<h2 style='text-align: center; color: #1E293B; margin-bottom: 2rem;'>Core Capabilities</h2>", unsafe_allow_html=True)
    
    # Grid of Features
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔬</div>
            <div class="feature-title">Disease Detection</div>
            <div class="feature-text">Analyze leaf anomalies using transfer learning with deep convolutional neural networks.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">Treatment Guidance</div>
            <div class="feature-text">Receive immediate, actionable chemical and organic treatment recommendation workflows.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📋</div>
            <div class="feature-title">Prevention Tips</div>
            <div class="feature-text">Implement crop rotation schemes and sanitary precautions to prevent future reoccurrences.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast AI Analysis</div>
            <div class="feature-text">Get sub-second classification outputs with clear visual confidence progress reports.</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # How it works section
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

# ----------------- PAGE: SCAN LEAF -----------------
elif page == "🔬 Scan Leaf":
    st.markdown("## 🔬 Crop Disease Scanner")
    st.markdown("Upload a crop leaf image (Tomato, Potato, or Pepper Bell) to identify diseases and load medical treatments.")
    
    if not model_exists:
        st.error("❌ **AI Inference Engine Offline**: The file `models/crop_disease_model.h5` is missing. You must run the training script (`train.py`) first to generate the model before scanning leaves.")
    else:
        uploaded_file = st.file_uploader(
            "Choose a crop leaf image...", 
            type=["jpg", "jpeg", "png"],
            help="Supported formats: JPG, JPEG, PNG"
        )
        
        if uploaded_file is not None:
            # Layout: Left for image, right for prediction results
            col_img, col_res = st.columns([1, 1.2])
            
            with col_img:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Crop Leaf", use_container_width=True)
                
            with col_res:
                with st.spinner("Analyzing leaf patterns..."):
                    try:
                        # 1. Preprocess the image
                        preprocessed = preprocess_image(uploaded_file)
                        
                        # 2. Get predictor
                        predictor = get_predictor()
                        
                        # 3. Predict class & confidence
                        predicted_class, confidence = predictor.predict(preprocessed)
                        
                        # 4. Fetch details from knowledge base
                        details = get_disease_details(predicted_class)
                        
                        is_healthy = "healthy" in predicted_class.lower()
                        badge_class = "badge-healthy" if is_healthy else "badge-diseased"
                        badge_text = "HEALTHY" if is_healthy else "DISEASED / PATTERN DETECTED"
                        
                        # 5. Display results dashboard
                        st.markdown(f"""
                        <div class="result-card">
                            <span class="status-badge {badge_class}">{badge_text}</span>
                            <div class="metric-label">Identified Crop Condition</div>
                            <div class="metric-value" style="color: {'#2E7D32' if is_healthy else '#C62828'}; margin-bottom:1rem;">{details['disease_name']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Confidence Score Progress
                        st.markdown(f"**Confidence Level**: `{confidence*100:.2f}%`")
                        st.progress(confidence)
                        
                        # Display detail tabs
                        st.markdown("---")
                        tab_desc, tab_sym, tab_treat, tab_prev = st.tabs([
                            "ℹ️ Disease Info", 
                            "🔍 Symptoms", 
                            "💊 Recommended Treatment", 
                            "🛡️ Prevention Tips"
                        ])
                        
                        with tab_desc:
                            st.markdown(f"**Description**:\n{details['description']}")
                            
                        with tab_sym:
                            st.markdown("### Symptoms to Look For")
                            for symptom in details['symptoms']:
                                st.markdown(f"- {symptom}")
                                
                        with tab_treat:
                            st.markdown("### Recommended Actionable Treatment")
                            for idx, treat in enumerate(details['treatment']):
                                st.markdown(f"**{idx + 1}.** {treat}")
                                
                        with tab_prev:
                            st.markdown("### Preventative Strategies")
                            for idx, prev in enumerate(details['prevention']):
                                st.markdown(f"**{idx + 1}.** {prev}")
                                
                    except Exception as e:
                        st.error(f"Prediction Error: {e}")
                        st.exception(e)

# ----------------- PAGE: DISEASE LIBRARY -----------------
elif page == "📚 Disease Library":
    st.markdown("## 📚 Agricultural Disease Library")
    st.markdown("Browse crop health profiles, diagnostic guides, and treatment procedures for all 15 supported categories.")
    
    try:
        kb = load_knowledge_base()
        
        # Crop filter
        crop_filter = st.selectbox("Filter by Crop Category", ["All Crops", "Tomato 🍅", "Potato 🥔", "Pepper Bell 🫑"])
        
        # Filter classes based on selection
        filtered_classes = {}
        for k, v in kb.items():
            if crop_filter == "Tomato 🍅" and "tomato" not in k.lower():
                continue
            elif crop_filter == "Potato 🥔" and "potato" not in k.lower():
                continue
            elif crop_filter == "Pepper Bell 🫑" and "pepper" not in k.lower():
                continue
            filtered_classes[k] = v
            
        # Display as cards or selectbox expander
        class_choice = st.selectbox(
            "Select a condition profile to examine:",
            options=list(filtered_classes.keys()),
            format_func=lambda x: filtered_classes[x]['disease_name']
        )
        
        if class_choice:
            profile = filtered_classes[class_choice]
            is_healthy = "healthy" in class_choice.lower()
            
            st.markdown("---")
            col_info, col_bullets = st.columns([1.2, 1])
            
            with col_info:
                st.subheader(profile['disease_name'])
                st.markdown(f"**Condition Status**: `{'Healthy' if is_healthy else 'Diseased'}`")
                st.markdown(f"**Description**:\n{profile['description']}")
                
                st.markdown("<br><h4>🛡️ Preventative Measures</h4>", unsafe_allow_html=True)
                for idx, prev in enumerate(profile['prevention']):
                    st.markdown(f"**{idx+1}.** {prev}")
                    
            with col_bullets:
                st.markdown("<h4>🔍 Symptoms</h4>", unsafe_allow_html=True)
                for symptom in profile['symptoms']:
                    st.markdown(f"- {symptom}")
                    
                st.markdown("<br><h4>💊 Recommended Treatments</h4>", unsafe_allow_html=True)
                for idx, treat in enumerate(profile['treatment']):
                    st.markdown(f"**{idx+1}.** {treat}")
                    
    except Exception as e:
        st.error(f"Failed to load disease library: {e}")

# ----------------- PAGE: MODEL ANALYTICS -----------------
elif page == "📊 Model Analytics":
    st.markdown("## 📊 Model Performance & Training Analytics")
    st.markdown("View training metrics, accuracy curves, and class confusion matrices computed on the PlantVillage dataset.")
    
    metrics_path = os.path.join("assets", "model_metrics.json")
    
    if not os.path.exists(metrics_path):
        st.info("💡 **No Analytics Data Found**: Training metrics files will be displayed here once you complete running `python train.py` on your machine.")
    else:
        try:
            with open(metrics_path, "r") as f:
                metrics = json.load(f)
                
            # Key statistics cards
            col_acc, col_prec, col_rec, col_f1 = st.columns(4)
            
            with col_acc:
                st.metric("Test Accuracy", f"{metrics['accuracy']*100:.2f}%")
            with col_prec:
                st.metric("Weighted Precision", f"{metrics['precision']*100:.2f}%")
            with col_rec:
                st.metric("Weighted Recall", f"{metrics['recall']*100:.2f}%")
            with col_f1:
                st.metric("F1 Score", f"{metrics['f1_score']*100:.2f}%")
                
            st.markdown("---")
            
            # Training details
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.markdown("### Model Specification")
                st.write(f"- **Base Architecture**: MobileNetV2 (Transfer Learning)")
                st.write(f"- **Pretrained Weights**: ImageNet")
                st.write(f"- **Augmentation**: Random Flip, Random Rotation, Random Zoom")
            with col_info2:
                st.markdown("### Training Logs")
                st.write(f"- **Epochs Trained**: {metrics['epochs_trained']}")
                st.write(f"- **Training Duration**: {metrics['training_time_seconds']:.2f} seconds")
                st.write(f"- **Test Categorical Loss**: {metrics['test_loss']:.4f}")
                
            st.markdown("---")
            
            # Plots layout
            col_plot1, col_plot2 = st.columns(2)
            
            history_plot = os.path.join("assets", "images", "training_history.png")
            cm_plot = os.path.join("assets", "images", "confusion_matrix.png")
            
            with col_plot1:
                st.markdown("### Accuracy and Loss Curves")
                if os.path.exists(history_plot):
                    st.image(history_plot, use_container_width=True)
                else:
                    st.warning("History plot image file not found.")
                    
            with col_plot2:
                st.markdown("### Test Split Confusion Matrix")
                if os.path.exists(cm_plot):
                    st.image(cm_plot, use_container_width=True)
                else:
                    st.warning("Confusion matrix image file not found.")
                    
        except Exception as e:
            st.error(f"Error loading analytics reports: {e}")
