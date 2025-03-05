"""
This is the full working model with the chatbot. The chatbot is made with the help of a pre-trained model taken
from a hugging face. The model was already trained to assist in medical cases and the response or accuracy of 
the response generated by our model is fully dependent on the accuracy of the hugging face model. Though the 
chatbot provides easygoing results, to improvise them it needs to be fine-tuned on more data to help assist
in the required task i.e. to work as per out model.

NOTE: The model taken from the hugging face is built on about 1 billion parameters thus, it takes a lot of 
time to run on any local machine. 
"""

# --- IMPORTING LIBRARIES  ---
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from typing import Any, Text, Dict, List
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftConfig, PeftModel
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import GradientBoostingClassifier

# --- PAGE CONFIGURATIONS ---
# Set page configuration
st.set_page_config(
    page_title="Mental Health Assessment",
    page_icon="💙",
    layout="wide"
)

# Add a custom background image
background_style = """
    <style>
    body {
        background-image: url("https://images.unsplash.com/photo-1506126613408-eca07ce68773");
        background-size: cover;
        background-repeat: no-repeat;
    }
    .main {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
    }
    </style>
"""
st.markdown(background_style, unsafe_allow_html=True)

# Sidebar Description
st.sidebar.title("About the App")
st.sidebar.info(
    """
    This application helps assess your mental health status based on several lifestyle 
factors. It uses **Machine Learning models** to predict if you may have 
Stress, Anxiety, or Depression.

🔹 **How It Works**  
1. Fill out the questionnaire  
2. Click **Predict My Mental Health Status**  
3. Get a recommendation based on your input  
4. Connect with our expert counselors  

🌿 *Your mental well-being matters!*
    """
)




# Load dataset and preprocess
df = pd.read_csv(r"C:\Users\Mokshda Sharma\Desktop\My Projects\mental_Health\students_mental_health_survey.csv")
df['CGPA'].fillna(df['CGPA'].mean(), inplace=True)
df['Substance_Use'].fillna(df['Substance_Use'].mode()[0], inplace=True)

numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

# Encode categorical variables
label_encoders = {}
for col in categorical_columns:
    label_encoders[col] = LabelEncoder()
    df[col] = label_encoders[col].fit_transform(df[col])

# Prepare features
X = df.drop(columns=['Stress_Level', 'Depression_Score', 'Anxiety_Score'])
y_stress = df['Stress_Level']
y_depression = df['Depression_Score']
y_anxiety = df['Anxiety_Score']

# Function to train and save voting classifier
def train_and_save_voting_model(X, y, model_name):
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create Voting Classifier
    voting_model = VotingClassifier(
        estimators=[
            ('xgb', XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric='logloss', random_state=42)),
            ('lgbm', LGBMClassifier(n_estimators=100, random_state=42)),
            ('gb', GradientBoostingClassifier(n_estimators=100, random_state=42))
        ],
        voting='soft'
    )
    
    # Fit the model
    voting_model.fit(X_train, y_train)
    
    # Save the model
    joblib.dump(voting_model, f'{model_name}_voting_model.pkl')
    
    return voting_model

# Train and save models for each target variable
stress_model = train_and_save_voting_model(X, y_stress, 'stress')
depression_model = train_and_save_voting_model(X, y_depression, 'depression')
anxiety_model = train_and_save_voting_model(X, y_anxiety, 'anxiety')

# Function for mental health prediction
def predict_mental_health(input_data):
    input_array = np.array(input_data).reshape(1, -1)

    stress_pred = stress_model.predict(input_array)[0]
    depression_pred = depression_model.predict(input_array)[0]
    anxiety_pred = anxiety_model.predict(input_array)[0]

    if stress_pred > 2:
        return "Stress"
    elif depression_pred > 3:
        return "Depression"
    elif anxiety_pred > 2:
        return "Anxiety"
    else:
        return "Healthy"
    
# Streamlit UI
st.title("💙 Mental Health Assessment App")
# User input section
st.subheader("🔍 Fill in the details below:")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("📌 Age", min_value=10, max_value=100, step=1)
    cgpa = st.number_input("📌 CGPA", min_value=0.0, max_value=4.0, step=0.1)
    financial_stress = st.number_input("💰 Financial Stress (0-10)", min_value=0, max_value=10, step=1)
    credit_load = st.number_input("📚 Semester Credit Load", min_value=1, max_value=30, step=1)
    course = st.selectbox("📖 Course", ["Medical", "Law", "Engineering", "Computer Science", "Business", "Others"])
    gender = st.selectbox("⚥ Gender",['Male', 'Female'])
    sleep_quality = st.selectbox("💤 Sleep Quality", ['Poor', 'Average', 'Good'])
    chronic_illness = st.selectbox("⚕️ Chronic Illness?", ['Yes', 'No'])
    extracurricular = st.selectbox("🎭 Extracurricular Activities?", ['Low', 'Moderate', 'High'])

with col2:
    physical_activity = st.selectbox("🏋️‍♂️ Physical Activity", ['Low', 'Moderate', 'High'])
    diet_quality = st.selectbox("🥗 Diet Quality", ['Poor', 'Average', 'Good'])
    social_support = st.selectbox("👥 Social Support", ['Low', 'Moderate', 'High'])
    relationship_status = st.selectbox("❤️ Relationship Status", ['Single', 'In a Relationship', 'Married'])
    residence_type = st.selectbox("🏠 Residence Type", ['On-Campus', 'Off-Campus', 'With Family'])
    counseling_service_use = st.selectbox("🧑‍⚕️ Used Counseling Services?", ['Never', 'Occasionally','Frequently'])
    substance_use = st.selectbox("🚬 Substance Use?", ['Never', 'Occasionally','Frequently'])
    family_history = st.selectbox("👨‍👩‍👧‍👦 Family History of Mental Illness?", ['Yes', 'No'])


# Combine all inputs into a dictionary
user_inputs = {
    "Age": age,
    "CGPA": cgpa,
    "Financial_Stress": financial_stress,
    "Semester_Credit_Load": credit_load,
    "Course": course,
    "Gender": gender,
    "Sleep_Quality": sleep_quality,
    "Physical_Activity": physical_activity,
    "Diet_Quality": diet_quality,
    "Social_Support": social_support,
    "Relationship_Status": relationship_status,
    "Substance_Use": substance_use,
    "Counseling_Service_Use": counseling_service_use,
    "Family_History": family_history,
    "Chronic_Illness": chronic_illness,
    "Extracurricular_Involvement": extracurricular,
    "Residence_Type": residence_type
}


# Encode categorical variables
encoded_values = []
for col, value in user_inputs.items():
    if col in categorical_columns:
        if value in label_encoders[col].classes_:
            encoded_values.append(label_encoders[col].transform([value])[0])
        else:
            st.error(f"Error: Unexpected value '{value}' for {col}. Please select a valid option.")
            st.stop()
    else:
        encoded_values.append(value)  # Keep numerical values as they are


# Prediction button
if st.button("Predict My Mental Health Status"):
    # Encode categorical variables
    encoded_values = []
    for col, value in user_inputs.items():
        if col in categorical_columns:
            if value in label_encoders[col].classes_:
                encoded_values.append(label_encoders[col].transform([value])[0])
            else:
                st.error(f"Error: Unexpected value '{value}' for {col}. Please select a valid option.")
                st.stop()
        else:
            encoded_values.append(value)  # Keep numerical values as they are

    # Make prediction
    prediction = predict_mental_health(encoded_values)

    # Display prediction
    st.subheader(f"📝 Your Health condition depicts you are: {prediction}")

    # Suggested treatment plan
    if prediction in ['Stress', 'Anxiety', 'Depression']:
        st.markdown("### 🌱 Suggested Treatment Plan:")
        if prediction == 'Stress':
            st.success("✔️ Practice mindfulness and meditation\n✔️ Exercise regularly\n✔️ Maintain a healthy work-life balance")
        elif prediction == 'Anxiety':
            st.warning("🔸 Engage in deep breathing techniques\n🔸 Reduce caffeine intake\n🔸 Consider professional counseling")
        elif prediction == 'Depression':
            st.error("⚠️ Seek social support\n⚠️ Engage in physical activities\n⚠️ Consult a mental health professional")

# --- CHATBOT ---
import streamlit as st
import torch
import re
import language_tool_python
from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the base and LoRA fine-tuned models
@st.cache_resource()
def load_model():
    base_model = "tiiuae/falcon-rw-1b"
    peft_model = "ShivomH/Falcon-1B-Mental-Health-v2"

    # Load the base Falcon-1B model
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Load LoRA fine-tuned model
    model = PeftModel.from_pretrained(model, peft_model)

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    tokenizer.pad_token = tokenizer.eos_token

    return tokenizer, model

tokenizer, model = load_model()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Load grammar correction tool
tool = language_tool_python.LanguageTool("en-US")

def correct_grammar(text):
    return tool.correct(text)

# --- Safety Filters ---
CRISIS_KEYWORDS = [
    "suicide", "self-harm", "overdose", "addict", "abuse", "rape", "assault", "emergency", "suicidal"
]
CRISIS_RESPONSE = (
    "\n\nIf you're in crisis, please contact a professional immediately. "
    "You can reach the National Suicide Prevention Lifeline at 988 or 112. "
    "Please reach out to a trusted friend, family member, or mental health professional. "
    "If you're in immediate danger, consider calling a crisis helpline. Your life matters, and support is available. 🙏"
)

def filter_response(response: str, user_input: str) -> str:
    response = re.sub(r'http\S+', '', response)
    response = re.sub(r'\[\w+\]|\(\w+\)|\*|\#', '', response)
    response = response.split("http")[0].split("©")[0]

    # Enforce brevity (first 2 sentences)
    sentences = re.split(r'(?<=[.!?])\s+', response)
    response = " ".join(sentences[:2])

    if any(keyword in user_input.lower() for keyword in CRISIS_KEYWORDS):
        response += CRISIS_RESPONSE

    return correct_grammar(response)

# Streamlit UI for chatbot
st.title("🧠Mental Health Chatbot")
st.write("Chat with our AI-powered assistant for mental health support.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        st.session_state.chat_history.append(("You", user_input))

        # Prepare model input
        system_instruction = (
            "You are an empathetic AI specialized in mental health support. "
            "Provide short, supportive, and comforting responses. "
            "Validate the user's emotions and offer non-judgmental support. "
        )

        chat_history = st.session_state.chat_history[-2:]
        prompt = f"{system_instruction}\n" + "\n".join(f"{role}: {text}" for role, text in chat_history) + "\nAI:"

        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_new_tokens=75,
                pad_token_id=tokenizer.eos_token_id,
                temperature=0.4,
                top_p=0.9,
                repetition_penalty=1.2,
                do_sample=True,
                no_repeat_ngram_size=2,
                early_stopping=True
            )

        response = tokenizer.decode(output[0], skip_special_tokens=True).split("AI:")[-1].strip()
        response = filter_response(response, user_input)

        st.session_state.chat_history.append(("Bot", response))

# Display chat history
st.subheader("🗨️ Chat History")
for role, text in st.session_state.chat_history:
    st.write(f"**{role}:** {text}")




# --- DISPLAY COUNSELOR DETAILS IN GRID FORMAT ---
st.subheader("🩺 Meet Our Counselors")

counselor1_img = r'C:\Users\Mokshda Sharma\Desktop\My Projects\mental_Health\download.png'
counselor2_img = r'C:\Users\Mokshda Sharma\Desktop\My Projects\mental_Health\download.png'

counselors = [
    {"name": "Dr. Sarah Johnson", "phone": "+1234567890", "email": "sarah@example.com", "image": counselor1_img},
    {"name": "Dr. James Smith", "phone": "+0987654321", "email": "james@example.com", "image": counselor2_img}
]

col1, col2 = st.columns(2)

with col1:
    st.image(counselors[0]["image"], width=150)
    st.markdown(f"**{counselors[0]['name']}**")
    st.write(f"📞 {counselors[0]['phone']}")
    st.write(f"📧 {counselors[0]['email']}")

with col2:
    st.image(counselors[1]["image"], width=150)
    st.markdown(f"**{counselors[1]['name']}**")
    st.write(f"📞 {counselors[1]['phone']}")
    st.write(f"📧 {counselors[1]['email']}")
