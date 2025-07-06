import streamlit as st
import os
import uuid
from gtts import gTTS
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect
from PyDictionary import PyDictionary

# Setup
dictionary = PyDictionary()

languages = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur"
}

st.set_page_config(page_title="🌍 Voice Translator", layout="centered")
st.title("🌍 Smart Voice Translator + Word Meaning + Voice")

# File Upload instead of Microphone
st.subheader("🎙️ Upload a Voice (.wav) File")
audio_file = st.file_uploader("Upload .wav audio", type=["wav"])

target_lang = st.selectbox("Translate to:", list(languages.keys()))
target_lang_code = languages[target_lang]

if audio_file is not None and st.button("Translate & Speak"):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            input_text = recognizer.recognize_google(audio_data)
            st.write("🗣️ Detected Text:", input_text)

        # Language detection and translation
        detected_lang = detect(input_text)
        translated = GoogleTranslator(source='auto', target=target_lang_code).translate(input_text)
        st.success("✅ Translated Text:")
        st.write(translated)
        st.write(f"🧠 Detected Language: `{detected_lang}` → `{target_lang_code}`")

        # Dictionary meaning
        if len(input_text.strip().split()) == 1:
            meaning = dictionary.meaning(input_text)
            if meaning:
                st.info("📚 Meaning:")
                for pos, defs in meaning.items():
                    st.markdown(f"**{pos}:** {', '.join(defs[:2])}")
            else:
                st.warning("No meaning found.")

        # Speak
        tts = gTTS(translated, lang=target_lang_code)
        audio_path = f"{uuid.uuid4()}.mp3"
        tts.save(audio_path)
        st.audio(audio_path, format="audio/mp3")
        os.remove(audio_path)

    except Exception as e:
        st.error(f"❌ Error: {e}")
