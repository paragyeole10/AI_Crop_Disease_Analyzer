import sys
import os
# Add project root to sys.path dynamically
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import base64
import streamlit as st
from PIL import Image
from src.config import load_config, get_absolute_path
from src.preprocessing.preprocess import preprocess_image
from src.prediction.predictor import CropDiseasePredictor
from src.helpers import get_disease_details
from src.marketplace import get_recommended_products

# 2. Config & Predictor setup
config = load_config()
model_rel_path = config.get("model", {}).get("save_path", "models/crop_disease_model.h5")
model_path = get_absolute_path(model_rel_path)
model_exists = os.path.exists(model_path)

@st.cache_resource
def get_predictor():
    return CropDiseasePredictor()

def get_base64_image(image_path):
    """Convert a local product image to base64 string to embed in HTML."""
    try:
        abs_path = get_absolute_path(image_path)
        if abs_path and os.path.exists(abs_path):
            with open(abs_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception:
        pass
    return ""

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
        col_img, col_res = st.columns([1, 1.2])
        
        with col_img:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Crop Leaf", use_container_width=True)
            
        with col_res:
            with st.spinner("Analyzing leaf patterns..."):
                try:
                    # Preprocess and predict
                    preprocessed = preprocess_image(uploaded_file)
                    predictor = get_predictor()
                    predicted_class, confidence = predictor.predict(preprocessed)
                    
                    # Fetch database details
                    details = get_disease_details(predicted_class)
                    
                    # Store in session state for recommendations
                    st.session_state.last_diagnosis = {
                        "class_name": predicted_class,
                        "disease_name": details['disease_name']
                    }
                    
                    is_healthy = "healthy" in predicted_class.lower()
                    badge_class = "badge-healthy" if is_healthy else "badge-diseased"
                    badge_text = "HEALTHY" if is_healthy else "DISEASED / PATTERN DETECTED"
                    
                    # Display results dashboard
                    st.markdown(f"""<div class="result-card">
<span class="status-badge {badge_class}">{badge_text}</span>
<div class="metric-label">Identified Crop Condition</div>
<div class="metric-value" style="color: {'#2E7D32' if is_healthy else '#C62828'}; margin-bottom:1rem;">{details['disease_name']}</div>
</div>""", unsafe_allow_html=True)
                    
                    # Confidence score progress
                    st.markdown(f"**Confidence Level**: `{confidence*100:.2f}%`")
                    st.progress(confidence)
                    
                    # Detail tabs
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
                        for symptom in details.get('symptoms', []):
                            st.markdown(f"- {symptom}")
                            
                    with tab_treat:
                        st.markdown("### Recommended Actionable Treatment")
                        for idx, treat in enumerate(details.get('treatment', [])):
                            st.markdown(f"**{idx + 1}.** {treat}")
                            
                    with tab_prev:
                        st.markdown("### Preventative Strategies")
                        for idx, prev in enumerate(details.get('prevention', [])):
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
                                    
                                st.markdown(f"""<div style="background: #F8FAF8; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem;">
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
</div>""", unsafe_allow_html=True)
                                
                                btn_col1, btn_col2 = st.columns([1, 1])
                                with btn_col1:
                                    if st.button(f"Add to Cart", key=f"add_cart_scan_{prod['id']}"):
                                        st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                                        st.toast(f"Added {prod['name']} to cart!")
                                with btn_col2:
                                    if st.button(f"Buy Now", key=f"buy_now_scan_{prod['id']}"):
                                        st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                                        st.session_state.checkout_step = "checkout"
                                        st.switch_page("pages/3_🛒_Marketplace.py")
                            
                except Exception as e:
                    st.error(f"Prediction Error: {e}")
                    st.exception(e)
