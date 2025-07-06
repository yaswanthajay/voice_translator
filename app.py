import streamlit as st
from deep_translator import GoogleTranslator
from PyDictionary import PyDictionary
from gtts import gTTS
import os
import uuid

# ----------------------------- Setup -----------------------------
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

# ---------------------------- UI ----------------------------
st.set_page_config(page_title="🌍 AI Word Translator + Meaning + Voice", layout="centered")
st.title("🌍 Smart Translator + Word Meaning + Voice")
st.markdown("🔤 Translate, define and speak any word or sentence in over 20 languages.")

input_text = st.text_input("Enter a word or sentence:")
target_lang = st.selectbox("Select language to translate to:", list(languages.keys()))
target_lang_code = languages[target_lang]

# ------------------------- Main Features --------------------------
if st.button("Translate and Define"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        try:
            # Translate full text
            translated = GoogleTranslator(source='auto', target=target_lang_code).translate(input_text)
            st.success("✅ Translated Text:")
            st.write(translated)

            # Show meaning for single word
            if len(input_text.strip().split()) == 1:
                meaning = dictionary.meaning(input_text)
                if meaning:
                    st.info("📚 Meaning:")
                    for pos, defs in meaning.items():
                        st.markdown(f"**{pos}:** {', '.join(defs[:2])}")
                else:
                    st.warning("No meaning found.")

            # Speak translated output (auto plays on next button)
            st.subheader("🔊 Hear the Translated Text")
            if translated.strip():
                audio_filename = f"{uuid.uuid4()}.mp3"
                tts = gTTS(translated, lang=target_lang_code)
                tts.save(audio_filename)
                audio_file = open(audio_filename, "rb")
                st.audio(audio_file.read(), format="audio/mp3")
                audio_file.close()
                os.remove(audio_filename)

        except Exception as e:
            st.error(f"Error: {e}")
