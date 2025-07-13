from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="OptiResume - ATS Resume Expert", page_icon=":guardsman:", layout="wide")
st.header("OptiResume - ATS Resume Expert")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

# Add custom CSS for better button styling
st.markdown("""
<style>
.stButton > button {
    width: 100%;
    margin: 2px;
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.3s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Create three columns with buttons placed close together
col1, col2, col3, col4 = st.columns([2, 2, 2, 3])

with col1:
    submit1 = st.button("Tell Me About the Resume")

with col2:
    submit2 = st.button("How to Improve My Skills?")

with col3:
    submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an expert Career Development Coach and Resume Optimization Specialist with extensive experience in talent acquisition and skill development. 
Your task is to analyze the provided resume against the job description and provide comprehensive, actionable advice for career improvement.

Please provide:
1. **Skill Gap Analysis**: Identify specific technical and soft skills missing from the resume that are required for the target role
2. **Learning Roadmap**: Suggest a structured learning path with specific courses, certifications, or resources to bridge these gaps
3. **Experience Enhancement**: Recommend ways to gain relevant experience (projects, internships, volunteer work, side projects)
4. **Resume Optimization**: Provide specific suggestions to better highlight existing skills and experiences
5. **Industry Trends**: Mention current market trends and emerging skills in this field that would be valuable to learn
6. **Timeline & Prioritization**: Suggest a realistic timeline for skill development and prioritize which skills to focus on first
7. **Networking & Professional Development**: Recommend professional communities, events, or networking opportunities relevant to this role

Format your response in a clear, structured manner with actionable steps the candidate can take immediately to improve their profile and increase their chances of landing the desired role.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("📋 Resume Analysis")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("🚀 Skill Development Roadmap")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("📊 ATS Match Analysis")
        st.write(response)
    else:
        st.write("Please upload the resume")