import streamlit as st
from deep_translator import GoogleTranslator

# Top 50 Languages and Codes
languages = {
    "English": "en", "Mandarin Chinese": "zh-CN", "Hindi": "hi", "Spanish": "es", "French": "fr",
    "Arabic": "ar", "Bengali": "bn", "Russian": "ru", "Portuguese": "pt", "Urdu": "ur",
    "Indonesian": "id", "German": "de", "Japanese": "ja", "Marathi": "mr", "Telugu": "te",
    "Turkish": "tr", "Tamil": "ta", "Vietnamese": "vi", "Korean": "ko", "Italian": "it",
    "Cantonese (Yue)": "yue", "Thai": "th", "Gujarati": "gu", "Polish": "pl", "Ukrainian": "uk",
    "Malayalam": "ml", "Kannada": "kn", "Burmese": "my", "Romanian": "ro", "Hausa": "ha",
    "Dutch": "nl", "Pashto": "ps", "Tagalog": "tl", "Persian (Farsi)": "fa", "Malay": "ms",
    "Amharic": "am", "Sinhala": "si", "Nepali": "ne", "Azerbaijani": "az", "Somali": "so",
    "Czech": "cs", "Greek": "el", "Swedish": "sv", "Serbian": "sr", "Hungarian": "hu",
    "Finnish": "fi", "Hebrew": "he", "Slovak": "sk", "Croatian": "hr", "Lithuanian": "lt"
}

st.set_page_config(page_title="🌐 AI Language Translator", layout="centered")

st.title("🌐 Voice-to-Voice AI Language Translator (Text Mode)")
st.markdown("Translate any language to another in real time using AI!")

# Input Text
input_text = st.text_area("Enter text to translate", height=150)

# Select Target Language
target_language_name = st.selectbox("Select Target Language", list(languages.keys()))
target_language_code = languages[target_language_name]

# Translate button
if st.button("Translate"):
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        try:
            translated = GoogleTranslator(source='auto', target=target_language_code).translate(input_text)
            st.success("Translated Text:")
            st.text_area("Result", translated, height=150)
        except Exception as e:
            st.error(f"Error during translation: {e}")
