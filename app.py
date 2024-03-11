# importing the required modules 

import streamlit as st

import openai

import PyPDF2
from docx import Document


from streamlit_custom_notification_box import custom_notification_box

# ||--API key integration--||

openai.api_key = "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"


# ||--Funtions--||


def generate_feedback(resume_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": resume_text},
            {"role": "system", "content": "Analyize my resume and provide good feedback on it"},
        ],
        max_tokens=4000
    )
    return response['choices'][0]['message']['content']


def read_pdf(uploaded_file):
    pdf_text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text()
    return pdf_text

def read_docx(uploaded_file):
    docx_text = ""
    doc = Document(uploaded_file)
    for paragraph in doc.paragraphs:
        docx_text += paragraph.text + "\n"
    return docx_text

# ||--application--|| 


def main():
    st.title("🎯ResuMate: AI-Powered Resume Feedback")

    st.subheader("Upload your resume")
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx'])

    st.info("💡 Use PDF for best results.")

    st.sidebar.title("🔍 About")
    st.sidebar.write("ResuMate is a cutting-edge application designed to enhance resume evaluation processes. With seamless integration of Streamlit and OpenAI's GPT-3.5-turbo model, users can effortlessly upload their resumes and receive comprehensive feedback in moments. Whether you're a seasoned Software Development Engineer or entering the field, ResuFeedback offers invaluable insights to refine your resume. Leverage the power of AI to uncover areas for improvement and polish your professional profile with precision. Say goodbye to manual review processes and embrace a more efficient and insightful approach to resume refinement with ResuFeedback.")

    if uploaded_file is not None:

        resume_text = ""
        if uploaded_file.type == "application/pdf":
            resume_text = read_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = read_docx(uploaded_file)

        if resume_text:
            st.subheader("Resume Content 📄:")
            st.write(resume_text)

            feedback = generate_feedback(resume_text)
            st.subheader("Your Feedback 🤖:")
            st.write(feedback)

if __name__ == "__main__":
    main()
