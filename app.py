import streamlit as st
import os
import uuid
from gtts import gTTS
from deep_translator import GoogleTranslator
from langdetect import detect
from PyDictionary import PyDictionary
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

# -------------------- UI Setup --------------------
st.set_page_config(page_title="🌍 Smart Voice Translator", layout="centered")
st.title("🌍 Smart Voice Translator + Dictionary + Speech")
st.markdown("🎤 Upload voice or type text → get translation, meaning, and speech output.")

# -------------------- Input Options --------------------
option = st.radio("Choose Input Method:", ("🎙️ Upload Audio (.wav)", "⌨️ Type Manually"))

input_text = ""

if option == "🎙️ Upload Audio (.wav)":
    audio_file = st.file_uploader("Upload .wav audio file", type=["wav"])
    if audio_file is not None:
        try:
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
                input_text = recognizer.recognize_google(audio_data)
                st.success(f"✅ Recognized Speech: `{input_text}`")
        except Exception as e:
            st.error(f"❌ Error recognizing speech: {e}")
else:
    input_text = st.text_input("💬 Enter text manually:")

# -------------------- Language Selection --------------------
target_lang = st.selectbox("🌐 Translate to:", list(languages.keys()))
target_lang_code = languages[target_lang]

# -------------------- Process --------------------
if st.button("🌍 Translate and Speak"):
    if not input_text.strip():
        st.warning("⚠️ Please provide some input.")
    else:
        try:
            # Detect Language
            detected_lang = detect(input_text)
            st.write(f"🧠 Detected Language: `{detected_lang}` → `{target_lang_code}`")

            # Translate
            if detected_lang == target_lang_code:
                translated = input_text
                st.info("The input is already in the target language.")
            else:
                translated = GoogleTranslator(source='auto', target=target_lang_code).translate(input_text)
                st.success("✅ Translated Text:")
                st.write(translated)

            # Show Dictionary Meaning (if single word)
            if len(input_text.strip().split()) == 1:
                meaning = dictionary.meaning(input_text)
                if meaning:
                    st.info("📚 Dictionary Meaning:")
                    for pos, defs in meaning.items():
                        st.markdown(f"**{pos}**: {', '.join(defs[:2])}")
                else:
                    st.warning("No meaning found in dictionary.")

            # Text to Speech
            st.subheader("🔊 Listen to Translation")
            audio_filename = f"{uuid.uuid4()}.mp3"
            tts = gTTS(translated, lang=target_lang_code)
            tts.save(audio_filename)
            with open(audio_filename, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
            os.remove(audio_filename)

        except Exception as e:
            st.error(f"❌ Processing Error: {e}")
