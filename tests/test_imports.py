from src.config import load_config
from src.preprocessing.preprocess import preprocess_image
from src.prediction.predictor import CropDiseasePredictor
from src.helpers import load_knowledge_base
from src.marketplace import get_recommended_products

def test_imports():
    config = load_config()
    assert config is not None
    print("All imports validated successfully!")

if __name__ == "__main__":
    test_imports()
