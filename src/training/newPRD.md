# 🌱 AgriVision AI Streamlit Upgrade PRD

## Project Title

AgriVision AI - Crop Disease Detection & Recommendation System

Version: 2.0

Status: Streamlit Enhancement Phase

---

# Objective

Upgrade the existing Streamlit application by integrating the newly trained 17-class MobileNetV2 crop disease classification model.

The upgraded system should not only detect diseases but also provide:

* Disease Information
* Symptoms
* Treatment Recommendations
* Prevention Guidelines
* Recommended Products
* Confidence Scores
* Prediction Analytics

---

# Current System

Existing Features:

* Image Upload
* Disease Detection
* Basic Prediction Output

Limitations:

* Limited disease classes
* No recommendation engine
* No disease knowledge base
* No confidence visualization
* No analytics dashboard

---

# Upgraded System Goals

Transform the application into a complete AI Agricultural Assistant.

---

# Supported Crop Diseases

## Corn

* Common Rust
* Gray Leaf Spot
* Healthy
* Northern Leaf Blight

## Potato

* Early Blight
* Healthy
* Late Blight

## Rice

* Brown Spot
* Healthy
* Leaf Blast
* Neck Blast

## Wheat

* Brown Rust
* Healthy
* Yellow Rust

## Sugarcane

* Bacterial Blight
* Healthy
* Red Rot

Total Classes: 17

---

# Functional Requirements

## FR-1 Image Upload

Users can:

* Upload image
* Drag and drop image
* Select image from device

Supported Formats:

* JPG
* JPEG
* PNG

Maximum Size:

* 10 MB

---

# FR-2 Disease Prediction

System shall:

* Load MobileNetV2 model
* Preprocess image
* Predict disease
* Calculate confidence score

Output:

```text
Disease Name

Confidence %

Prediction Time
```

---

# FR-3 Confidence Visualization

Display:

* Confidence Progress Bar
* Top Prediction
* Top 3 Predictions

Example:

```text
Rice Leaf Blast 92%

Rice Brown Spot 5%

Rice Healthy 3%
```

---

# FR-4 Disease Information Panel

Show:

* Disease Description
* Cause
* Impact

Example:

```text
Rice Leaf Blast is a fungal disease affecting rice leaves and reducing crop yield.
```

---

# FR-5 Symptoms Section

Display:

* Visual symptoms
* Disease indicators

Example:

* Brown lesions
* Yellow patches
* Leaf curling

---

# FR-6 Treatment Recommendations

Display:

* Treatment steps
* Agricultural practices

Example:

1. Remove infected leaves
2. Apply fungicide
3. Avoid excessive irrigation

---

# FR-7 Prevention Guidelines

Display:

* Preventive measures
* Best practices

Example:

* Crop rotation
* Field sanitation
* Resistant varieties

---

# FR-8 Product Recommendations

Display:

* Product Name
* Product Type
* Usage Instructions

Example:

```text
Tricyclazole

Type:
Fungicide

Usage:
Apply according to label instructions
```

---

# FR-9 Healthy Crop Handling

If healthy class detected:

Display:

```text
Healthy Crop Detected
```

Show:

* Crop health tips
* Fertilizer recommendations
* Best practices

---

# FR-10 Analytics Dashboard

Display:

* Prediction Confidence
* Disease Category
* Crop Type
* Class Distribution

Charts:

* Confidence Chart
* Probability Bar Graph

---

# Streamlit UI Structure

## Sidebar

Navigation:

```text
Home

Disease Detection

Disease Library

Model Analytics

About
```

---

# Home Page

Display:

* Project Overview
* Supported Crops
* Total Diseases Supported

Statistics:

```text
17 Disease Classes

13,324 Training Images

87% Validation Accuracy
```

---

# Disease Detection Page

Sections:

```text
Upload Image

Preview Image

Analyze Button

Prediction Result

Recommendations
```

---

# Results Page Layout

```text
Uploaded Image

Disease Prediction

Confidence Score

Disease Information

Symptoms

Treatment

Prevention

Products
```

---

# Disease Library

Searchable Database

Categories:

* Corn
* Rice
* Potato
* Wheat
* Sugarcane

Each Entry Contains:

* Description
* Symptoms
* Treatments
* Prevention

---

# Model Analytics Page

Display:

* Model Accuracy
* Dataset Information
* Confusion Matrix
* Classification Report Summary

Metrics:

```text
Validation Accuracy: 87%

Weighted F1: 0.86

Macro F1: 0.84
```

---

# Technical Requirements

## Model

File:

```text
crop_disease_model.keras
```

---

## Class Mapping

File:

```text
class_names.json
```

Contains:

17 Class Labels

---

## Disease Knowledge Base

File:

```text
disease_info.json
```

Contains:

* Description
* Symptoms
* Treatment
* Prevention
* Products

---

# Backend Architecture

```text
Streamlit
     ↓
Prediction Engine
     ↓
TensorFlow Model
     ↓
Knowledge Base
     ↓
UI Components
```

---

# Folder Structure

```text
AgriVision/

├── app.py

├── model/
│   ├── crop_disease_model.keras
│   ├── class_names.json

├── data/
│   └── disease_info.json

├── assets/
│   ├── logo.png
│   ├── icons/

├── pages/
│   ├── disease_library.py
│   ├── analytics.py

├── utils/
│   ├── predictor.py
│   ├── image_processor.py
│   ├── recommendation.py

├── requirements.txt

└── README.md
```

---

# Success Criteria

Model Accuracy:

> 85%

Prediction Time:

< 3 Seconds

Supported Diseases:

17

User Experience:

Simple and Farmer Friendly

---

# Deliverables

✅ Streamlit Web Application

✅ MobileNetV2 Integration

✅ 17 Disease Classes

✅ Disease Knowledge Base

✅ Treatment Recommendations

✅ Prevention Guidelines

✅ Product Suggestions

✅ Analytics Dashboard

✅ Responsive UI

---

# Future Upgrade Path

Phase 3:

* Multilingual Support
* Voice Support
* User Login

Phase 4:

* FastAPI Backend
* React Native Mobile App

Phase 5:

* Cloud Deployment
* Real-Time Agricultural Assistant

```
```
