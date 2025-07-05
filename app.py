import streamlit as st
from translate_text import translate_text
from speak_text import speak_text

st.set_page_config(page_title="Voice-to-Voice Translator", layout="centered")
st.title("🌐 Voice-to-Voice AI Translator")
st.markdown("💬 Type your sentence to translate and hear it.")

# Input
input_text = st.text_input("Enter text to translate:")

# Language selection
target_lang = st.selectbox("Translate to:", ["en", "hi", "te", "fr", "es", "de"])

if st.button("🔄 Translate & Speak"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        translated = translate_text(input_text, target_lang)
        st.success(f"Translated: {translated}")
        speak_text(translated, lang=target_lang)
