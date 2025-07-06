import streamlit as st
from deep_translator import GoogleTranslator
from PyDictionary import PyDictionary
from gtts import gTTS
from langdetect import detect
import uuid
import os
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr

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
st.set_page_config(page_title="🌍 Translator + Voice", layout="centered")
st.title("🌍 Smart Voice Translator + Meaning")
st.markdown("🎤 Speak or type to translate any sentence in 20+ languages.")

# -------------------- Record Voice --------------------
if st.button("🎙 Click to Record Voice (5 sec)"):
    try:
        fs = 44100  # Sampling frequency
        seconds = 5
        st.info("Recording for 5 seconds... Speak now!")
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()
        write("input.wav", fs, recording)

        recognizer = sr.Recognizer()
        with sr.AudioFile("input.wav") as source:
            audio_data = recognizer.record(source)
            input_text = recognizer.recognize_google(audio_data)
            st.success(f"✅ Detected Speech: {input_text}")
    except Exception as e:
        st.error(f"❌ Error during voice input: {e}")
        input_text = ""
else:
    input_text = st.text_input("Or type a word or sentence:")

# -------------------- Language Selection --------------------
target_lang = st.selectbox("Translate to:", list(languages.keys()))
target_lang_code = languages[target_lang]

# -------------------- Main Logic --------------------
if st.button("🔄 Translate and Define"):
    if not input_text.strip():
        st.warning("Please speak or enter some text.")
    else:
        try:
            source_lang_code = detect(input_text)
            st.write(f"🧠 Detected Source Language: `{source_lang_code}` → Target: `{target_lang_code}`")

            if source_lang_code == target_lang_code:
                st.info("✅ The text is already in the selected language.")
                translated = input_text
            else:
                translated = GoogleTranslator(source='auto', target=target_lang_code).translate(input_text)
                st.success("✅ Translated Text:")
                st.write(translated)

            if len(input_text.strip().split()) == 1:
                meaning = dictionary.meaning(input_text)
                if meaning:
                    st.info("📚 Meaning:")
                    for pos, defs in meaning.items():
                        st.markdown(f"**{pos}:** {', '.join(defs[:2])}")
                else:
                    st.warning("No meaning found.")

            # Voice Output
            st.subheader("🔊 Listen")
            audio_filename = f"{uuid.uuid4()}.mp3"
            tts = gTTS(translated, lang=target_lang_code)
            tts.save(audio_filename)
            with open(audio_filename, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")
            os.remove(audio_filename)

        except Exception as e:
            st.error(f"❌ Error: {e}")
