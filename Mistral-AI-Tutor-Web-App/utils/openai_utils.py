from openai import OpenAI
import json
import os
import streamlit as st

def get_openai_client():
    if not st.session_state.get("openai_api_key"):
        st.error("Please enter your OpenAI API key in the sidebar.")
        st.stop()
    return OpenAI(api_key=st.session_state.openai_api_key)

# Generate Summary
@st.cache_data
def generate_summary(content):
    client = get_openai_client()
    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional summarization assistant. Your task is to provide a structured summary for the given document "
                "and output it in JSON format with specific keys."
            )
        },
        {
            "role": "user",
            "content": f"Please analyze this content and provide a summary in JSON format with the following keys:\n"
                      f"- `summary`: A concise summary (150-200 words)\n"
                      f"- `key_skills`: List of key skills required\n"
                      f"- `difficulty`: Estimated difficulty (Easy, Medium, or Hard)\n"
                      f"- `estimated_time`: Estimated time in minutes to comprehend\n\n"
                      f"Content to analyze:\n{content}"
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

def generate_quiz(content, num_questions=10, difficulty="Medium", include_explanations=False):
    client = get_openai_client()
    messages = [
        {
            "role": "system",
            "content": "You are an expert quiz generator. Create multiple-choice questions based on the provided content."
        },
        {
            "role": "user",
            "content": f"""Generate {num_questions} {difficulty.lower()}-level multiple-choice questions based on this content:

Content: {content}

Return a JSON object with a 'questions' array. Each question object must have these exact keys:
- 'question': The question text
- 'options': Array of 4 answer choices
- 'correct_answer': Index of the correct option (0-3)
{' - explanation: Detailed explanation of why this answer is correct' if include_explanations else ''}

Example format:
{{
    "questions": [
        {{
            "question": "What is the main purpose of...",
            "options": [
                "First option",
                "Second option",
                "Third option",
                "Fourth option"
            ],
            "correct_answer": 2,
            "explanation": "The third option is correct because..."
        }}
    ]
}}"""
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt4-o-mini",
        messages=messages,
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    return result.get('questions', [])

def generate_coding_questions(content, num_questions=5, difficulty="Medium", include_explanations=True):
    client = get_openai_client()
    messages = [
        {
            "role": "system",
            "content": "You are an expert programming instructor. Create Python coding exercises based on the provided content."
        },
        {
            "role": "user",
            "content": f"""Generate {num_questions} {difficulty.lower()}-level Python coding questions based on this content:

Content: {content}

Return a JSON object with a 'questions' array. Each question object must have these exact keys:
- 'question': A clear description of the coding problem
- 'starter_code': A Python code template for the student to start with
- 'solution': The complete working Python solution
- 'test_cases': Array of test cases, each showing input and expected output
{' - explanation: Detailed explanation of how the solution works' if include_explanations else ''}

Example format:
{{
    "questions": [
        {{
            "question": "Write a function that...",
            "starter_code": "def solution(n):\\n    # Your code here\\n    pass",
            "solution": "def solution(n):\\n    return n * 2",
            "test_cases": [
                {{"input": "5", "output": "10"}},
                {{"input": "0", "output": "0"}}
            ],
            "explanation": "This solution works by..."
        }}
    ]
}}"""
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)
