import os
import sys
import time
import json
import argparse
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, ConfusionMatrixDisplay

# Ensure reproducibility
np.random.seed(42)
random.seed(42)

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="AgriVision AI - Model Training Pipeline")
    parser.add_argument("--dataset_path", type=str, default=r"d:\Uma_Tai\archive (3)\PlantVillage", help="Path to PlantVillage dataset folder")
    parser.add_argument("--epochs", type=int, default=2, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for training")
    parser.add_argument("--quick_mode", type=str, default="True", help="Use subset of images per class for fast training (True/False)")
    parser.add_argument("--max_samples", type=int, default=100, help="Max samples per class in quick mode")
    
    args = parser.parse_args()
    
    # Parse quick_mode boolean
    quick_mode = args.quick_mode.lower() in ("true", "1", "yes")
    
    print("=" * 60)
    print("      AGRIVISION AI - MODEL TRAINING PIPELINE      ")
    print("=" * 60)
    print(f"Dataset Path: {args.dataset_path}")
    print(f"Quick Mode: {quick_mode} (Max samples per class: {args.max_samples if quick_mode else 'All'})")
    print(f"Epochs: {args.epochs}")
    print(f"Batch Size: {args.batch_size}")
    
    # Check dataset directory
    if not os.path.exists(args.dataset_path):
        print(f"Error: Dataset directory not found at {args.dataset_path}")
        sys.exit(1)
        
    # Get all class subdirectories, ignoring nested 'PlantVillage' folder
    all_dirs = sorted([d for d in os.listdir(args.dataset_path) 
                       if os.path.isdir(os.path.join(args.dataset_path, d)) and d != "PlantVillage"])
    
    print(f"Found {len(all_dirs)} supported classes:")
    for idx, class_name in enumerate(all_dirs):
        print(f"  {idx + 1}. {class_name}")
        
    # 1. Load and Preprocess Dataset
    print("\n[1/6] Loading and Preprocessing dataset...")
    X = []
    y = []
    
    start_load_time = time.time()
    
    for class_idx, class_name in enumerate(all_dirs):
        class_dir = os.path.join(args.dataset_path, class_name)
        image_files = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # In quick mode, sample a subset of images
        if quick_mode and len(image_files) > args.max_samples:
            sampled_files = random.sample(image_files, args.max_samples)
        else:
            sampled_files = image_files
            
        print(f"  Loading {len(sampled_files)}/{len(image_files)} images from '{class_name}'...")
        
        for file_name in sampled_files:
            file_path = os.path.join(class_dir, file_name)
            try:
                # Read image
                img = cv2.imread(file_path)
                if img is None:
                    continue
                # Convert BGR to RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # Resize to 224x224
                img_resized = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
                # Normalize pixel values to [-1, 1] for MobileNetV2
                img_normalized = (img_resized.astype(np.float32) / 127.5) - 1.0
                
                X.append(img_normalized)
                y.append(class_idx)
            except Exception as e:
                print(f"    Failed to process image {file_name}: {e}")
                
    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.int32)
    
    print(f"Loaded a total of {len(X)} images. Loading time: {time.time() - start_load_time:.2f} seconds.")
    print(f"Data shape: {X.shape}, Labels shape: {y.shape}")
    
    # 2. Split Dataset: Train (70%), Validation (15%), Test (15%)
    print("\n[2/6] Splitting dataset into Train, Val, and Test splits...")
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)
    
    print(f"  Train set: {X_train.shape[0]} samples")
    print(f"  Val set:   {X_val.shape[0]} samples")
    print(f"  Test set:  {X_test.shape[0]} samples")
    
    # Delay TensorFlow import until here to let script print diagnostics fast if arguments are wrong
    import tensorflow as tf
    
    # 3. Build Model (MobileNetV2 Transfer Learning)
    print("\n[3/6] Building MobileNetV2 Model...")
    
    # Data Augmentation Layer (runs inside the network during training)
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal_and_vertical"),
        tf.keras.layers.RandomRotation(0.15),
        tf.keras.layers.RandomZoom(0.15),
    ], name="data_augmentation")
    
    # Load MobileNetV2 pretrained on ImageNet
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    # Freeze the convolutional base
    base_model.trainable = False
    
    # Combine layers
    model = tf.keras.models.Sequential([
        tf.keras.Input(shape=(224, 224, 3)),
        data_augmentation,
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(len(all_dirs), activation='softmax')
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    model.summary()
    
    # 4. Train Model
    print("\n[4/6] Training model classification head...")
    start_train_time = time.time()
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=args.epochs,
        batch_size=args.batch_size,
        verbose=1
    )
    
    training_duration = time.time() - start_train_time
    print(f"Training completed in {training_duration:.2f} seconds.")
    
    # Create output folders
    os.makedirs("models", exist_ok=True)
    os.makedirs(os.path.join("assets", "images"), exist_ok=True)
    
    # Save Model
    model_save_path = os.path.join("models", "crop_disease_model.h5")
    print(f"\nSaving model to {model_save_path}...")
    model.save(model_save_path)
    print("Model saved successfully.")
    
    # 5. Evaluate Model
    print("\n[5/6] Evaluating model on the test split...")
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")
    
    # Run predictions on Test set to compute detailed metrics
    predictions = model.predict(X_test)
    y_pred = np.argmax(predictions, axis=1)
    
    # Compute precision, recall, f1-score
    precision, recall, f1_score, _ = precision_recall_fscore_support(
        y_test, y_pred, average='weighted', zero_division=0
    )
    
    print(f"Weighted Precision: {precision:.4f}")
    print(f"Weighted Recall:    {recall:.4f}")
    print(f"Weighted F1 Score:  {f1_score:.4f}")
    
    # Create evaluation metrics JSON file for Streamlit dashboard load
    metrics_summary = {
        "accuracy": float(test_acc),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1_score),
        "test_loss": float(test_loss),
        "epochs_trained": args.epochs,
        "training_time_seconds": float(training_duration),
        "num_classes": len(all_dirs),
        "classes_list": all_dirs
    }
    
    metrics_save_path = os.path.join("assets", "model_metrics.json")
    with open(metrics_save_path, "w") as f:
        json.dump(metrics_summary, f, indent=2)
    print(f"Saved metrics data to {metrics_save_path}")
    
    # 6. Generate and Save Visualizations
    print("\n[6/6] Generating evaluation plots...")
    
    # Plot 1: Accuracy & Loss curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Accuracy
    ax1.plot(history.history['accuracy'], label='Train Accuracy', color='#2E7D32', marker='o')
    ax1.plot(history.history['val_accuracy'], label='Val Accuracy', color='#FF9800', marker='x')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # Loss
    ax2.plot(history.history['loss'], label='Train Loss', color='#C62828', marker='o')
    ax2.plot(history.history['val_loss'], label='Val Loss', color='#FF9800', marker='x')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    history_plot_path = os.path.join("assets", "images", "training_history.png")
    plt.savefig(history_plot_path, dpi=150)
    plt.close()
    print(f"Saved training history plot to {history_plot_path}")
    
    # Plot 2: Confusion Matrix
    fig, ax = plt.subplots(figsize=(12, 10))
    # Standard labels display (abbreviated classes for better sizing on visual)
    display_labels = [c.replace("Tomato__", "T_").replace("Potato___", "P_").replace("Pepper__bell___", "PB_") for c in all_dirs]
    cm = confusion_matrix(y_test, y_pred)
    
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=display_labels)
    disp.plot(ax=ax, cmap='YlGn', xticks_rotation='vertical', colorbar=True)
    
    plt.title('Confusion Matrix on Test Dataset', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    cm_plot_path = os.path.join("assets", "images", "confusion_matrix.png")
    plt.savefig(cm_plot_path, dpi=150)
    plt.close()
    print(f"Saved confusion matrix plot to {cm_plot_path}")
    
    print("\n" + "=" * 60)
    print("   MODEL TRAINING AND EVALUATION PIPELINE COMPLETED   ")
    print("=" * 60)

if __name__ == "__main__":
    main()
