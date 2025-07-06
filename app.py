import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import requests

# Title
st.title("🔤 Word Translator + Meaning + Voice Output")

# Input word
word = st.text_input("Enter a word:")

# Target language selection
# Get supported languages and convert to dictionary format
language_list = GoogleTranslator.get_supported_languages()
languages = {lang.capitalize(): lang for lang in language_list}
language_names = list(languages.keys())
selected_language = st.selectbox("Select language to translate to:", language_names)


# Button
if st.button("Translate and Explain"):
    if word.strip() == "":
        st.warning("Please enter a word.")
    else:
        try:
            # Translate
            translated = GoogleTranslator(source='auto', target=languages[selected_language]).translate(word)
            st.success(f"Translated to {selected_language}: {translated}")

            # Meaning from Dictionary API
            try:
                response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
                if response.status_code == 200:
                    data = response.json()
                    meanings = data[0]['meanings'][0]['definitions'][0]['definition']
                    st.info(f"Meaning in English: {meanings}")
                else:
                    st.warning("Meaning not found. Try another word.")
            except Exception as e:
                st.error(f"Error fetching meaning: {e}")

            # Generate speech for the translated word
            tts = gTTS(translated, lang=languages[selected_language])
            audio_file = "translated_audio.mp3"
            tts.save(audio_file)

            # Play audio
            st.audio(audio_file, format='audio/mp3')
        except Exception as e:
            st.error(f"Translation error: {e}")
