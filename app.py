# app.py
import streamlit as st
import openai

st.title("Campus Oracle - Your AI College Assistant")

# Get OpenAI API key safely from Streamlit secrets or prompt
openai.api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("Enter your OpenAI API Key", type="password")


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
    """
    Extract text from uploaded files.
    Reads UTF-8 text or returns a placeholder if unreadable.
    """
    texts = []
    for f in files:
        try:
            content = f.read().decode("utf-8")
            texts.append(content)
        except:
            texts.append(f"Could not read {f.name}, placeholder used.")
    return "\n".join(texts) if texts else "No content extracted"

def generate_ai_response(college_name, question, context):
    """
    Generate AI response using OpenAI ChatCompletion API (>=1.0.0).
    """
    prompt = f"""
You are an expert AI assistant for {college_name}.
Here is context from uploaded materials:
{context}

Question: {question}

Please provide a clear, step-by-step study roadmap or answer.
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        # Access the content properly
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error generating AI response: {e}"

if st.button("Generate AI Answer"):
    context = extract_text_from_files(uploaded_files) if uploaded_files else "No files uploaded, answer will be general."
    
    with st.spinner("Thinking..."):
        answer = generate_ai_response("MyCollege", question, context)

    st.success("Response generated")
    st.write(answer)
