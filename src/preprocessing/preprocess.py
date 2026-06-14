import numpy as np
import cv2
from PIL import Image

def preprocess_image(image_source, target_size=(224, 224)):
    """
    Load and preprocess an image for MobileNetV2.
    
    Parameters:
    - image_source: Can be a file path, a PIL Image, or a file-like bytes object.
    - target_size: Tuple (width, height) for resizing.
    
    Returns:
    - Preprocessed image as a numpy array with shape (1, 224, 224, 3) normalized to [-1, 1].
    """
    if isinstance(image_source, str):
        # File path
        img = cv2.imread(image_source)
        if img is None:
            raise ValueError(f"Image at {image_source} could not be loaded.")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif isinstance(image_source, Image.Image):
        # PIL Image
        img = np.array(image_source.convert('RGB'))
    elif hasattr(image_source, 'read'):
        # File-like object (e.g. BytesIO from Streamlit uploader)
        try:
            image_source.seek(0)
        except Exception:
            pass
        file_bytes = np.asarray(bytearray(image_source.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Failed to decode uploaded image.")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            image_source.seek(0)
        except Exception:
            pass
    else:
        # Assume numpy array (RGB)
        img = np.asarray(image_source)

    # Resize image
    img_resized = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
    
    # Normalize to [-1, 1] (standard MobileNetV2 scaling: (pixel_val / 127.5) - 1.0)
    img_normalized = (img_resized.astype(np.float32) / 127.5) - 1.0
    
    # Add batch dimension: (1, 224, 224, 3)
    img_batch = np.expand_dims(img_normalized, axis=0)
    
    return img_batch
