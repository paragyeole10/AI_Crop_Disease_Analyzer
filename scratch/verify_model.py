import os
import sys
import numpy as np

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.prediction.predictor import CropDiseasePredictor
from src.helpers import get_disease_details
from src.marketplace import get_recommended_products

def main():
    print("=" * 60)
    print("      AGRIVISION AI - MODEL INTEGRATION TEST       ")
    print("=" * 60)
    
    # 1. Initialize predictor
    try:
        predictor = CropDiseasePredictor()
        print(f"Predictor initialized with model path: {predictor.model_path}")
        
        # Check model exists
        if not os.path.exists(predictor.model_path):
            print(f"ERROR: Model file not found at {predictor.model_path}")
            sys.exit(1)
            
        print("Model file exists on disk. Loading model...")
        model = predictor.load_model()
        print("Model loaded successfully!")
        
        # Verify output shape is (None, 17)
        output_shape = model.output_shape
        print(f"Model output shape: {output_shape}")
        if output_shape[-1] != 17:
            print(f"ERROR: Expected 17 output classes, but model has {output_shape[-1]} outputs.")
            sys.exit(1)
        else:
            print("SUCCESS: Output shape verified!")
            
    except Exception as e:
        print(f"ERROR: Failed to initialize/load model: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    # 2. Run mock inference
    try:
        print("\nRunning mock inference on random noise image...")
        # Create a dummy image matching preprocessing specs
        dummy_img = np.random.uniform(-1.0, 1.0, (1, 224, 224, 3)).astype(np.float32)
        
        # Run predict_top_k
        top_k_results = predictor.predict_top_k(dummy_img, k=3)
        print("Inference completed successfully!")
        
        print("\nTop 3 Predictions:")
        for rank, (class_name, confidence) in enumerate(top_k_results):
            details = get_disease_details(class_name)
            print(f"{rank+1}. Class: {class_name} ({details['disease_name']})")
            print(f"   Confidence: {confidence * 100:.2f}%")
            
        # 3. Verify product recommendations
        top_class = top_k_results[0][0]
        recs = get_recommended_products(top_class)
        print(f"\nRecommended products for top prediction '{top_class}':")
        for prod in recs:
            print(f"- {prod['name']} ({prod['category']}): ${prod['price']}")
            
        print("\n" + "=" * 60)
        print("   SUCCESS: Model integration fully verified!   ")
        print("=" * 60)
        
    except Exception as e:
        print(f"ERROR during mock inference validation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
