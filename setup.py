from setuptools import setup, find_packages

setup(
    name="agrivision_ai",
    version="1.0.0",
    description="AgriVision AI Core ML and Preprocessing Library",
    packages=find_packages(),
    install_requires=[
        "tensorflow",
        "numpy",
        "opencv-python-headless",
        "pillow",
        "scikit-learn",
        "matplotlib"
    ]
)
