import streamlit as st
import os

def inject_custom_css():
    """
    Injects custom CSS styling for premium SaaS aesthetics.
    """
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

def render_sidebar_branding():
    """
    Renders the sidebar branding elements.
    """
    with st.sidebar:
        logo_path = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png"))
        if os.path.exists(logo_path):
            st.image(logo_path, width=80)
        else:
            st.image("https://img.icons8.com/color/96/000000/sprout.png", width=80)
        st.markdown("<h2 style='margin-top:0;'>AgriVision AI</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; font-size: 0.9rem;'>Smart Crop Health Intelligence</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### Supported Crops")
        st.markdown("- 🍅 Tomato (11 classes)")
        st.markdown("- 🥔 Potato (3 classes)")
        st.markdown("- 🫑 Pepper Bell (2 classes)")
        
        st.markdown("<div style='position: fixed; bottom: 10px; font-size: 0.8rem; color: #94A3B8;'>Phase 1 - Release v1.0.0</div>", unsafe_allow_html=True)
