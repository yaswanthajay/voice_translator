import streamlit as st
from deep_translator import GoogleTranslator
from PyDictionary import PyDictionary
from gtts import gTTS
from langdetect import detect
import speech_recognition as sr
import uuid
import os

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

# -------------------- UI --------------------
st.set_page_config(page_title=" Smart Voice Translator", layout="centered")
st.title(" Smart Voice Translator + Dictionary + Speech")
st.markdown(" Speak or type a word/sentence → get translation, meaning, and audio.")

# Voice Input
use_voice = st.checkbox("🎙 Use microphone to input")

if use_voice:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Please speak now...")
        audio = recognizer.listen(source, timeout=5)
    try:
        input_text = recognizer.recognize_google(audio)
        st.success(f" You said: `{input_text}`")
    except Exception as e:
        st.error(f"Speech Error: {e}")
        input_text = ""
else:
    input_text = st.text_input(" Enter text manually:")

target_lang = st.selectbox(" Translate to:", list(languages.keys()))
target_lang_code = languages[target_lang]

# -------------------- Main Logic --------------------
if st.button(" Translate and Define"):
    if not input_text.strip():
        st.warning("Please provide text input.")
    else:
        try:
            # Detect source language
            source_lang_code = detect(input_text)
            st.write(f"Detected Language: `{source_lang_code}` → `{target_lang_code}`")

            # Translate
            if source_lang_code == target_lang_code:
                translated = input_text
                st.info("Input is already in the target language.")
            else:
                translated = GoogleTranslator(source='auto', target=target_lang_code).translate(input_text)
                st.success(" Translated Text:")
                st.write(translated)

            # Dictionary Meaning (if word only)
            if len(input_text.strip().split()) == 1:
                meaning = dictionary.meaning(input_text)
                if meaning:
                    st.info(" Word Meaning:")
                    for pos, defs in meaning.items():
                        st.markdown(f"**{pos}**: {', '.join(defs[:2])}")
                else:
                    st.warning("❌ No meaning found.")

            # Text to Speech
            st.subheader(" Listen to Translation")
            audio_filename = f"{uuid.uuid4()}.mp3"
            tts = gTTS(translated, lang=target_lang_code)
            tts.save(audio_filename)
            audio_file = open(audio_filename, "rb")
            st.audio(audio_file.read(), format="audio/mp3")
            audio_file.close()
            os.remove(audio_filename)

        except Exception as e:
            st.error(f"❌ Error: {e}")
