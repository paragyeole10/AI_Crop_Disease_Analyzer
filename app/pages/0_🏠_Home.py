import sys
import os
# Add project root to sys.path dynamically
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from src.config import load_config, get_absolute_path
from src.translations import t

config = load_config()
model_rel_path = config.get("model", {}).get("save_path", "models/crop_disease_model.h5")
model_path = get_absolute_path(model_rel_path)
model_exists = os.path.exists(model_path)

# Hero Section
st.markdown(f"""<div class="hero-container">
<div class="hero-title">{t('hero_title')}</div>
<div class="hero-subtitle">{t('hero_subtitle')}</div>
</div>""", unsafe_allow_html=True)

# Core Capabilities
st.markdown(f"<h2 style='text-align: center; color: #1E293B; margin-bottom: 2rem;'>{t('core_capabilities')}</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""<div class="feature-card">
<div class="feature-icon">🔬</div>
<div class="feature-title">{t('detection_title')}</div>
<div class="feature-text">{t('detection_desc')}</div>
</div>""", unsafe_allow_html=True)
    
with col2:
    st.markdown(f"""<div class="feature-card">
<div class="feature-icon">🛡️</div>
<div class="feature-title">{t('guidance_title')}</div>
<div class="feature-text">{t('guidance_desc')}</div>
</div>""", unsafe_allow_html=True)
    
with col3:
    st.markdown(f"""<div class="feature-card">
<div class="feature-icon">📋</div>
<div class="feature-title">{t('prevention_title')}</div>
<div class="feature-text">{t('prevention_desc')}</div>
</div>""", unsafe_allow_html=True)
    
with col4:
    st.markdown(f"""<div class="feature-card">
<div class="feature-icon">⚡</div>
<div class="feature-title">{t('fast_analysis_title')}</div>
<div class="feature-text">{t('fast_analysis_desc')}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# How It Works
st.markdown(f"### {t('how_it_works')}")
col_step1, col_step2, col_step3 = st.columns(3)
with col_step1:
    st.info(f"**{t('step1_title')}**\n{t('step1_desc')}")
with col_step2:
    st.info(f"**{t('step2_title')}**\n{t('step2_desc')}")
with col_step3:
    st.info(f"**{t('step3_title')}**\n{t('step3_desc')}")
    
if not model_exists:
    st.warning(t('model_warning'))
