import os
import tensorflow as tf
import numpy as np

class CropDiseasePredictor:
    def __init__(self, model_path=None):
        if model_path is None:
            # Default location
            self.model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "crop_disease_model.h5")
        else:
            self.model_path = model_path
            
        self.model = None
        # Class names ordered alphabetically as loaded by tf.keras.utils.image_dataset_from_directory
        self.class_names = [
            'Pepper__bell___Bacterial_spot',
            'Pepper__bell___healthy',
            'Potato___Early_blight',
            'Potato___Late_blight',
            'Potato___healthy',
            'Tomato_Bacterial_spot',
            'Tomato_Early_blight',
            'Tomato_Late_blight',
            'Tomato_Leaf_Mold',
            'Tomato_Septoria_leaf_spot',
            'Tomato_Spider_mites_Two_spotted_spider_mite',
            'Tomato__Target_Spot',
            'Tomato__Tomato_YellowLeaf__Curl_Virus',
            'Tomato__Tomato_mosaic_virus',
            'Tomato_healthy'
        ]

    def load_model(self):
        """Load the TensorFlow/Keras model if not already loaded."""
        if self.model is None:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(
                    f"Model file not found at {self.model_path}. "
                    "Please run train.py first to train the model."
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
