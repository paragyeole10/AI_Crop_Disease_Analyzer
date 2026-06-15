import os
import json
from src.config import load_config, get_absolute_path

def load_knowledge_base():
    """
    Load the disease information JSON database using the path configured in config.yaml.
    Support multilingual databases dynamically.
    """
    config = load_config()
    rel_path = config.get("paths", {}).get("knowledge_base", "knowledge_base/disease_info.json")
    kb_path = get_absolute_path(rel_path)
    
    try:
        import streamlit as st
        lang = st.session_state.get("language", "en")
    except Exception:
        lang = "en"
        
    if lang == "hi":
        loc_path = kb_path.replace("disease_info.json", "disease_info_hi.json")
        if os.path.exists(loc_path):
            kb_path = loc_path
    elif lang == "es":
        loc_path = kb_path.replace("disease_info.json", "disease_info_es.json")
        if os.path.exists(loc_path):
            kb_path = loc_path
            
    if not os.path.exists(kb_path):
        raise FileNotFoundError(f"Knowledge base not found at {kb_path}")
        
    with open(kb_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_disease_details(class_name):
    """
    Get detailed disease profile from the knowledge base.
    
    Parameters:
    - class_name: string label predicted by the model (or folder name)
    
    Returns:
    - dict containing disease_name, description, symptoms, treatment, prevention
    """
    try:
        kb = load_knowledge_base()
        if class_name in kb:
            return kb[class_name]
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        
    # Fallback if class not found or error occurs
    formatted_name = class_name.replace("___", " - ").replace("__", " ").replace("_", " ")
    return {
        "disease_name": formatted_name,
        "description": "Information for this category is currently being updated in our agricultural knowledge base.",
        "symptoms": [
            "Foliar irregularities, discolorations, or spotting.",
            "Potential lesions on fruit or stems."
        ],
        "treatment": [
            "Remove and isolate the affected plant parts.",
            "Ensure proper watering at the base to avoid wetting the leaves.",
            "Consult a local agricultural extension officer or agronomist for targeted treatments."
        ],
        "prevention": [
            "Rotate crops annually to break disease cycles.",
            "Use certified clean seeds or seedlings.",
            "Maintain proper plant spacing for optimal air circulation."
        ]
    }
