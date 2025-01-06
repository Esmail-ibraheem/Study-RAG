import streamlit as st
from typing import Optional
import json
import os

def initialize_settings():
    """Initialize settings in session state if they don't exist."""
    if "settings" not in st.session_state:
        # Try to load settings from file
        settings_file = "settings.json"
        if os.path.exists(settings_file):
            with open(settings_file, "r") as f:
                st.session_state.settings = json.load(f)
        else:
            st.session_state.settings = {
                "api_keys": {
                    "openai": "",
                    "mistral": "",
                    "together": ""
                },
                "model_preferences": {
                    "default_model": "gpt4-o-mini",
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                "ui_preferences": {
                    "theme": "light",
                    "show_explanations": True
                }
            }
    # Ensure all required fields exist
    if "model_preferences" not in st.session_state.settings:
        st.session_state.settings["model_preferences"] = {
            "default_model": "gpt4-o-mini",
            "temperature": 0.7,
            "max_tokens": 2000
        }
    if "ui_preferences" not in st.session_state.settings:
        st.session_state.settings["ui_preferences"] = {
            "theme": "light",
            "show_explanations": True
        }
    if "api_keys" not in st.session_state.settings:
        st.session_state.settings["api_keys"] = {
            "openai": "",
            "mistral": "",
            "together": ""
        }

def save_settings():
    """Save current settings to a file."""
    settings_file = "settings.json"
    with open(settings_file, "w") as f:
        json.dump(st.session_state.settings, f, indent=4)

def validate_api_key(api_key: Optional[str], provider: str) -> bool:
    """Validate API key format (basic check)."""
    if not api_key:
        return False
    
    if provider == "openai" and api_key.startswith("sk-"):
        return len(api_key) > 20
    elif provider == "mistral" and len(api_key) > 20:
        return True
    elif provider == "together" and len(api_key) > 20:
        return True
    return False

# Initialize settings
initialize_settings()

# Page title and description
st.title("⚙️ Settings")
st.markdown("""
    <style>
        .settings-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #dee2e6;
        }
        .settings-header {
            color: #2c3e50;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# API Keys Section
st.markdown('<div class="settings-container">', unsafe_allow_html=True)
st.markdown('<h2 class="settings-header">🔑 API Keys</h2>', unsafe_allow_html=True)
st.markdown("Securely manage your API keys for different AI providers.")

# OpenAI API Key
openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    value=st.session_state.settings["api_keys"]["openai"],
    help="Enter your OpenAI API key"
)
if openai_api_key != st.session_state.settings["api_keys"]["openai"]:
    st.session_state.settings["api_keys"]["openai"] = openai_api_key
    st.session_state.openai_api_key = openai_api_key
    save_settings()

# Together AI API Key
together_api_key = st.text_input(
    "Together AI API Key",
    type="password",
    value=st.session_state.settings["api_keys"]["together"],
    help="Enter your Together AI API key for OCR and image analysis"
)
if together_api_key != st.session_state.settings["api_keys"]["together"]:
    st.session_state.settings["api_keys"]["together"] = together_api_key
    st.session_state.together_api_key = together_api_key
    save_settings()

# Mistral API Key
mistral_api_key = st.text_input(
    "Mistral API Key",
    type="password",
    value=st.session_state.settings["api_keys"]["mistral"],
    help="Enter your Mistral API key"
)
if mistral_api_key != st.session_state.settings["api_keys"]["mistral"]:
    st.session_state.settings["api_keys"]["mistral"] = mistral_api_key
    st.session_state.mistral_api_key = mistral_api_key
    save_settings()

st.markdown('</div>', unsafe_allow_html=True)

# Model Preferences Section
st.markdown('<div class="settings-container">', unsafe_allow_html=True)
st.markdown('<h2 class="settings-header">🤖 Model Preferences</h2>', unsafe_allow_html=True)

# Model selection
default_model = st.selectbox(
    "Default Model",
    options=["gpt4-o-mini", "gpt-3.5-turbo", "mistral-medium", "mistral-small", "together-ai-model"],
    index=0,
    help="Select the default AI model to use"
)
if default_model != st.session_state.settings["model_preferences"]["default_model"]:
    st.session_state.settings["model_preferences"]["default_model"] = default_model
    save_settings()

# Temperature setting
temperature = st.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=st.session_state.settings["model_preferences"]["temperature"],
    step=0.1,
    help="Control randomness in responses (0 = deterministic, 1 = creative)"
)
if temperature != st.session_state.settings["model_preferences"]["temperature"]:
    st.session_state.settings["model_preferences"]["temperature"] = temperature
    save_settings()

st.markdown('</div>', unsafe_allow_html=True)

# UI Preferences Section
st.markdown('<div class="settings-container">', unsafe_allow_html=True)
st.markdown('<h2 class="settings-header">🎨 UI Preferences</h2>', unsafe_allow_html=True)

# Theme selection
theme = st.selectbox(
    "Theme",
    options=["light", "dark"],
    index=0 if st.session_state.settings["ui_preferences"]["theme"] == "light" else 1,
    help="Select the application theme"
)
if theme != st.session_state.settings["ui_preferences"]["theme"]:
    st.session_state.settings["ui_preferences"]["theme"] = theme
    save_settings()

# Show explanations toggle
show_explanations = st.toggle(
    "Show Explanations",
    value=st.session_state.settings["ui_preferences"]["show_explanations"],
    help="Toggle detailed explanations in quiz and coding questions"
)
if show_explanations != st.session_state.settings["ui_preferences"]["show_explanations"]:
    st.session_state.settings["ui_preferences"]["show_explanations"] = show_explanations
    save_settings()

st.markdown('</div>', unsafe_allow_html=True)

# Reset Settings Button
if st.button("Reset to Default Settings", type="secondary"):
    st.session_state.settings = {
        "api_keys": {
            "openai": "",
            "mistral": "",
            "together": ""
        },
        "model_preferences": {
            "default_model": "gpt4-o-mini",
            "temperature": 0.7,
            "max_tokens": 2000
        },
        "ui_preferences": {
            "theme": "light",
            "show_explanations": True
        }
    }
    save_settings()
    st.success("Settings reset to default values!")
    st.rerun()
