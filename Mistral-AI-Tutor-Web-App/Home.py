import streamlit as st
from utils.st_utils import extract_text_from_pdfs,display_enhanced_summary
from utils.openai_utils import generate_summary
import json

st.set_page_config(page_title="AI Study Buddy", layout="wide")

# Initialize session state for API key from settings
if "settings" in st.session_state and "api_keys" in st.session_state.settings:
    st.session_state.openai_api_key = st.session_state.settings["api_keys"]["openai"]

# Sidebar
with st.sidebar:
    st.info("Select a page from the sidebar to master your study material!")
    
    if not st.session_state.get("openai_api_key"):
        st.warning("Please set up your OpenAI API key in the Settings page to use the application.")

# Create a layout with the title and logo closer together, centered
col1, col2, col3 = st.columns([2, 6, 1])  # Adjust the column widths for alignment

with col1:
    st.write("")  # Empty column for spacing

with col2:
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: center;">
            <h1 style="font-family: 'Roboto', sans-serif; color: #2c3e50; font-size: 36px; margin: 0; display: inline-block;">
                📚 Your AI-Powered Personal Tutor
            </h1>            
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.write("")  # Empty column for spacing


st.markdown("""
    <style>
        .centered-box {
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin: 20px auto;
            max-width: 800px;
        }
        .btn-container {
            margin-top: 30px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }
        .btn {
            color: white; /* White text for contrast */
            padding: 15px 30px; /* Larger padding for better clickability */
            border-radius: 25px; /* Rounded corners for a modern look */
            font-size: 16px; /* Increase font size for readability */
            font-weight: bold;
            text-decoration: none;
            text-align: center;
            transition: all 0.3s ease; /* Smooth hover effect */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
            margin: 10px; /* Spacing between buttons */
            border: none; /* Remove border */
        }
        .btn:hover {
            background-color: #16a085; /* Slightly darker teal on hover */
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15); /* Deeper shadow on hover */
            transform: translateY(-2px); /* Hover "lift" effect */
        }
        .upload-box {
            text-align: center;
            margin-bottom: 20px;
        }
        .feature-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .feature-description {
            font-size: 16px;
            color: #666;
        }
    </style>
""", unsafe_allow_html=True)

# Introductory section
st.markdown("""
    <div class="centered-box">
        <h2>Step 1: Upload Your Study Material</h2>
        <p>Upload one or more PDFs to generate instant summaries, study plans, and quizzes tailored just for you!</p>
    </div>
""", unsafe_allow_html=True)

# File uploader
uploaded_files = st.file_uploader("Upload one or more PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    # Spinning loader for processing
    with st.spinner("Hang tight! We're summarizing your documents..."):

        documents = extract_text_from_pdfs(uploaded_files)

        # Generate summaries
        summaries = {}
        for doc in documents:
            summaries[doc["name"]] = generate_summary(doc["content"])

        # Save summaries in session state
        st.session_state["summaries"] = summaries
        st.session_state["documents"] = documents

    # Display summaries using columns
    st.markdown("<h3 style='text-align: center;'>Document Summaries</h3>", unsafe_allow_html=True)
    cols = st.columns(len(summaries))  # Create as many columns as there are summaries
    for i, (name, summary) in enumerate(summaries.items()):
        with cols[i]:  # Place each summary in its respective column
            st.markdown(f"Document Name: **{name}**")
            display_enhanced_summary(summary)

    # Success message
    st.success("Documents processed successfully! Use the sidebar to explore quiz generation, coding questions, and flashcards.")

# Main navigation
st.markdown("""
    <div class="centered-box">
        <div class='feature-title'>🔍 Ask Questions</div>
        <div class='feature-description'>Get instant answers to your questions about the study material.</div>
    </div>
    
    <div class='centered-box'>
        <div class='feature-title'>📝 Generate Quizzes</div>
        <div class='feature-description'>Create custom quizzes to test your knowledge.</div>
    </div>
    
    <div class='centered-box'>
        <div class='feature-title'>💻 Practice Coding</div>
        <div class='feature-description'>Get hands-on with coding exercises based on your materials.</div>
    </div>

    <div class='centered-box'>
        <div class='feature-title'>📄 OCR & Image Analysis</div>
        <div class='feature-description'>Extract text from images and ask questions about them.</div>
    </div>
""", unsafe_allow_html=True)
