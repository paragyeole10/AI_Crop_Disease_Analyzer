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
from utils.tts_service import TTSService, TTSServiceException

# 2. Config & Predictor setup
config = load_config()
model_rel_path = config.get("model", {}).get("save_path", "models/mobilenet_crop_disease.keras")
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

from src.translations import t

st.markdown(f"## {t('scan_title')}")
st.markdown(t('scan_subtitle'))

if not model_exists:
    st.error(t('model_offline'))
else:
    uploaded_file = st.file_uploader(
        t('choose_image'), 
        type=["jpg", "jpeg", "png"],
        help=t('image_help')
    )
    
    if uploaded_file is not None:
        if "last_uploaded_file" not in st.session_state or st.session_state.last_uploaded_file != uploaded_file.name:
            st.session_state.last_uploaded_file = uploaded_file.name
            if "tts_audio_path" in st.session_state and st.session_state.tts_audio_path:
                try:
                    TTSService().cleanup_file(st.session_state.tts_audio_path)
                except Exception:
                    pass
                st.session_state.tts_audio_path = None
                
        col_img, col_res = st.columns([1, 1.2])
        
        with col_img:
            image = Image.open(uploaded_file)
            st.image(image, caption=t('uploaded_caption'), use_container_width=True)
            
        with col_res:
            with st.spinner(t('analyzing')):
                try:
                    # Preprocess and predict
                    preprocessed = preprocess_image(uploaded_file)
                    predictor = get_predictor()
                    
                    # Get top 3 predictions to satisfy FR-3
                    top_k_preds = predictor.predict_top_k(preprocessed, k=3)
                    predicted_class, confidence = top_k_preds[0]
                    
                    # Fetch database details for top prediction
                    details = get_disease_details(predicted_class)
                    
                    # Store in session state for recommendations
                    st.session_state.last_diagnosis = {
                        "class_name": predicted_class,
                        "disease_name": details['disease_name']
                    }
                    
                    is_healthy = "healthy" in predicted_class.lower()
                    badge_class = "badge-healthy" if is_healthy else "badge-diseased"
                    badge_text = t('status_healthy') if is_healthy else t('status_diseased')
                    
                    # Display results dashboard
                    st.markdown(f"""<div class="result-card">
<span class="status-badge {badge_class}">{badge_text}</span>
<div class="metric-label">{t('identified_condition')}</div>
<div class="metric-value" style="color: {'#2E7D32' if is_healthy else '#C62828'}; margin-bottom:1rem;">{details['disease_name']}</div>
</div>""", unsafe_allow_html=True)
                    
                    # FR-9: Healthy Crop Handling
                    if is_healthy:
                        st.success("🌱 **Healthy Crop Detected!** Enjoy your healthy field. Below are crop health tips, fertilizer recommendations, and best maintenance practices.")
                    
                    # FR-3: Confidence Visualization (Top 3 Predictions)
                    st.markdown(f"### {t('confidence_level')} (Top 3 Predictions)")
                    for c_name, conf in top_k_preds:
                        c_details = get_disease_details(c_name)
                        st.markdown(f"**{c_details['disease_name']}**: `{conf*100:.2f}%`")
                        st.progress(conf)
                    
                    # Generate TTS Text for Audio Guide using server-side gTTS
                    st.markdown("---")
                    st.markdown("### 🎙️ Audio Guide / ऑडिओ मार्गदर्शक / ऑडियो मार्गदर्शिका")
                    
                    tts_lang = st.selectbox(
                        "Choose Audio Language / आवाजाची भाषा निवडा / ऑडियो भाषा चुनें",
                        options=["en", "hi", "mr"],
                        format_func=lambda x: {"en": "English", "hi": "हिन्दी (Hindi)", "mr": "मराठी (Marathi)"}[x],
                        key="tts_lang_selector"
                    )
                    
                    if st.button("🔊 Listen Result / परिणाम ऐका / परिणाम सुनें", use_container_width=True):
                        try:
                            # Construct narrative text based on selected language
                            # Fetch disease details in that language
                            with st.spinner("Generating audio guide..." if tts_lang == "en" else ("ऑडिओ मार्गदर्शक तयार करत आहे..." if tts_lang == "mr" else "ऑडियो गाइड तैयार किया जा रहा है...")):
                                tts_details = get_disease_details(predicted_class, lang=tts_lang)
                                disease_name_tts = tts_details['disease_name']
                                confidence_percent_tts = f"{confidence * 100:.1f}"
                                
                                symptoms_list = tts_details.get('symptoms', [])
                                treatment_list = tts_details.get('treatment', [])
                                prevention_list = tts_details.get('prevention', [])
                                
                                if tts_lang == "hi":
                                    symptoms_txt = "। ".join(symptoms_list)
                                    treatment_txt = "। ".join(treatment_list)
                                    prevention_txt = "। ".join(prevention_list)
                                    
                                    narrative_text = f"निदान परिणाम: {disease_name_tts} ({confidence_percent_tts} प्रतिशत विश्वास के साथ)। "
                                    if symptoms_txt:
                                        narrative_text += f"देखने योग्य लक्षण: {symptoms_txt}। "
                                    if treatment_txt:
                                        narrative_text += f"अनुशंसित उपचार: {treatment_txt}। "
                                    if prevention_txt:
                                        narrative_text += f"निवारक रणनीतियाँ: {prevention_txt}।"
                                        
                                elif tts_lang == "mr":
                                    symptoms_txt = ". ".join(symptoms_list)
                                    treatment_txt = ". ".join(treatment_list)
                                    prevention_txt = ". ".join(prevention_list)
                                    
                                    narrative_text = f"निदान निकाल: {disease_name_tts} ({confidence_percent_tts} टक्के विश्वास)। "
                                    if symptoms_txt:
                                        narrative_text += f"दिसणारी लक्षणे: {symptoms_txt}. "
                                    if treatment_txt:
                                        narrative_text += f"शिफारस केलेले उपचार: {treatment_txt}. "
                                    if prevention_txt:
                                        narrative_text += f"प्रतिबंधात्मक उपाय: {prevention_txt}."
                                        
                                else: # English
                                    symptoms_txt = ", ".join(symptoms_list)
                                    treatment_txt = ", ".join(treatment_list)
                                    prevention_txt = ", ".join(prevention_list)
                                    
                                    narrative_text = f"Diagnosis result: {disease_name_tts} with {confidence_percent_tts} percent confidence. "
                                    if symptoms_txt:
                                        narrative_text += f"Symptoms to look for: {symptoms_txt}. "
                                    if treatment_txt:
                                        narrative_text += f"Recommended treatments: {treatment_txt}. "
                                    if prevention_txt:
                                        narrative_text += f"Preventative strategies: {prevention_txt}."
                                
                                # Clean up previous file if any exists
                                if "tts_audio_path" in st.session_state and st.session_state.tts_audio_path:
                                    try:
                                        TTSService().cleanup_file(st.session_state.tts_audio_path)
                                    except Exception:
                                        pass
                                
                                # Generate the audio file
                                tts_service = TTSService()
                                audio_file_path = tts_service.generate_audio(narrative_text, language=tts_lang)
                                st.session_state.tts_audio_path = audio_file_path
                                st.toast("Audio generated successfully!" if tts_lang == "en" else ("ऑडिओ यशस्वीरित्या तयार केला!" if tts_lang == "mr" else "ऑडियो सफलतापूर्वक तैयार किया गया!"))
                        except TTSServiceException as ex:
                            st.error(f"🎙️ {str(ex)}")
                        except Exception as ex:
                            st.error(f"🎙️ Failed to generate speech: {str(ex)}")
                            
                    # If we have generated audio in this session, render it
                    if "tts_audio_path" in st.session_state and st.session_state.tts_audio_path and os.path.exists(st.session_state.tts_audio_path):
                        st.audio(st.session_state.tts_audio_path, format="audio/mp3")
                    
                    # Detail tabs
                    st.markdown("---")
                    tab_desc, tab_sym, tab_treat, tab_prev, tab_shop = st.tabs([
                        t('tab_info'), 
                        t('tab_symptoms'), 
                        t('tab_treatment'), 
                        t('tab_prevention'),
                        t('tab_shop')
                    ])
                    
                    with tab_desc:
                        st.markdown(f"**{t('desc_label')}**:\n{details['description']}")
                        
                    with tab_sym:
                        st.markdown(f"### {t('symptoms_look_for')}")
                        for symptom in details.get('symptoms', []):
                            st.markdown(f"- {symptom}")
                            
                    with tab_treat:
                        st.markdown(f"### {t('recommended_treatment')}")
                        for idx, treat in enumerate(details.get('treatment', [])):
                            st.markdown(f"**{idx + 1}.** {treat}")
                            
                    with tab_prev:
                        st.markdown(f"### {t('preventative_strategies')}")
                        for idx, prev in enumerate(details.get('prevention', [])):
                            st.markdown(f"**{idx + 1}.** {prev}")
                            
                    with tab_shop:
                        st.markdown(f"### {t('recommended_products_title')}")
                        st.markdown(t('recommended_products_subtitle'))
                        
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
<span style="font-size: 1.15rem; font-weight: 700; color: #2E7D32;">₹{prod['price']:.2f}</span>
<span style="font-size: 0.85rem; color: #F59E0B; font-weight: 600;">⭐ {prod['rating']} / 5.0</span>
</div>
</div>""", unsafe_allow_html=True)
                                
                                btn_col1, btn_col2 = st.columns([1, 1])
                                with btn_col1:
                                    if st.button(t('add_to_cart'), key=f"add_cart_scan_{prod['id']}", use_container_width=True):
                                        st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                                        st.toast(t('added_to_cart_toast').format(prod['name']))
                                with btn_col2:
                                    if st.button(t('buy_now'), key=f"buy_now_scan_{prod['id']}", use_container_width=True):
                                        st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                                        st.session_state.checkout_step = "checkout"
                                        st.switch_page("pages/3_🛒_Marketplace.py")
                            
                except Exception as e:
                    st.error(f"Prediction Error: {e}")
                    st.exception(e)
