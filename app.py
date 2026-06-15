import os
import sys
import streamlit as st

# Ensure root directory is in python search path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 1. Page Configuration (Must be called first in Streamlit apps)
st.set_page_config(
    page_title="AgriVision AI - Smart Crop Disease Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injects custom SaaS styles and sidebar branding globally
from app.components.layout import inject_custom_css, render_sidebar_branding
inject_custom_css()
render_sidebar_branding()

# 3. Session State Initializations
if "language" not in st.session_state:
    st.session_state.language = "en"
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "orders" not in st.session_state:
    st.session_state.orders = []
if "last_diagnosis" not in st.session_state:
    st.session_state.last_diagnosis = None
if "checkout_step" not in st.session_state:
    st.session_state.checkout_step = "cart"
if "current_order_id" not in st.session_state:
    st.session_state.current_order_id = None

# 4. Multi-Page Navigation setup using Streamlit's native Page API
home_page = st.Page("app/pages/0_🏠_Home.py", title="Home", icon="🏠", default=True)
scan_page = st.Page("app/pages/1_🔬_Scan_Leaf.py", title="Scan Leaf", icon="🔬")
library_page = st.Page("app/pages/2_📚_Disease_Library.py", title="Disease Library", icon="📚")
marketplace_page = st.Page("app/pages/3_🛒_Marketplace.py", title="Marketplace", icon="🛒")
analytics_page = st.Page("app/pages/4_📊_Model_Analytics.py", title="Model Analytics", icon="📊")

pg = st.navigation([home_page, scan_page, library_page, marketplace_page, analytics_page])
pg.run()
