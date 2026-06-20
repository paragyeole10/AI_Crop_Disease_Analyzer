import os
import tensorflow as tf
import numpy as np
from src.config import load_config, get_absolute_path

class CropDiseasePredictor:
    def __init__(self, model_path=None):
        if model_path is None:
            config = load_config()
            rel_path = config.get("model", {}).get("save_path", "models/mobilenet_crop_disease.keras")
            self.model_path = get_absolute_path(rel_path)
        else:
            self.model_path = model_path
            
        self.model = None
        # Class names ordered alphabetically
        self.class_names = [
            "Corn___Common_Rust",
            "Corn___Gray_Leaf_Spot",
            "Corn___Healthy",
            "Corn___Northern_Leaf_Blight",
            "Potato___Early_Blight",
            "Potato___Healthy",
            "Potato___Late_Blight",
            "Rice___Brown_Spot",
            "Rice___Healthy",
            "Rice___Leaf_Blast",
            "Rice___Neck_Blast",
            "Sugarcane___Bacterial_Blight",
            "Sugarcane___Healthy",
            "Sugarcane___Red_Rot",
            "Wheat___Brown_Rust",
            "Wheat___Healthy",
            "Wheat___Yellow_Rust"
        ]

    def load_model(self):
        """Load the TensorFlow/Keras model if not already loaded."""
        if self.model is None:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(
                    f"Model file not found at {self.model_path}. "
                    "Please run the training pipeline first to train the model."
                )
            # load_model with compile=False avoids needing to specify custom loss/optimizer configs
            self.model = tf.keras.models.load_model(self.model_path, compile=False)
        return self.model

    def predict(self, preprocessed_image):
        """
        Run inference on a preprocessed image.
        
        Parameters:
        - preprocessed_image: preprocessed image numpy array of shape (1, 224, 224, 3)
        
        Returns:
        - predicted_class: string label of predicted category
        - confidence: float score between 0.0 and 1.0
        """
        model = self.load_model()
        predictions = model.predict(preprocessed_image)
        predicted_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_idx])
        predicted_class = self.class_names[predicted_idx]
        return predicted_class, confidence

    def predict_top_k(self, preprocessed_image, k=3):
        """
        Run inference and return top K predicted classes and their confidence scores.
        
        Parameters:
        - preprocessed_image: preprocessed image numpy array of shape (1, 224, 224, 3)
        - k: number of top predictions to return
        
        Returns:
        - list of tuples (class_name, confidence) sorted by confidence descending
        """
        model = self.load_model()
        predictions = model.predict(preprocessed_image)
        # Get indices of top K predictions sorted by confidence descending
        top_k_indices = np.argsort(predictions[0])[-k:][::-1]
        results = []
        for idx in top_k_indices:
            class_name = self.class_names[idx]
            conf = float(predictions[0][idx])
            results.append((class_name, conf))
        return results
