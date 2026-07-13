# AgriVision AI: A Deep Learning-Based Crop Health Intelligence System for Automated Leaf Disease Detection and Actionable Treatment Recommendations

**AgriVision AI Development Team**  
*Department of Agricultural Engineering and Artificial Intelligence*  
*AgriVision Research Initiative*  

**Deployed Live Application**: [https://aicropdiseaseanalyzer-igmdshjcgch6hpexkxxwkz.streamlit.app/](https://aicropdiseaseanalyzer-igmdshjcgch6hpexkxxwkz.streamlit.app/)

---

### **Abstract**
> *Crop diseases represent a significant threat to global agricultural productivity, food security, and smallholder farmer livelihoods. Traditional diagnosis methods rely heavily on visual inspections by experts, which are often slow, costly, and inaccessible in remote regions. In this paper, we present **AgriVision AI**, a production-grade, end-to-end framework that leverages Deep Learning (specifically, a fine-tuned MobileNetV2 architecture) to perform real-time identification of 17 distinct crop conditions across 5 primary crop species (Corn, Potato, Rice, Sugarcane, and Wheat). The system is coupled with a multilingual Knowledge Base (supporting English, Hindi, Marathi, and Spanish) to deliver instant, localized diagnostic reports, symptoms catalogs, and recommended treatment workflows (both chemical and organic). Operating through an optimized Streamlit interface integrated with a Text-to-Speech (TTS) auditory service, AgriVision AI achieves a classification test accuracy of **87.35%** and a weighted F1-score of **86.54%** in sub-second inference speeds. Our results demonstrate that transfer learning-based computer vision frameworks can be deployed in lightweight web architectures to provide accessible, expert-level agricultural guidance.*

---

## I. Introduction
The agricultural sector is under constant pressure from climate change, soil degradation, and phytopathogens. Plant diseases are responsible for crop yield losses ranging between 20% and 40% annually, severely impacting global food supplies. Early detection and localized intervention are critical to mitigating these losses. However, the scarcity of agricultural extension officers in developing countries leaves many farmers without timely or accurate diagnostic advice.

To address this challenge, we introduce **AgriVision AI**, an agricultural intelligence system designed to democratize disease diagnosis. By utilizing deep convolutional neural networks (CNNs), the system processes uploaded leaf images, detects specific anomalies, and outputs actionable chemical and organic solutions, bridging the gap between expert knowledge and local farmers.

---

## II. Problem Statement
The central problem addressed by this system is the **inaccessibility of rapid, accurate, and localized crop disease diagnosis**. 

Key challenges include:
1. **Diagnostic Delay**: Conventional lab tests or expert visits take days or weeks, allowing pathogens to spread unchecked.
2. **Lack of Localized Recommendations**: Many generic computer vision models stop at classification (e.g., "Tomato Late Blight"), without providing actionable chemical or organic remedy steps.
3. **Language Barriers**: Smallholder farmers often speak regional languages (such as Hindi or Marathi), rendering English-centric applications useless.
4. **Infrastructure Constraints**: Rural areas require lightweight applications capable of running on low-resource computing nodes or standard mobile browsers with minimal network overhead.

---

## III. System Architecture and Methodology
The system architecture of AgriVision AI consists of three core pipeline layers: Data Preprocessing, Deep Learning Inference, and the Recommendation/UI Engine.

```text
       [ Crop Leaf Image ] 
                │
                ▼
   ┌───────────────────────────┐
   │    Image Preprocessing    │  <-- Resizing (224x224), Normalization (/255)
   └────────────┬──────────────┘
                │
                ▼
   ┌───────────────────────────┐
   │    MobileNetV2 Model      │  <-- Fine-tuned Transfer Learning
   └────────────┬──────────────┘
                │
                ▼
   ┌───────────────────────────┐
   │    Disease Classifier     │  <-- 17 Classes (Softmax Probabilities)
   └────────────┬──────────────┘
                │
                ▼
   ┌───────────────────────────┐
   │      Knowledge Base       │  <-- Multilingual JSON (EN, HI, MR, ES)
   └────────────┬──────────────┘
                │
                ▼
   ┌───────────────────────────┐
   │   User Interface (UI)     │  <-- Streamlit App & Audio Narrative (TTS)
   └───────────────────────────┘
```

### A. Dataset & Preprocessing
The model is trained on subsets of the public **PlantVillage** dataset, focusing on 17 specific healthy and diseased classes across Corn, Potato, Rice, Sugarcane, and Wheat. 
Images are preprocessed by:
- Resizing to $224 \times 224 \times 3$ pixels to fit the input shape.
- Scaling pixel values to the range $[0, 1]$ via normalization ($x_{\text{norm}} = x / 255.0$).
- Applying data augmentation (random flips, rotations, and zooms) during training to mitigate overfitting.

### B. Convolutional Neural Network (CNN) Model
We employ **MobileNetV2** as our base feature extractor. MobileNetV2 is selected for its highly efficient inverted residual blocks and depthwise separable convolutions, making it ideal for deployment on mobile networks and cloud platforms. 
The base network is initialized with **ImageNet** weights, and the classification head is fine-tuned:
$$\text{Output} = \text{Softmax}(\text{Dense}(\text{Dropout}(\text{GlobalAveragePooling}(\mathbf{X})))$$

### C. Multilingual Knowledge Base
To translate model predictions into actionable advice, we construct a multilingual knowledge base mapping classification tokens to detailed diagnosis profiles. The knowledge base contains translations in English (`en`), Hindi (`hi`), Marathi (`mr`), and Spanish (`es`), returning:
- **Disease Description**: Pathogen details and crop impact.
- **Visual Symptoms**: What signs the farmer should search for on the leaf.
- **Treatment Protocols**: Step-by-step chemical and organic recommendations.
- **Prevention Strategies**: Cultural and sanitary guidelines to protect future crop cycles.

---

## IV. Experimental Results and Evaluation
The system was trained for 15 epochs with a batch size of 32 using the Adam optimizer (learning rate $\eta = 0.001$). 

### A. Performance Metrics
Evaluation on the test partition yielded the following performance metrics:

| Metric | Score / Value |
| :--- | :--- |
| **Test Accuracy** | 87.35% |
| **Weighted Precision** | 86.82% |
| **Weighted Recall** | 87.35% |
| **F1-Score** | 86.54% |
| **Test Loss** | 0.3842 |
| **Training Time** | 342.12 Seconds (on GPU node) |

### B. Supported Crop Categories & Classes
The classifier distinguishes between 17 crop-disease pairings:
1. **Corn**: Common Rust, Gray Leaf Spot, Northern Leaf Blight, Healthy
2. **Potato**: Early Blight, Late Blight, Healthy
3. **Rice**: Brown Spot, Leaf Blast, Neck Blast, Healthy
4. **Sugarcane**: Bacterial Blight, Red Rot, Healthy
5. **Wheat**: Brown Rust, Yellow Rust, Healthy

---

## V. Project Structure and Layout
The repository is structured to separate concern between core machine learning models, database catalogs, and user interface components:

```text
Plant_Disease_analyzer/
├── .streamlit/
│   └── config.toml             # Custom theme settings and server parameters
├── assets/
│   ├── images/                 # Model evaluation charts (confusion matrix, history)
│   ├── products/               # Recommended agricultural product images
│   ├── logo.png                # Sidebar application logo
│   └── model_metrics.json      # Compiled training parameters and performance scores
├── app/
│   ├── __init__.py
│   ├── components/
│   │   └── layout.py           # Core page layout, styling (CSS), and sidebar branding
│   └── pages/                  # Streamlit Multi-Page scripts
│       ├── 0_🏠_Home.py        # Welcome dashboard and features introduction
│       ├── 1_🔬_Scan_Leaf.py   # AI Scanner interface and TTS auditory output
│       ├── 2_📚_Disease_Library.py # Multilingual agricultural catalog explorer
│       ├── 3_🛒_Marketplace.py  # Localized agricultural shop and order tracking
│       └── 4_📊_Model_Analytics.py # Model performance metrics visualizer
├── src/
│   ├── __init__.py
│   ├── config.py               # Path resolution and YAML loader
│   ├── translations.py         # Multi-language translation maps
│   ├── tts_service.py          # Google TTS audio generation service
│   ├── helpers.py              # Knowledge base loading utilities
│   ├── marketplace.py          # E-commerce products and mapping logic
│   ├── prediction/
│   │   └── predictor.py        # Keras model inference implementation
│   └── preprocessing/
│       └── preprocess.py       # Image resizing and normalization pipeline
├── knowledge_base/             # Multilingual disease description JSON databases
│   ├── disease_info.json       # English profiles
│   ├── disease_info_es.json    # Spanish profiles
│   ├── disease_info_hi.json    # Hindi profiles
│   └── disease_info_mr.json    # Marathi profiles
├── models/
│   └── mobilenet_crop_disease.keras # Trained Keras neural network weights
├── tests/
│   ├── test_imports.py         # Import sanity checker
│   └── test_tts.py             # TTS functional verification test script
├── config.yaml                 # Central project configuration parameters
├── app.py                      # Main entrypoint script for Streamlit
├── requirements.txt            # Software dependencies list
└── setup.py                    # Package setup script
```

---

## VI. Setup & Deployment Instructions

### A. Environment Configuration
Install the required dependencies listed in the requirements file:
```bash
pip install -r requirements.txt
```

### B. Running the Application Locally
Launch the Streamlit server from the root directory:
```bash
python -m streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### C. Running Verification Tests
Execute the test suite to verify module imports and TTS operation:
```bash
python tests/test_imports.py
python tests/test_tts.py
```

---

## VII. Conclusion & Future Work
This paper presented AgriVision AI, a complete deep learning framework that detects crop leaf diseases and supplies actionable treatments. By placing a lightweight MobileNetV2 model inside an intuitive Streamlit interface, we successfully deliver low-latency diagnoses. In future phases, we will explore:
* **Severity Detection**: Calculating the exact percentage of leaf infection area.
* **AgriVision Chatbot**: An LLM-powered interactive advisor.
* **Offline Deployment**: Compiling the model via TensorFlow Lite for edge deployment in low-connectivity areas.

---

## References
1. **Hughes, D., & Salathé, M. (2015).** *An open access image database of plant diseases on crowdsourced photos.* arXiv preprint arXiv:1511.08060. (PlantVillage Dataset).
2. **Sandler, M., Howard, A., Zhu, M., Zhmoginov, A., & Chen, L. C. (2018).** *MobileNetV2: Inverted residuals and linear bottlenecks.* Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 4510-4520.
3. **Streamlit Inc.** *Streamlit Documentation for Multi-page Application Development.* Available: https://docs.streamlit.io.
4. **Google LLC.** *gTTS: Python library and CLI tool to interface with Google Translate's text-to-speech API.* Available: https://pypi.org/project/gTTS/.
