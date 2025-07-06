import streamlit as st
from googletrans import Translator

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
    "Chinese (Simplified)": "zh-cn",
    "Arabic": "ar"
}

st.set_page_config(page_title="Dual Translator + Transliterator", layout="wide")
st.title("🌐 Dual Translator + Transliterator")
st.markdown(
    "Enter text and select a target language. "
    "You’ll get both the **translated meaning** and the **transliteration**."
)

# Initialize the translator once
translator = Translator()

text = st.text_area("📝 Enter text to translate:", height=150)
target_lang = st.selectbox("🎯 Select target language:", list(languages.keys()))
lang_code = languages[target_lang]

if st.button("🔄 Translate & Transliterate"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            # Perform translation
            result = translator.translate(text, dest=lang_code)
            translated = result.text
            transliterated = result.pronunciation or translated

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🈳 Translated Meaning")
                st.success(translated)
            with col2:
                st.subheader("🔤 Transliteration (Script)")
                st.info(transliterated)

        except Exception as e:
            st.error(f"Error during translation: {e}")
