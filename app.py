import streamlit as st
from deep_translator import GoogleTranslator
from PyDictionary import PyDictionary
from gtts import gTTS
from langdetect import detect
import os
import uuid
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import speech_recognition as sr

# -------------------- Setup --------------------
dictionary = PyDictionary()

languages = {
    "English": "en", "Mandarin Chinese": "zh-CN", "Hindi": "hi", "Spanish": "es", "French": "fr",
    "Arabic": "ar", "Bengali": "bn", "Russian": "ru", "Portuguese": "pt", "Urdu": "ur",
    "German": "de", "Japanese": "ja", "Tamil": "ta", "Telugu": "te", "Italian": "it",
    "Korean": "ko", "Turkish": "tr", "Vietnamese": "vi", "Indonesian": "id", "Marathi": "mr"
}

# -------------------- UI --------------------
st.set_page_config(page_title="🌍 Translator + Meaning + Voice", layout="centered")
st.title("🌍 Smart Voice Translator")
st.markdown("🎤 Speak or type a sentence to translate, define, and speak it in another language.")

# Input method
use_voice = st.checkbox("🎙️ Use Microphone Input")

if use_voice:
    duration = st.slider("Select duration of recording (seconds)", 2, 10, 5)
    if st.button("Start Recording"):
        st.info("Recording...")
        fs = 44100
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        audio_path = f"recording_{uuid.uuid4()}.wav"
        scipy.io.wavfile.write(audio_path, fs, recording)

        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                input_text = recognizer.recognize_google(audio_data)
                st.success(f"🎧 Recognized: {input_text}")
            except sr.UnknownValueError:
                st.error("❌ Could not understand audio.")
                input_text = ""
        os.remove(audio_path)
else:
    input_text = st.text_input("Enter a word or sentence:")

# Select language
target_lang = st.selectbox("Translate to:", list(languages.keys()))
target_lang_code = languages[target_lang]

# -------------------- Main Logic --------------------
if st.button("Translate and Define"):
    if not input_text.strip():
        st.warning("Please enter or speak something.")
    else:
        try:
            # Language Detection
            source_lang_code = detect(input_text)
            st.write(f"🧠 Detected: `{source_lang_code}` → `{target_lang_code}`")

            # Translation
            if source_lang_code == target_lang_code:
                st.info("Already in target language.")
                translated = input_text
            else:
                translated = GoogleTranslator(source='auto', target=target_lang_code).translate(input_text)

            st.success("✅ Translated Text:")
            st.write(translated)

            # Meaning (for single word)
            if len(input_text.split()) == 1:
                meaning = dictionary.meaning(input_text)
                if meaning:
                    st.info("📚 Meaning:")
                    for pos, defs in meaning.items():
                        st.markdown(f"**{pos}:** {', '.join(defs[:2])}")
                else:
                    st.warning("❌ No meaning found.")

            # Speak translated output
            st.subheader("🔊 Listen")
            audio_filename = f"{uuid.uuid4()}.mp3"
            tts = gTTS(translated, lang=target_lang_code)
            tts.save(audio_filename)
            audio_file = open(audio_filename, "rb")
            st.audio(audio_file.read(), format="audio/mp3")
            audio_file.close()
            os.remove(audio_filename)

        except Exception as e:
            st.error(f"❌ Error: {e}")
