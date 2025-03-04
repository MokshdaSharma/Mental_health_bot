# Problem Statement

**Early Identification of Mental Health Disorders in Students Using Advanced Ensemble Machine Learning Techniques for Proactive Intervention.**

Mental health disorders—especially **stress, anxiety, and depression**—are increasingly prevalent among students, with studies showing that **over one-third suffer from moderate to severe symptoms**, and a significant number experience **suicidal thoughts**.  

Despite the high prevalence, **more than 60% of students do not seek support**, often due to stigma, lack of awareness, or limited access to mental health services. Left undetected, these issues can escalate, severely impacting **academic performance**, **social life**, and **long-term well-being**.

Current detection methods largely rely on self-reported questionnaires like the **PHQ-9** and **GAD-7**, which, while useful, are often **reactive** and dependent on a student's willingness to disclose symptoms.  

There is an urgent need for a **proactive, data-driven system** that can identify students at risk of mental health disorders **before these issues become critical**, thereby enabling timely intervention and support.

---

## Project Objectives

- Predict whether a student is at risk of a mental health disorder.
- Estimate levels of **stress**, **anxiety**, and **depression** on a scale of **1 to 5**.
- Build a **robust**, **scalable**, and **accurate model** using **ensemble learning techniques**.
- Take user inputs on **lifestyle**, **academic**, and **social factors** for **live predictions**.

  # 📊 Dataset Description

This project utilizes the [Students Mental Health Assessments Dataset](https://www.kaggle.com/datasets/sonia22222/students-mental-health-assessments) from Kaggle, which contains data collected from **7,022 university students** aimed at understanding the key factors contributing to mental health issues such as **stress**, **anxiety**, and **depression**.

The dataset provides comprehensive information on **academic performance**, **lifestyle habits**, **social relationships**, and **mental health symptoms**, enabling the development of predictive models for early identification of mental health disorders.

## Dataset Overview

| Feature Name                   | Description                                     | Data Type | Example Values             |
|---------------------------------|-------------------------------------------------|-----------|-----------------------------|
| Age                            | Age of the student (18-35 years)               | Integer   | 18, 22, 25                |
| Course                         | Field of study                                 | Object    | Engineering, Business      |
| Gender                         | Gender identity                                | Object    | Male, Female               |
| CGPA                           | Cumulative Grade Point Average (2.44 - 4.0)   | Float     | 3.56, 3.74                |
| Stress_Level                   | Stress intensity (scale 0-5)                  | Integer   | 2, 3, 4                   |
| Depression_Score               | Depression severity (scale 0-5)               | Integer   | 1, 3, 4                   |
| Anxiety_Score                  | Anxiety severity (scale 0-5)                  | Integer   | 0, 2, 4                   |
| Sleep_Quality                  | Sleep health status                           | Object    | Good, Average              |
| Physical_Activity              | Physical activity level                       | Object    | Low, Moderate              |
| Diet_Quality                   | Nutrition quality                             | Object    | Good, Average              |
| Social_Support                 | Level of social support                       | Object    | Low, Moderate, High        |
| Relationship_Status            | Current relationship status                   | Object    | Single, Married            |
| Substance_Use                  | Use of substances (alcohol, drugs)            | Object    | Never, Occasionally        |
| Counseling_Service_Use         | Access to counseling services                 | Object    | Never, Occasionally        |
| Family_History                 | Family mental health history                  | Object    | Yes, No                    |
| Chronic_Illness                | Presence of chronic illnesses                 | Object    | Yes, No                    |
| Financial_Stress               | Financial pressure level (scale 0-5)          | Integer   | 2, 3, 4                   |
| Extracurricular_Involvement    | Participation in extracurricular activities   | Object    | Low, Moderate, High        |
| Semester_Credit_Load           | Total credit load per semester (15-29)        | Integer   | 18, 22, 27                |
| Residence_Type                 | Living arrangement                            | Object    | On-Campus, Off-Campus      |

## Key Statistics

| Metric               | Value                    |
|----------------------|--------------------------|
| **Total Records**   | 7,022                    |
| **Total Features**  | 20                       |
| **Age Range**       | 18 – 35 years            |
| **CGPA Range**      | 2.44 – 4.00              |
| **Stress Levels**   | 0 (Low) – 5 (High)       |
| **Depression Score**| 0 (Low) – 5 (High)       |
| **Anxiety Score**   | 0 (Low) – 5 (High)       |
| **Financial Stress**| 0 (None) – 5 (Extreme)   |

This dataset enables:
- **Early detection** of mental health risks in students.
- Identification of key stressors including **academic pressure**, **social challenges**, and **health factors**.
- Development of a **machine learning-powered system** for proactive mental health support.
- Supports targeted interventions by educational institutions.

## ⚡ Preprocessing Steps Applied

- Handling missing values (`CGPA`, `Substance_Use`)
- Label encoding for categorical features
- Feature scaling for numeric attributes
- Oversampling with **SMOTE** to handle imbalance
- Feature engineering (lifestyle scores, academic stress index)

> 🔗 **Dataset Source:** [Students Mental Health Assessments](https://www.kaggle.com/datasets/sonia22222/students-mental-health-assessments)

## ⚙️ Solution Approach  

### 🔹 Data Preprocessing  
- Handling missing values  
- Encoding categorical variables  
- Scaling numerical features using **StandardScaler**  
- Balancing the dataset using **SMOTE** to address class imbalance  

### 🔹 Model Building  
We evaluated and compared multiple models:  
- **XGBoost** — *94.67% accuracy*  
- **LightGBM** — *95.24% accuracy*  
- **MLP Classifier** — *93.71% accuracy*  
- **Gradient Boosting** — *94.54% accuracy*  
- **Stacking Ensemble (XGBoost, LightGBM, Gradient Boosting, MLP)** — *95.49% accuracy*  
- **Voting Classifier (XGBoost, LightGBM, Gradient Boosting)** — **⭐ 95.75% accuracy (Best)**


### 🔹 Model Evaluation  
- Performance measured using **Accuracy**, **Classification Report**, and **Confusion Matrix**.  
- The **Voting Classifier** on **XGBoost, LightGBM, and Gradient Boosting** achieved the **highest accuracy of 95.75%**, outperforming all other models, including the **Deep Learning Hybrid Model (MLP)**.

---

## 🌟 Unique Selling Points (USP)  

**Exceptional Accuracy:** Achieved **95.75%** with ensemble learning.  
**Proactive Mental Health Detection:** Early identification of mental health risks.  
**Real-Time Predictions:** User-friendly system for instant results.  
**Personalized Mental Health Insights:** Understanding emotional trends and stress triggers.  
**Tailored Recommendations:** Including self-care tips, counseling services, and professional support.  
**AI-Powered Chat Support:** Interactive guidance and mental health resources.  
**Scalability:** Ready to integrate into educational platforms for widespread use.  

---

## Results  

| Model                          | Accuracy (%) |
|---------------------------------|--------------|
| XGBoost                        | 94.67        |
| LightGBM                       | 95.24        |
| MLP Classifier (Deep Learning) | 93.71        |
| Gradient Boosting              | 94.54        |
| Stacking Ensemble              | 95.49        |
| **Voting Classifier**          | **95.75**    |

---

## 🏆 Outcome  

This system allows educational institutions to:  
 Detect mental health concerns early.  
 Offer proactive, personalized mental health support.  
 Minimize severe mental health crises.  
 Enhance students’ academic performance through emotional well-being.

---

