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
    
    /* Marketplace custom styles */
    .recommendation-banner {
        background: linear-gradient(135deg, #1E3A8A 0%, #2E7D32 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    .recommendation-banner-content {
        flex: 1;
    }
    .recommendation-banner-title {
        font-weight: 700;
        font-size: 1.25rem;
        margin-bottom: 0.25rem;
    }
    .recommendation-banner-text {
        font-size: 0.95rem;
        opacity: 0.9;
    }
    
    .product-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .prod-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.25rem;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        position: relative;
    }
    .prod-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border-color: #2E7D32;
    }
    .prod-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background: #E8F5E9;
        color: #2E7D32;
        padding: 0.2rem 0.5rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .prod-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }
    .prod-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #1E293B;
        margin-bottom: 0.5rem;
        min-height: 2.2rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .prod-desc {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 1rem;
        min-height: 3rem;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .prod-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    .prod-price {
        font-weight: 800;
        font-size: 1.25rem;
        color: #2E7D32;
    }
    .prod-rating {
        font-size: 0.85rem;
        color: #F59E0B;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    /* Stepper tracking styles */
    .stepper-wrapper {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        position: relative;
    }
    .stepper-item {
        flex: 1;
        text-align: center;
        position: relative;
        z-index: 2;
    }
    .stepper-item::before {
        position: absolute;
        content: '';
        border-bottom: 3px solid #E2E8F0;
        width: 100%;
        top: 20px;
        left: -50%;
        z-index: -1;
    }
    .stepper-item:first-child::before {
        content: none;
    }
    .stepper-item .step-counter {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #E2E8F0;
        margin: 0 auto 10px auto;
        font-weight: bold;
        color: #64748B;
        font-size: 1rem;
    }
    .stepper-item.completed .step-counter {
        background-color: #2E7D32;
        color: white;
    }
    .stepper-item.completed::before {
        border-bottom: 3px solid #2E7D32;
    }
    .stepper-item.active .step-counter {
        background-color: #2E7D32;
        color: white;
        box-shadow: 0 0 0 4px rgba(46, 125, 50, 0.2);
    }
    .stepper-item .step-name {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748B;
    }
    .stepper-item.active .step-name {
        color: #2E7D32;
    }
    .stepper-item.completed .step-name {
        color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# Imports from utils
import base64
from utils.preprocess import preprocess_image
from utils.predictor import CropDiseasePredictor
from utils.helpers import get_disease_details, load_knowledge_base
from utils.marketplace_data import PRODUCTS, get_recommended_products, DISEASE_PRODUCT_MAPPING

def get_base64_image(image_path):
    """
    Convert a local image to base64 string to embed in HTML.
    """
    try:
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        pass
    return ""

# Initialize session state variables
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "orders" not in st.session_state:
    st.session_state.orders = []
if "last_diagnosis" not in st.session_state:
    st.session_state.last_diagnosis = None
if "active_page" not in st.session_state:
    st.session_state.active_page = "🏠 Home"
if "checkout_step" not in st.session_state:
    st.session_state.checkout_step = "cart"
if "current_order_id" not in st.session_state:
    st.session_state.current_order_id = None

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
    
    # Navigation options
    nav_options = ["🏠 Home", "🔬 Scan Leaf", "📚 Disease Library", "🛒 Marketplace", "📊 Model Analytics"]
    if st.session_state.active_page not in nav_options:
        st.session_state.active_page = "🏠 Home"
        
    default_idx = nav_options.index(st.session_state.active_page)
    
    # Render sidebar radio
    selected_nav = st.radio(
        "Navigation",
        nav_options,
        index=default_idx,
        key="navigation_radio"
    )
    
    # Sync if user manually changed radio selection
    if selected_nav != st.session_state.active_page:
        st.session_state.active_page = selected_nav
        
    page = st.session_state.active_page
    
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
                        
                        # Save latest diagnosis for recommendations
                        st.session_state.last_diagnosis = {
                            "class_name": predicted_class,
                            "disease_name": details['disease_name']
                        }
                        
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
                        tab_desc, tab_sym, tab_treat, tab_prev, tab_shop = st.tabs([
                            "ℹ️ Disease Info", 
                            "🔍 Symptoms", 
                            "💊 Recommended Treatment", 
                            "🛡️ Prevention Tips",
                            "🛒 Shop Treatments"
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
                                
                        with tab_shop:
                            st.markdown("### 🛒 Recommended Products for this Condition")
                            st.markdown("These products are available in the AgriVision Marketplace to treat this condition:")
                            
                            recs = get_recommended_products(predicted_class)
                            for prod in recs:
                                with st.container():
                                    img_base64 = get_base64_image(prod.get('image_path', ''))
                                    if img_base64:
                                        img_html = f'<img src="data:image/png;base64,{img_base64}" style="width: 65px; height: 65px; border-radius: 8px; object-fit: cover;" />'
                                    else:
                                        img_html = f'<span style="font-size: 2.2rem;">{prod["image"]}</span>'
                                    st.markdown(f"""
                                    <div style="background: #F8FAF8; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem;">
                                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                                            {img_html}
                                            <div>
                                                <h4 style="margin: 0; color: #1E293B;">{prod['name']}</h4>
                                                <span style="font-size: 0.8rem; background: #E2E8F0; color: #475569; padding: 0.15rem 0.5rem; border-radius: 12px; font-weight: 600;">{prod['category']}</span>
                                            </div>
                                        </div>
                                        <p style="font-size: 0.9rem; color: #475569; margin-bottom: 0.75rem;">{prod['description']}</p>
                                        <div style="display: flex; justify-content: space-between; align-items: center;">
                                            <span style="font-size: 1.15rem; font-weight: 700; color: #2E7D32;">${prod['price']:.2f}</span>
                                            <span style="font-size: 0.85rem; color: #F59E0B; font-weight: 600;">⭐ {prod['rating']} / 5.0</span>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    btn_col1, btn_col2 = st.columns([1, 1])
                                    with btn_col1:
                                        if st.button(f"Add to Cart", key=f"add_cart_scan_{prod['id']}"):
                                            st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                                            st.toast(f"Added {prod['name']} to cart!")
                                    with btn_col2:
                                        if st.button(f"Buy Now", key=f"buy_now_scan_{prod['id']}"):
                                            st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                                            st.session_state.checkout_step = "cart"
                                            st.session_state.active_page = "🛒 Marketplace"
                                            st.rerun()
                                
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
            lib_tab_profile, lib_tab_shop = st.tabs(["📋 Disease Profile", "🛒 Shop Recommended Products"])
            
            with lib_tab_profile:
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
                        
            with lib_tab_shop:
                st.markdown("### 🛒 Recommended Products for this Condition")
                st.markdown("These products are available in the AgriVision Marketplace to treat this condition:")
                
                recs = get_recommended_products(class_choice)
                for prod in recs:
                    with st.container():
                        img_base64 = get_base64_image(prod.get('image_path', ''))
                        if img_base64:
                            img_html = f'<img src="data:image/png;base64,{img_base64}" style="width: 65px; height: 65px; border-radius: 8px; object-fit: cover;" />'
                        else:
                            img_html = f'<span style="font-size: 2.2rem;">{prod["image"]}</span>'
                        st.markdown(f"""
                        <div style="background: #F8FAF8; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem;">
                            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                                {img_html}
                                <div>
                                    <h4 style="margin: 0; color: #1E293B;">{prod['name']}</h4>
                                    <span style="font-size: 0.8rem; background: #E2E8F0; color: #475569; padding: 0.15rem 0.5rem; border-radius: 12px; font-weight: 600;">{prod['category']}</span>
                                </div>
                            </div>
                            <p style="font-size: 0.9rem; color: #475569; margin-bottom: 0.75rem;">{prod['description']}</p>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 1.15rem; font-weight: 700; color: #2E7D32;">${prod['price']:.2f}</span>
                                <span style="font-size: 0.85rem; color: #F59E0B; font-weight: 600;">⭐ {prod['rating']} / 5.0</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        btn_col1, btn_col2 = st.columns([1, 1])
                        with btn_col1:
                            if st.button(f"Add to Cart", key=f"add_cart_lib_{prod['id']}"):
                                st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                                st.toast(f"Added {prod['name']} to cart!")
                        with btn_col2:
                            if st.button(f"Buy Now", key=f"buy_now_lib_{prod['id']}"):
                                st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                                st.session_state.checkout_step = "cart"
                                st.session_state.active_page = "🛒 Marketplace"
                                st.rerun()
                    
    except Exception as e:
        st.error(f"Failed to load disease library: {e}")

# ----------------- PAGE: MARKETPLACE -----------------
elif page == "🛒 Marketplace":
    st.markdown("## 🛒 AgriVision Crop Care Marketplace")
    st.markdown("Browse high-quality fertilizer, pest control, and soil restoration products customized for your crops.")
    
    # Helper to render stepper
    def render_tracking_stepper(status_index):
        steps = [
            {"name": "Order Placed", "icon": "📝"},
            {"name": "Dispatched", "icon": "📦"},
            {"name": "In Transit", "icon": "🚚"},
            {"name": "Delivered", "icon": "🏡"}
        ]
        
        html = '<div class="stepper-wrapper">'
        for idx, step in enumerate(steps):
            status_class = ""
            if idx < status_index:
                status_class = "completed"
            elif idx == status_index:
                status_class = "active"
                
            html += f"""
            <div class="stepper-item {status_class}">
                <div class="step-counter">{step['icon']}</div>
                <div class="step-name">{step['name']}</div>
            </div>
            """
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    # 1. Personalized Recommendations Banner
    if st.session_state.last_diagnosis:
        diag = st.session_state.last_diagnosis
        st.markdown(f"""
        <div class="recommendation-banner">
            <span style="font-size: 2.2rem;">💡</span>
            <div class="recommendation-banner-content">
                <div class="recommendation-banner-title">Personalized Treatment Available</div>
                <div class="recommendation-banner-text">Based on your recent scan showing <b>{diag['disease_name']}</b>, we recommend specific treatments below (marked with ⭐).</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Determine the step view
    if st.session_state.checkout_step == "tracking":
        # Find current order
        order = None
        for o in st.session_state.orders:
            if o['order_id'] == st.session_state.current_order_id:
                order = o
                break
                
        if not order:
            st.error("No active order found.")
            if st.button("Return to Marketplace"):
                st.session_state.checkout_step = "cart"
                st.rerun()
        else:
            st.success(f"🎉 Order {order['order_id']} placed successfully! Estimated delivery in 2-3 business days.")
            
            st.markdown("### 🚚 Live Delivery Tracker")
            st.markdown("Use the slider below to simulate the dispatch and delivery steps:")
            
            simulated_step = st.select_slider(
                "Simulation Stage",
                options=["Order Placed 📝", "Dispatched from Depot 📦", "In Transit 🚚", "Delivered 🏡"],
                value=["Order Placed 📝", "Dispatched from Depot 📦", "In Transit 🚚", "Delivered 🏡"][order['status_index']]
            )
            
            step_mapping = {
                "Order Placed 📝": 0,
                "Dispatched from Depot 📦": 1,
                "In Transit 🚚": 2,
                "Delivered 🏡": 3
            }
            order['status_index'] = step_mapping[simulated_step]
            order['status'] = simulated_step
            
            # Render stepper
            render_tracking_stepper(order['status_index'])
            
            # Display detailed delivery receipt
            st.markdown("### 📄 Order Receipt")
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.markdown(f"""
                **Customer Details**:
                - **Name**: {order['name']}
                - **Phone**: {order['phone']}
                - **Address**: {order['address']}
                - **Payment Method**: {order['payment_method']}
                """)
            with col_r2:
                st.markdown(f"**Order Reference**: `{order['order_id']}`")
                for pid, qty in order['items'].items():
                    prod = PRODUCTS[pid]
                    st.markdown(f"- {prod['image']} {prod['name']} (x{qty}): **${prod['price']*qty:.2f}**")
                    
                st.markdown(f"""
                <div style="background: #F8FAF8; padding: 1rem; border-radius: 8px; margin-top: 0.5rem; font-size: 0.9rem;">
                    <div style="display: flex; justify-content: space-between;"><span>Subtotal:</span><span>${order['subtotal']:.2f}</span></div>
                    {f'<div style="display: flex; justify-content: space-between; color: #C62828;"><span>Discount:</span><span>-${order["discount"]:.2f}</span></div>' if order['discount'] > 0 else ''}
                    <div style="display: flex; justify-content: space-between;"><span>Shipping:</span><span>{"FREE" if order['shipping'] == 0 else f"${order['shipping']:.2f}"}</span></div>
                    <div style="display: flex; justify-content: space-between;"><span>Tax (8%):</span><span>${order['tax']:.2f}</span></div>
                    <hr style="margin: 0.3rem 0;">
                    <div style="display: flex; justify-content: space-between; font-weight: 700; color: #2E7D32;"><span>Grand Total:</span><span>${order['total']:.2f}</span></div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("---")
            
            if st.button("Continue Shopping 🛒", use_container_width=True):
                st.session_state.checkout_step = "cart"
                st.rerun()

    else:
        # Two-column layout: Left for Products / Checkout Form, Right for Cart
        col_catalog, col_cart = st.columns([2.0, 1.1])
        
        with col_catalog:
            if st.session_state.checkout_step == "checkout":
                st.markdown("### 💳 Secure Checkout")
                st.markdown("Please fill out your delivery details to complete the fertilizer recommendation order.")
                
                with st.form("checkout_form"):
                    name = st.text_input("Full Name", placeholder="e.g. John Doe")
                    address = st.text_area("Delivery Address", placeholder="e.g. 123 Farm Road, Green County")
                    phone = st.text_input("Phone Number", placeholder="e.g. +1 555-0199")
                    
                    pay_method = st.selectbox(
                        "Payment Method", 
                        ["Cash on Delivery (COD)", "UPI / Instant FarmPay", "Credit/Debit Card", "Agricultural Subsidy Credits"]
                    )
                    
                    terms = st.checkbox("I agree to the Agricultural Direct Delivery Terms & Conditions")
                    
                    col_back, col_submit = st.columns([1, 1])
                    with col_back:
                        back_click = st.form_submit_button("Back to Cart")
                    with col_submit:
                        submit_click = st.form_submit_button("Place Order 🚀")
                        
                if back_click:
                    st.session_state.checkout_step = "cart"
                    st.rerun()
                    
                if submit_click:
                    if not name or not address or not phone:
                        st.error("Please fill in all the required delivery details.")
                    elif not terms:
                        st.error("Please accept the terms and conditions to proceed.")
                    else:
                        # Successful order placement!
                        import random
                        order_id = f"AV-{random.randint(100000, 999999)}"
                        st.session_state.current_order_id = order_id
                        
                        # Calculate totals
                        subtotal = sum(PRODUCTS[pid]['price'] * qty for pid, qty in st.session_state.cart.items())
                        discount_pct = 0.50 if st.session_state.coupon == "GROW50" else (0.20 if st.session_state.coupon == "AGRISMART" else 0.0)
                        discount = subtotal * discount_pct
                        shipping = 5.0 if subtotal < 50 else 0.0
                        tax = (subtotal - discount) * 0.08
                        grand_total = subtotal - discount + shipping + tax
                        
                        # Create order detail
                        order_detail = {
                            "order_id": order_id,
                            "name": name,
                            "address": address,
                            "phone": phone,
                            "payment_method": pay_method,
                            "items": {pid: qty for pid, qty in st.session_state.cart.items()},
                            "subtotal": subtotal,
                            "discount": discount,
                            "shipping": shipping,
                            "tax": tax,
                            "total": grand_total,
                            "status": "Order Placed",
                            "status_index": 0
                        }
                        
                        st.session_state.orders.append(order_detail)
                        # Clear cart and coupon
                        st.session_state.cart = {}
                        st.session_state.coupon = None
                        
                        st.session_state.checkout_step = "tracking"
                        st.rerun()
            else:
                # Browse mode
                st.markdown("### Browse Products")
                
                # Filters
                col_f1, col_f2, col_f3 = st.columns(3)
                with col_f1:
                    cat_filter = st.selectbox("Category Filter", ["All", "Fertilizer", "Fungicide", "Pest Control", "Soil & Nutrient Care"])
                with col_f2:
                    search_query = st.text_input("🔍 Search Products", placeholder="Search products...")
                with col_f3:
                    sort_option = st.selectbox("Sort By", ["Popularity", "Price: Low to High", "Price: High to Low", "Rating"])
                
                # Filter logic
                filtered_prods = list(PRODUCTS.values())
                
                recs_ids = []
                if st.session_state.last_diagnosis:
                    recs_ids = DISEASE_PRODUCT_MAPPING.get(st.session_state.last_diagnosis['class_name'], [])
                
                if cat_filter != "All":
                    filtered_prods = [p for p in filtered_prods if p['category'] == cat_filter]
                    
                if search_query:
                    q = search_query.lower()
                    filtered_prods = [p for p in filtered_prods if q in p['name'].lower() or q in p['description'].lower() or q in p['suitability'].lower()]
                    
                if sort_option == "Price: Low to High":
                    filtered_prods.sort(key=lambda x: x['price'])
                elif sort_option == "Price: High to Low":
                    filtered_prods.sort(key=lambda x: x['price'], reverse=True)
                elif sort_option == "Rating":
                    filtered_prods.sort(key=lambda x: x['rating'], reverse=True)
                
                # Render in a clean grid using columns (2 columns for catalog area)
                gcols = st.columns(2)
                for idx, prod in enumerate(filtered_prods):
                    gcol = gcols[idx % 2]
                    with gcol:
                        is_rec = prod['id'] in recs_ids
                        rec_badge = '<div style="position: absolute; top: 10px; right: 10px; background: #E8F5E9; color: #2E7D32; padding: 0.2rem 0.5rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; border: 1px solid #2E7D32;">⭐ RECOMMENDED</div>' if is_rec else ''
                        
                        img_base64 = get_base64_image(prod.get('image_path', ''))
                        if img_base64:
                            img_html = f'<img src="data:image/png;base64,{img_base64}" style="width: 80px; height: 80px; border-radius: 8px; object-fit: cover; margin-bottom: 0.5rem; display: block;" />'
                        else:
                            img_html = f'<span style="font-size: 2.5rem; display: block; margin-bottom: 0.5rem;">{prod["image"]}</span>'
                        
                        st.markdown(f"""
                        <div style="background: white; border: 1px solid {'#2E7D32' if is_rec else '#E2E8F0'}; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; position: relative; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); min-height: 330px; display: flex; flex-direction: column; justify-content: space-between;">
                            {rec_badge}
                            <div>
                                {img_html}
                                <span style="font-size: 0.8rem; background: #E2E8F0; color: #475569; padding: 0.15rem 0.5rem; border-radius: 12px; font-weight: 600;">{prod['category']}</span>
                                <h4 style="margin: 0.5rem 0 0.25rem 0; color: #1E293B; font-size: 1.05rem;">{prod['name']}</h4>
                                <p style="font-size: 0.85rem; color: #64748B; line-height: 1.3; min-height: 3.5rem;">{prod['description']}</p>
                                <div style="font-size: 0.8rem; color: #475569; margin-bottom: 0.5rem;"><b>Suitable for:</b> {prod['suitability']}</div>
                            </div>
                            <div>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                                    <span style="font-size: 1.25rem; font-weight: 800; color: #2E7D32;">${prod['price']:.2f}</span>
                                    <span style="font-size: 0.85rem; color: #F59E0B; font-weight: 600;">⭐ {prod['rating']}</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        ac_col1, ac_col2 = st.columns(2)
                        with ac_col1:
                            if st.button("Add to Cart", key=f"catalog_add_{prod['id']}"):
                                st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                                st.toast(f"Added {prod['name']}!")
                                st.rerun()
                        with ac_col2:
                            if st.button("Buy Now", key=f"catalog_buy_{prod['id']}"):
                                st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                                st.session_state.checkout_step = "checkout"
                                st.rerun()

        # Cart Column
        with col_cart:
            st.markdown("### 🛒 Shopping Cart")
            if not st.session_state.cart:
                st.markdown("Your cart is empty. Add recommended fertilizers to get started!")
            else:
                subtotal = 0.0
                for pid, qty in list(st.session_state.cart.items()):
                    if qty <= 0:
                        del st.session_state.cart[pid]
                        continue
                    prod = PRODUCTS[pid]
                    item_total = prod['price'] * qty
                    subtotal += item_total
                    
                    st.markdown(f"**{prod['image']} {prod['name']}**")
                    item_col1, item_col2 = st.columns([2, 1])
                    with item_col1:
                        st.write(f"${prod['price']:.2f} x {qty} = **${item_total:.2f}**")
                    with item_col2:
                        q_col1, q_col2 = st.columns(2)
                        with q_col1:
                            if st.button("➕", key=f"cart_inc_{pid}"):
                                st.session_state.cart[pid] = qty + 1
                                st.rerun()
                        with q_col2:
                            if st.button("➖", key=f"cart_dec_{pid}"):
                                st.session_state.cart[pid] = max(0, qty - 1)
                                if st.session_state.cart[pid] == 0:
                                    del st.session_state.cart[pid]
                                st.rerun()
                    st.markdown("<hr style='margin: 0.4rem 0;'>", unsafe_allow_html=True)
                
                # Coupon Input
                if "coupon" not in st.session_state:
                    st.session_state.coupon = None
                    
                coupon_input = st.text_input("Promo Code", value=st.session_state.coupon or "", placeholder="Try GROW50 or AGRISMART")
                
                discount_pct = 0.0
                if coupon_input.upper() == "GROW50":
                    st.success("Grower's Special: 50% discount applied!")
                    discount_pct = 0.50
                    st.session_state.coupon = "GROW50"
                elif coupon_input.upper() == "AGRISMART":
                    st.success("AgriSmart: 20% discount applied!")
                    discount_pct = 0.20
                    st.session_state.coupon = "AGRISMART"
                elif coupon_input:
                    st.error("Invalid coupon code.")
                    st.session_state.coupon = None
                    
                discount = subtotal * discount_pct
                shipping = 5.0 if subtotal < 50 else 0.0
                tax = (subtotal - discount) * 0.08
                grand_total = subtotal - discount + shipping + tax
                
                st.markdown(f"""
                <div style="background: #F8FAF8; padding: 1rem; border-radius: 8px; margin-top: 1rem; font-size: 0.9rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                        <span>Subtotal:</span>
                        <span>${subtotal:.2f}</span>
                    </div>
                    {f'<div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem; color: #C62828;"><span>Discount ({discount_pct*100:.0f}%):</span><span>-${discount:.2f}</span></div>' if discount > 0 else ''}
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                        <span>Shipping:</span>
                        <span>{"FREE" if shipping == 0 else f"${shipping:.2f}"}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                        <span>Tax (8%):</span>
                        <span>${tax:.2f}</span>
                    </div>
                    <hr style="margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 1.1rem; color: #2E7D32;">
                        <span>Total:</span>
                        <span>${grand_total:.2f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.checkout_step == "cart":
                    if st.button("Proceed to Checkout 💳", use_container_width=True):
                        st.session_state.checkout_step = "checkout"
                        st.rerun()

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
