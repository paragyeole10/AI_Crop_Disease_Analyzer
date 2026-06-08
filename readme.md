# 🌱 AgriVision AI - Smart Crop Disease Detection & Recommendation System

## Overview

AgriVision AI is an AI-powered crop health assistant designed to help farmers identify plant diseases from leaf images and receive actionable treatment recommendations. Using Deep Learning and Computer Vision, the system detects diseases from crop leaf images and provides disease information, symptoms, preventive measures, and recommended treatments.

The goal is to reduce crop losses, improve farming productivity, and make disease diagnosis accessible to farmers through an easy-to-use interface.

---

# Problem Statement

Crop diseases significantly impact agricultural productivity and farmer income. Traditional disease identification often requires expert consultation, which may not be accessible in rural areas.

AgriVision AI aims to:

* Detect crop diseases from leaf images.
* Provide instant diagnosis.
* Recommend suitable treatments.
* Suggest preventive measures.
* Improve decision-making for farmers.

---

# Objectives

### Primary Objectives

* Identify crop diseases using image classification.
* Provide accurate disease predictions.
* Display confidence scores.
* Recommend treatments and preventive actions.

### Secondary Objectives

* Improve accessibility to agricultural knowledge.
* Build an intuitive and farmer-friendly interface.
* Enable future integration with mobile applications and IoT systems.

---

# Dataset

### Dataset Name

PlantVillage Dataset

### Dataset Characteristics

* 50,000+ Images
* Multiple Crop Categories
* Healthy and Diseased Leaf Classes
* Publicly Available Research Dataset

### Sample Crops

* Tomato
* Potato
* Corn
* Apple
* Grape
* Pepper

---

# System Architecture

```text
Leaf Image
     ↓
Image Preprocessing
     ↓
Deep Learning Model
(MobileNetV2)
     ↓
Disease Prediction
     ↓
Knowledge Base
(JSON)
     ↓
Recommendations
     ↓
User Dashboard
```

---

# Features

## Disease Detection

Upload a crop leaf image and receive:

* Predicted Disease
* Confidence Score

Example:

Disease: Tomato Late Blight

Confidence: 96.7%

---

## Disease Information

Displays:

* Disease Description
* Causes
* Impact on Crops

---

## Symptoms Identification

Example:

* Brown Spots
* Yellowing Leaves
* Wilting
* Fungal Growth

---

## Treatment Recommendations

Example:

* Remove infected leaves
* Apply fungicide
* Avoid overhead irrigation

---

## Prevention Tips

Example:

* Use certified seeds
* Maintain proper spacing
* Improve field drainage

---

## Product Recommendations (Future Phase)

Suggested agricultural products based on detected disease.

Example:

* Copper Oxychloride
* Mancozeb
* Chlorothalonil

---

# Technology Stack

## Frontend

* Streamlit

## Backend

* Python

## Deep Learning

* TensorFlow
* Keras

## Model

* MobileNetV2 (Transfer Learning)

## Data Processing

* NumPy
* Pandas
* OpenCV

## Visualization

* Matplotlib
* Seaborn

---

# Machine Learning Pipeline

## 1. Data Collection

PlantVillage Dataset

## 2. Data Preprocessing

* Image Resizing
* Image Normalization
* Data Augmentation

## 3. Dataset Splitting

* Train Set (70%)
* Validation Set (15%)
* Test Set (15%)

## 4. Model Training

Transfer Learning using MobileNetV2

## 5. Model Evaluation

Metrics:

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix

## 6. Prediction

Real-time disease classification from uploaded images.

---

# Functional Requirements

### FR-01

User shall upload a leaf image.

### FR-02

System shall preprocess the image.

### FR-03

System shall classify the disease.

### FR-04

System shall display prediction confidence.

### FR-05

System shall provide disease information.

### FR-06

System shall recommend treatment actions.

### FR-07

System shall provide preventive measures.

---

# Non-Functional Requirements

### Performance

Prediction response time less than 3 seconds.

### Usability

Simple and intuitive interface for farmers.

### Reliability

Prediction accuracy above 90%.

### Scalability

Support future integration with cloud deployment.

---

# Future Enhancements

## Phase 2

* Product Recommendation Engine
* Disease Severity Detection
* Multilingual Support
* Voice Assistance

## Phase 3

* Mobile Application
* Weather Integration
* Fertilizer Recommendation
* Farmer Dashboard
* AI Chatbot

## Phase 4

* MLOps Pipeline
* MLflow Integration
* Docker Deployment
* AWS Cloud Hosting

---

# Expected Outcomes

* Accurate crop disease identification.
* Faster disease diagnosis.
* Reduced dependency on agricultural experts.
* Improved crop health management.
* Enhanced decision-making for farmers.

---

# Project Status

Current Phase: Phase 1 - Proof of Concept

Completed:

* Dataset Selection
* Project Planning
* System Design
* Model Selection (MobileNetV2)

In Progress:

* Data Preprocessing
* Model Training
* Streamlit UI Development

Upcoming:

* Recommendation Engine
* Product Suggestions
* Deployment

---

# Team Vision

To build an intelligent agricultural assistant that empowers farmers with AI-driven disease diagnosis, treatment recommendations, and crop management insights through a simple and accessible platform.
