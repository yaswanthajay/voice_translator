import streamlit as st
from deep_translator import GoogleTranslator

# Language options with language codes
languages = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Bengali": "bn",
    "Punjabi": "pa",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Arabic": "ar"
}

# Streamlit UI
st.set_page_config(page_title="🌐 Dual Language Translator", layout="centered")
st.title("🌐 AI Translator + Script Converter (Transliteration)")
st.markdown("🔤 Enter a sentence, get **translated** meaning and **transliterated** script.")

# Input
text = st.text_input("Enter text to translate:")
selected_lang = st.selectbox("Select target language:", list(languages.keys()))
lang_code = languages[selected_lang]

# Process
if st.button("Translate & Transliterate"):
    if text.strip() == "":
        st.warning("Please enter text.")
    else:
        try:
            # Translate
            translated = GoogleTranslator(source='auto', target=lang_code).translate(text)

            # Transliterate (convert script)
            transliterated = GoogleTranslator(source='auto', target=lang_code).transliterate(text)

            st.subheader("🔁 Translated Text:")
            st.success(translated)

            st.subheader("✍️ Transliteration (Script Change Only):")
            st.info(transliterated)

        except Exception as e:
            st.error(f"❌ Error: {e}")
