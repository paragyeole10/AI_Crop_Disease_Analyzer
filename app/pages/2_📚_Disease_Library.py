import sys
import os
# Add project root to sys.path dynamically
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import base64
import streamlit as st
from src.config import load_config, get_absolute_path
from src.helpers import load_knowledge_base, get_disease_details
from src.marketplace import get_recommended_products

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

st.markdown("## 📚 Agricultural Disease Library")
st.markdown("Browse crop health profiles, diagnostic guides, and treatment procedures for all supported categories.")

try:
    kb = load_knowledge_base()
    
    # Crop filter
    crop_filter = st.selectbox("Filter by Crop Category", ["All Crops", "Tomato 🍅", "Potato 🥔", "Pepper Bell 🫑"])
    
    # Filter classes
    filtered_classes = {}
    for k, v in kb.items():
        if crop_filter == "Tomato 🍅" and "tomato" not in k.lower():
            continue
        elif crop_filter == "Potato 🥔" and "potato" not in k.lower():
            continue
        elif crop_filter == "Pepper Bell 🫑" and "pepper" not in k.lower():
            continue
        filtered_classes[k] = v
        
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
                for idx, prev in enumerate(profile.get('prevention', [])):
                    st.markdown(f"**{idx+1}.** {prev}")
                    
            with col_bullets:
                st.markdown("<h4>🔍 Symptoms</h4>", unsafe_allow_html=True)
                for symptom in profile.get('symptoms', []):
                    st.markdown(f"- {symptom}")
                    
                st.markdown("<br><h4>💊 Recommended Treatments</h4>", unsafe_allow_html=True)
                for idx, treat in enumerate(profile.get('treatment', [])):
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
                        if st.button(f"Add to Cart", key=f"add_cart_lib_{prod['id']}"):
                            st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                            st.toast(f"Added {prod['name']} to cart!")
                    with btn_col2:
                        if st.button(f"Buy Now", key=f"buy_now_lib_{prod['id']}"):
                            st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                            st.session_state.checkout_step = "checkout"
                            st.switch_page("pages/3_🛒_Marketplace.py")
                
except Exception as e:
    st.error(f"Failed to load disease library: {e}")
