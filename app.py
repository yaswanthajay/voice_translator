import streamlit as st
from deep_translator import GoogleTranslator

# Supported languages and their ISO codes
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
    "Chinese (Simplified)": "zh-CN",
    "Arabic": "ar"
}

st.set_page_config(page_title="Dual Translator + Script Converter", layout="wide")
st.title("🌐 Dual Translator + Transliterator")
st.markdown(
    "Enter text below and select a target language. "
    "You’ll see both the **translated meaning** and the **script-converted** (transliterated) version."
)

# Inputs
text = st.text_area("📝 Enter text to translate:", height=150)
target_lang = st.selectbox("🎯 Select target language:", list(languages.keys()))
lang_code = languages[target_lang]

# Action
if st.button("🔄 Translate & Convert Script"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            # 1. Translation (meaning)
            translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
            # 2. Transliteration (script conversion)
            transliterated = GoogleTranslator(source='auto', target=lang_code).transliterate(text)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🈳 Translated Meaning")
                st.success(translated)
            with col2:
                st.subheader("🔤 Transliteration (Script)")
                # If transliteration fails or returns same as input, we still show it
                st.info(transliterated)
        except Exception as e:
            st.error(f"Error during translation: {e}")
