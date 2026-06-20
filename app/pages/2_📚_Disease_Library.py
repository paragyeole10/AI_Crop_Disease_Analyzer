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

from src.translations import t

st.markdown(f"## {t('lib_title')}")
st.markdown(t('lib_subtitle'))

try:
    kb = load_knowledge_base()
    
    # Process Voice command input
    voice_query = st.query_params.get("disease_voice", "")
    if voice_query:
        voice_query_lower = voice_query.lower()
        matched_class = None
        for k, v in kb.items():
            disease_name = v['disease_name'].lower()
            if voice_query_lower in disease_name or voice_query_lower in k.lower():
                matched_class = k
                break
        
        if matched_class:
            if "corn" in matched_class.lower():
                st.session_state.disease_lib_crop = "Corn"
            elif "potato" in matched_class.lower():
                st.session_state.disease_lib_crop = "Potato"
            elif "rice" in matched_class.lower():
                st.session_state.disease_lib_crop = "Rice"
            elif "sugarcane" in matched_class.lower():
                st.session_state.disease_lib_crop = "Sugarcane"
            elif "wheat" in matched_class.lower():
                st.session_state.disease_lib_crop = "Wheat"
            else:
                st.session_state.disease_lib_crop = "All"
                
            st.session_state.disease_lib_class = matched_class
            
        st.query_params.pop("disease_voice", None)
        
    # Crop filter
    crops_options = ["All", "Corn", "Potato", "Rice", "Sugarcane", "Wheat"]
    crops_labels = {
        "All": t('all_crops'),
        "Corn": t('crop_corn_opt'),
        "Potato": t('crop_potato_opt'),
        "Rice": t('crop_rice_opt'),
        "Sugarcane": t('crop_sugarcane_opt'),
        "Wheat": t('crop_wheat_opt')
    }
    
    if "disease_lib_crop" not in st.session_state:
        st.session_state.disease_lib_crop = "All"
        
    crop_filter_idx = crops_options.index(st.session_state.disease_lib_crop)
    crop_filter = st.selectbox(
        t('filter_crop'), 
        options=crops_options,
        index=crop_filter_idx,
        format_func=lambda x: crops_labels[x],
        key="disease_lib_crop"
    )
    
    # Filter classes
    filtered_classes = {}
    for k, v in kb.items():
        if crop_filter == "Corn" and "corn" not in k.lower():
            continue
        elif crop_filter == "Potato" and "potato" not in k.lower():
            continue
        elif crop_filter == "Rice" and "rice" not in k.lower():
            continue
        elif crop_filter == "Sugarcane" and "sugarcane" not in k.lower():
            continue
        elif crop_filter == "Wheat" and "wheat" not in k.lower():
            continue
        filtered_classes[k] = v
        
    # Determine default class choice index
    default_choice_idx = 0
    if "disease_lib_class" in st.session_state and st.session_state.disease_lib_class in filtered_classes:
        default_choice_idx = list(filtered_classes.keys()).index(st.session_state.disease_lib_class)
        
    col_sel, col_mic = st.columns([6, 1])
    with col_sel:
        class_choice = st.selectbox(
            t('select_profile'),
            options=list(filtered_classes.keys()),
            index=default_choice_idx,
            format_func=lambda x: filtered_classes[x]['disease_name'],
            key="disease_lib_class"
        )
    with col_mic:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        from app.components.layout import render_voice_search
        render_voice_search(
            target_placeholder="",
            language_code=st.session_state.get("language", "en"),
            key="disease_search",
            use_query_param=True,
            query_param_name="disease_voice"
        )
        
    if class_choice:
        profile = filtered_classes[class_choice]
        is_healthy = "healthy" in class_choice.lower()
        
        st.markdown("---")
        lib_tab_profile, lib_tab_shop = st.tabs([t('tab_profile'), t('tab_shop_recs')])
        
        with lib_tab_profile:
            # Render TTS Narrator for selected Profile
            lang = st.session_state.get("language", "en")
            disease_name = profile['disease_name']
            status_lbl = t('status_healthy_lbl') if is_healthy else t('status_diseased_lbl')
            desc = profile['description']
            
            # Truncate description for narration
            desc_sentences = desc.split(".")
            short_desc = ". ".join(desc_sentences[:2]) + "." if len(desc_sentences) > 0 else desc
            
            symptoms_txt = ", ".join(profile.get('symptoms', []))
            treatment_txt = ", ".join(profile.get('treatment', []))
            
            if lang == "hi":
                tts_text = f"रोग प्रोफ़ाइल: {disease_name}। स्थिति: {status_lbl}। विवरण: {short_desc} लक्षण: {symptoms_txt}। अनुशंसित उपचार: {treatment_txt}।"
            elif lang == "es":
                tts_text = f"Perfil de enfermedad: {disease_name}. Estado: {status_lbl}. Descripción: {short_desc} Síntomas: {symptoms_txt}. Tratamientos recomendados: {treatment_txt}."
            else:
                tts_text = f"Disease Profile: {disease_name}. Status: {status_lbl}. Description: {short_desc} Symptoms: {symptoms_txt}. Recommended treatments: {treatment_txt}."
            
            from app.components.layout import render_voice_player
            render_voice_player(tts_text, lang, key=f"profile_{class_choice}")
            
            col_info, col_bullets = st.columns([1.2, 1])
            
            with col_info:
                st.subheader(profile['disease_name'])
                status_lbl = t('status_healthy_lbl') if is_healthy else t('status_diseased_lbl')
                st.markdown(f"**{t('condition_status')}**: `{status_lbl}`")
                st.markdown(f"**{t('description_lbl')}**:\n{profile['description']}")
                
                st.markdown(f"<br><h4>{t('preventative_measures_lbl')}</h4>", unsafe_allow_html=True)
                for idx, prev in enumerate(profile.get('prevention', [])):
                    st.markdown(f"**{idx+1}.** {prev}")
                    
            with col_bullets:
                st.markdown(f"<h4>{t('symptoms_lbl')}</h4>", unsafe_allow_html=True)
                for symptom in profile.get('symptoms', []):
                    st.markdown(f"- {symptom}")
                    
                st.markdown(f"<br><h4>{t('recommended_treatments_lbl')}</h4>", unsafe_allow_html=True)
                for idx, treat in enumerate(profile.get('treatment', [])):
                    st.markdown(f"**{idx+1}.** {treat}")
                    
        with lib_tab_shop:
            st.markdown(f"### {t('recommended_products_title')}")
            st.markdown(t('recommended_products_subtitle'))
            
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
                        if st.button(t('add_to_cart'), key=f"add_cart_lib_{prod['id']}", use_container_width=True):
                            st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                            st.toast(t('added_to_cart_toast').format(prod['name']))
                    with btn_col2:
                        if st.button(t('buy_now'), key=f"buy_now_lib_{prod['id']}", use_container_width=True):
                            st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                            st.session_state.checkout_step = "checkout"
                            st.switch_page("pages/3_🛒_Marketplace.py")
                
except Exception as e:
    st.error(f"Failed to load disease library: {e}")
