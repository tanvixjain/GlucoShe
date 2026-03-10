# GlucoShe
AI-Powered Diabetes Risk Awareness for Women

Gluco-She is a women-centric machine learning application designed to provide early diabetes risk awareness, particularly for pregnant women and individuals affected by PCOS (Polycystic Ovary Syndrome). The project focuses on preventive insights rather than diagnosis, helping users understand risk patterns and lifestyle factors using interpretable AI.

🩺 Problem Statement

Diabetes screening methods often overlook:

Early pregnancy risk indicators
Hormonal conditions like PCOS
Non-linear interactions between lifestyle and metabolic factors As a result, many women are diagnosed late, missing opportunities for early lifestyle intervention.
💡 Solution Overview

Gluco-She applies machine learning models to analyze health indicators such as glucose, BMI, age, pregnancy stage, and hormonal symptoms to:
Predict diabetes risk probability
Highlight key contributing factors
Provide trimester-safe, personalized lifestyle insights The system is designed to be interpretable, accessible, and women-focused.
📊 Dataset

Base Dataset: Pima Indians Diabetes Dataset
Source: Kaggle / OpenML
Extension: Pregnancy- and PCOS-related features were added to better represent real-world women’s health scenarios.
Key Features:

Glucose
BMI
Age
Pregnancies
Insulin
Blood Pressure
Diabetes Pedigree Function
Trimester
Weight Gain Pattern
Physical Activity Level
Menstrual Regularity
Hormonal Symptoms
Target Variable:

Outcome (0 = Non-Diabetic, 1 = Diabetic)

⚙️ Methodology

Data Preprocessing
Handled missing and zero-value medical indicators

Encoded categorical pregnancy and hormonal features

Normalized numerical attributes

Exploratory Data Analysis (EDA)
Distribution analysis (Glucose, BMI, Age)

Class imbalance analysis

Correlation and feature behavior visualization

Model Development
The following models were trained and compared:

Logistic Regression

Decision Tree

Support Vector Machine (SVM)

Random Forest (Final Model)

Model Evaluation
Accuracy

Precision, Recall, F1-Score

ROC-AUC Curve

Confusion Matrix

🏆 Why Random Forest?

Random Forest was selected as the final model because it:

Handles non-linear relationships effectively
Reduces overfitting through ensemble learning
Provides feature importance, enabling explainable predictions
Performs consistently across diverse edge cases (early pregnancy, PCOS, borderline glucose levels)
📈 Key Insights

Glucose and BMI are the strongest predictors of diabetes risk
Pregnancy stage and weight gain patterns influence late-stage risk
Hormonal and menstrual irregularities contribute to hidden risk profiles
Ensemble learning improves generalization in healthcare data
🌿 Application Features (Concept)

Minimal-question risk assessment
Risk score visualization (Low / Moderate / High)
Feature contribution explanation
Pregnancy- and PCOS-specific lifestyle guidance
“What-if” risk simulation for preventive awareness
⚠️ This application is intended for awareness and educational purposes only and does not replace medical advice.

🛠️ Tech Stack

Language: Python
Libraries: NumPy, Pandas, Scikit-learn
Visualization: Matplotlib, Seaborn
Backend (Planned): Flask / FastAPI
Frontend (Planned): React / Streamlit
📌 Project Status

🚧 In Progress

Model refinement
UI integration
Deployment planning
🌍 Impact Gluco-She aims to contribute to women’s health equity by:

Promoting early awareness
Supporting preventive healthcare
Making AI systems more inclusive of women-specific health data
📚 References

Pima Indians Diabetes Dataset (Kaggle, OpenML)
Machine Learning Prediction Models for Gestational Diabetes (PMC, PubMed)
Studies on PCOS and impaired glucose tolerance
