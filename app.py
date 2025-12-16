# app.py
import streamlit as st
import requests

st.title("Campus Oracle - Your AI College Assistant")

# Get RapidAPI key from secrets or user input
RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY") or st.text_input(
    "Enter your RapidAPI Key", type="password"
)

# Upload college materials
uploaded_files = st.file_uploader(
    "Upload syllabi / notes (PDF or text)", 
    accept_multiple_files=True
)

# Question input
question = st.text_input(
    "Ask anything about your college:",
    value="Create a clear, step-by-step study roadmap from this PDF for my college."
)

st.write("App is running")

def extract_text_from_files(files):
    texts = []
    for f in files:
        try:
            content = f.read().decode("utf-8")
            texts.append(content)
        except:
            texts.append(f"Could not read {f.name}, placeholder used.")
    return "\n".join(texts) if texts else "No content extracted"

def generate_ai_response_rapidapi(college_name, question, context):
    """
    Generate AI response using RapidAPI Hugging Face endpoint.
    """
    if not RAPIDAPI_KEY:
        return "RapidAPI key not provided."

    url = "https://hf.space/embed/tiiuae/falcon-7b-instruct/api/predict/"

    payload = {
        "data": [
            f"You are an expert AI assistant for {college_name}.\n"
            f"Context: {context}\n"
            f"Question: {question}\n"
            "Provide a clear, step-by-step study roadmap or answer."
        ]
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "hf.space"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        result = response.json()
        # Hugging Face API returns predictions as a list
        return result.get("data", ["No response"])[0]
    except Exception as e:
        return f"Error generating AI response: {e}"

if st.button("Generate AI Answer"):
    context = extract_text_from_files(uploaded_files) if uploaded_files else "No files uploaded, answer will be general."

    with st.spinner("Thinking..."):
        answer = generate_ai_response_rapidapi("MyCollege", question, context)

    st.success("Response generated")
    st.write(answer)
