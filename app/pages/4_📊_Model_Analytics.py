import sys
import os
# Add project root to sys.path dynamically
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import streamlit as st
from src.config import load_config, get_absolute_path

# 2. Setup config & file paths
config = load_config()
metrics_rel_path = config.get("paths", {}).get("metrics_json", "assets/model_metrics.json")
metrics_path = get_absolute_path(metrics_rel_path)

st.markdown("## 📊 Model Performance & Training Analytics")
st.markdown("View training metrics, accuracy curves, and class confusion matrices computed on agricultural crop leaf datasets.")

if not os.path.exists(metrics_path):
    st.info("💡 **No Analytics Data Found**: Training metrics files will be displayed here once you complete running `python train.py` on your machine.")
else:
    try:
        with open(metrics_path, "r", encoding="utf-8") as f:
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
        
        plots_dir = config.get("paths", {}).get("plots_dir", "assets/images")
        history_plot = get_absolute_path(os.path.join(plots_dir, "training_history.png"))
        cm_plot = get_absolute_path(os.path.join(plots_dir, "confusion_matrix.png"))
        
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
