import os
import sys
import time
import random
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from src.config import load_config, get_absolute_path

# Ensure reproducibility
np.random.seed(42)
random.seed(42)

def run_training(dataset_path=None, epochs=None, batch_size=None, quick_mode=None, max_samples=None):
    """
    Executes the model training pipeline.
    """
    config = load_config()
    
    # Resolve parameters with configs or fallbacks
    dataset_path = dataset_path or get_absolute_path(config.get("dataset", {}).get("path", ""))
    epochs = epochs or config.get("training", {}).get("epochs", 2)
    batch_size = batch_size or config.get("training", {}).get("batch_size", 32)
    if quick_mode is None:
        quick_mode = config.get("training", {}).get("quick_mode", True)
    max_samples = max_samples or config.get("training", {}).get("max_samples", 100)
    save_path = get_absolute_path(config.get("model", {}).get("save_path", "models/crop_disease_model.h5"))
    
    print("=" * 60)
    print("      AGRIVISION AI - TRAINING CORE PIPELINE       ")
    print("=" * 60)
    print(f"Dataset Path: {dataset_path}")
    print(f"Quick Mode: {quick_mode} (Max samples per class: {max_samples if quick_mode else 'All'})")
    print(f"Epochs: {epochs}")
    print(f"Batch Size: {batch_size}")
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset directory not found at {dataset_path}")
        
    all_dirs = sorted([d for d in os.listdir(dataset_path) 
                       if os.path.isdir(os.path.join(dataset_path, d)) and d != "PlantVillage"])
    
    print(f"Found {len(all_dirs)} supported classes.")
    
    # 1. Load and Preprocess Dataset
    print("\n[1/4] Loading and Preprocessing dataset...")
    X = []
    y = []
    
    start_load_time = time.time()
    
    for class_idx, class_name in enumerate(all_dirs):
        class_dir = os.path.join(dataset_path, class_name)
        image_files = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if quick_mode and len(image_files) > max_samples:
            sampled_files = random.sample(image_files, max_samples)
        else:
            sampled_files = image_files
            
        print(f"  Loading {len(sampled_files)}/{len(image_files)} images from '{class_name}'...")
        
        for file_name in sampled_files:
            file_path = os.path.join(class_dir, file_name)
            try:
                img = cv2.imread(file_path)
                if img is None:
                    continue
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_resized = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
                img_normalized = (img_resized.astype(np.float32) / 127.5) - 1.0
                
                X.append(img_normalized)
                y.append(class_idx)
            except Exception as e:
                print(f"    Failed to process image {file_name}: {e}")
                
    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.int32)
    
    print(f"Loaded a total of {len(X)} images in {time.time() - start_load_time:.2f} seconds.")
    
    # 2. Split Dataset
    print("\n[2/4] Splitting dataset into Train, Val, and Test splits...")
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)
    
    # Import TensorFlow inside training pipeline
    import tensorflow as tf
    
    # 3. Build Model (MobileNetV2 Transfer Learning)
    print("\n[3/4] Building MobileNetV2 Model...")
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal_and_vertical"),
        tf.keras.layers.RandomRotation(0.15),
        tf.keras.layers.RandomZoom(0.15),
    ], name="data_augmentation")
    
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights=config.get("model", {}).get("weights", "imagenet")
    )
    base_model.trainable = False
    
    model = tf.keras.models.Sequential([
        tf.keras.Input(shape=(224, 224, 3)),
        data_augmentation,
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dropout(config.get("model", {}).get("dropout_rate", 0.2)),
        tf.keras.layers.Dense(len(all_dirs), activation='softmax')
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=config.get("training", {}).get("learning_rate", 0.001)),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    model.summary()
    
    # 4. Train Model
    print("\n[4/4] Stage 1 - Training classification head (Frozen Base)...")
    start_train_time = time.time()
    
    stage1_epochs = min(5, epochs)
    stage2_epochs = max(0, epochs - stage1_epochs)
    
    # Setup callbacks
    checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
        filepath=save_path,
        monitor='val_loss',
        save_best_only=True,
        verbose=1
    )
    early_stop_cb = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=4,
        restore_best_weights=True,
        verbose=1
    )
    reduce_lr_cb = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=2,
        min_lr=1e-6,
        verbose=1
    )
    
    # Train stage 1
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=stage1_epochs,
        batch_size=batch_size,
        callbacks=[checkpoint_cb, reduce_lr_cb],
        verbose=1
    )
    
    # Stage 2: Fine-Tuning
    if stage2_epochs > 0:
        print("\nStage 2 - Fine-Tuning top base model layers (Unfrozen from layer 100 onwards)...")
        # Unfreeze MobileNetV2 base
        base_model.trainable = True
        # Freeze initial layers to retain basic feature extractors
        for layer in base_model.layers[:100]:
            layer.trainable = False
            
        # Compile with a very low learning rate for fine-tuning
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        model.summary()
        
        # Fit Stage 2
        history2 = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=stage2_epochs,
            batch_size=batch_size,
            callbacks=[checkpoint_cb, early_stop_cb, reduce_lr_cb],
            verbose=1
        )
        
        # Merge history dictionary lists
        for key in history.history.keys():
            if key in history2.history:
                history.history[key].extend(history2.history[key])
                
    training_duration = time.time() - start_train_time
    print(f"Training completed in {training_duration:.2f} seconds.")
    
    # Load the absolute best saved model weights from disk for final evaluation
    print(f"\nLoading best saved model weights from {save_path} for final evaluation split...")
    best_model = tf.keras.models.load_model(save_path, compile=False)
    best_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return best_model, history, (X_test, y_test), all_dirs, training_duration

if __name__ == "__main__":
    run_training()
