import os
import json

def load_knowledge_base():
    """
    Load the disease information JSON database.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    kb_path = os.path.join(base_dir, "knowledge_base", "disease_info.json")
    
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
