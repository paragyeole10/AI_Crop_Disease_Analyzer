import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix, ConfusionMatrixDisplay
from src.config import load_config, get_absolute_path

def evaluate_model(model, history, test_data, all_dirs, training_duration, epochs_trained):
    """
    Evaluates the model on the test dataset and saves evaluation artifacts (JSON metrics and plots).
    """
    config = load_config()
    X_test, y_test = test_data
    
    print("\n" + "=" * 60)
    print("      AGRIVISION AI - EVALUATION PIPELINE       ")
    print("=" * 60)
    print("Evaluating model on the test split...")
    
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")
    
    predictions = model.predict(X_test)
    y_pred = np.argmax(predictions, axis=1)
    
    precision, recall, f1_score, _ = precision_recall_fscore_support(
        y_test, y_pred, average='weighted', zero_division=0
    )
    
    print(f"Weighted Precision: {precision:.4f}")
    print(f"Weighted Recall:    {recall:.4f}")
    print(f"Weighted F1 Score:  {f1_score:.4f}")
    
    # Save metrics JSON
    metrics_summary = {
        "accuracy": float(test_acc),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1_score),
        "test_loss": float(test_loss),
        "epochs_trained": epochs_trained,
        "training_time_seconds": float(training_duration),
        "num_classes": len(all_dirs),
        "classes_list": all_dirs
    }
    
    metrics_save_path = get_absolute_path(config.get("paths", {}).get("metrics_json", "assets/model_metrics.json"))
    os.makedirs(os.path.dirname(metrics_save_path), exist_ok=True)
    with open(metrics_save_path, "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2)
    print(f"Saved metrics data to {metrics_save_path}")
    
    # Generate Plots
    plots_dir = get_absolute_path(config.get("paths", {}).get("plots_dir", "assets/images"))
    os.makedirs(plots_dir, exist_ok=True)
    
    # 1. Training curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.plot(history.history['accuracy'], label='Train Accuracy', color='#2E7D32', marker='o')
    ax1.plot(history.history['val_accuracy'], label='Val Accuracy', color='#FF9800', marker='x')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    ax2.plot(history.history['loss'], label='Train Loss', color='#C62828', marker='o')
    ax2.plot(history.history['val_loss'], label='Val Loss', color='#FF9800', marker='x')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    history_plot_path = os.path.join(plots_dir, "training_history.png")
    plt.savefig(history_plot_path, dpi=150)
    plt.close()
    print(f"Saved training history plot to {history_plot_path}")
    
    # 2. Confusion Matrix
    fig, ax = plt.subplots(figsize=(12, 10))
    display_labels = [c.replace("Corn___", "C_").replace("Potato___", "P_").replace("Rice___", "R_").replace("Sugarcane___", "S_").replace("Wheat___", "W_") for c in all_dirs]
    cm = confusion_matrix(y_test, y_pred)
    
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=display_labels)
    disp.plot(ax=ax, cmap='YlGn', xticks_rotation='vertical', colorbar=True)
    
    plt.title('Confusion Matrix on Test Dataset', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    cm_plot_path = os.path.join(plots_dir, "confusion_matrix.png")
    plt.savefig(cm_plot_path, dpi=150)
    plt.close()
    print(f"Saved confusion matrix plot to {cm_plot_path}")
    
    print("\n" + "=" * 60)
    print("   MODEL EVALUATION PIPELINE COMPLETED   ")
    print("=" * 60)
    
    return metrics_summary
