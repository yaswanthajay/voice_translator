import streamlit as st
from deep_translator import GoogleTranslator
from PyDictionary import PyDictionary
from gtts import gTTS
from langdetect import detect
import os
import uuid

# -------------------- Setup --------------------
dictionary = PyDictionary()

languages = {
    "English": "en",
    "Mandarin Chinese": "zh-CN",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "Arabic": "ar",
    "Bengali": "bn",
    "Russian": "ru",
    "Portuguese": "pt",
    "Urdu": "ur",
    "German": "de",
    "Japanese": "ja",
    "Tamil": "ta",
    "Telugu": "te",
    "Italian": "it",
    "Korean": "ko",
    "Turkish": "tr",
    "Vietnamese": "vi",
    "Indonesian": "id",
    "Marathi": "mr"
}

# -------------------- UI Setup --------------------
st.set_page_config(page_title="🌍 Translator + Meaning + Voice", layout="centered")
st.title("🌍 Smart Translator + Word Meaning + Voice")
st.markdown("🔤 Translate, define, and listen to any word or sentence in 20+ languages.")

input_text = st.text_input("Enter a word or sentence:")
target_lang = st.selectbox("Translate to:", list(languages.keys()))
target_lang_code = languages[target_lang]

# -------------------- Main Logic --------------------
if st.button("Translate and Define"):
    if not input_text.strip():
        st.warning("Please enter text.")
    else:
        try:
            # Detect source language
            source_lang_code = detect(input_text)
            st.write(f"🧠 Detected Source Language: `{source_lang_code}` → Target: `{target_lang_code}`")

            # If input and target languages are the same, skip translation
            if source_lang_code == target_lang_code:
                st.info("🌐 The word is already in the selected language. No translation needed.")
                translated = input_text
            else:
                translated = GoogleTranslator(source='auto', target=target_lang_code).translate(input_text)
                st.success("✅ Translated Text:")
                st.write(translated)

            # Show meaning if input is a single word (in source language)
            if len(input_text.strip().split()) == 1:
                meaning = dictionary.meaning(input_text)
                if meaning:
                    st.info("📚 Meaning:")
                    for pos, defs in meaning.items():
                        st.markdown(f"**{pos}:** {', '.join(defs[:2])}")
                else:
                    st.warning("No meaning found.")

            # Text-to-speech output
            st.subheader("🔊 Listen")
            audio_filename = f"{uuid.uuid4()}.mp3"
            tts = gTTS(text=translated, lang=target_lang_code)
            tts.save(audio_filename)
            with open(audio_filename, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
            os.remove(audio_filename)

        except Exception as e:
            st.error(f"❌ Error: {e}")
