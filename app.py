import streamlit as st
import http.client
import json

st.title("Campus Oracle - Your AI College Assistant")

# Get RapidAPI Key safely
RAPIDAPI_KEY = st.text_input("Enter your RapidAPI Key", type="password")

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
            texts.append(f.read().decode("utf-8"))
        except:
            texts.append(f"Could not read {f.name}, placeholder used.")
    return "\n".join(texts) if texts else "No content extracted"

def generate_ai_response_rapidapi(question, context):
    if not RAPIDAPI_KEY:
        return "Please provide a RapidAPI key."

    conn = http.client.HTTPSConnection("copilot5.p.rapidapi.com")

    payload = json.dumps({
        "message": f"Context: {context}\nQuestion: {question}",
        "conversation_id": None,
        "mode": "CHAT",
        "markdown": True
    })

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "copilot5.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    try:
        conn.request("POST", "/copilot", payload, headers)
        res = conn.getresponse()
        data = res.read()
        response_json = json.loads(data)
        return response_json.get("message", "No response from API")
    except Exception as e:
        return f"Error generating AI response: {e}"

if st.button("Generate AI Answer"):
    context = extract_text_from_files(uploaded_files) if uploaded_files else "No files uploaded, answer will be general."
    with st.spinner("Thinking..."):
        answer = generate_ai_response_rapidapi(question, context)
    st.success("Response generated")
    st.write(answer)
