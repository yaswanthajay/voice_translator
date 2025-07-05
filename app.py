import streamlit as st
from record_voice import record_voice
from translate_text import translate_text
from speak_text import speak_text

st.set_page_config(page_title="Voice-to-Voice AI Translator", layout="centered")
st.title("🌐 Voice-to-Voice AI Translator")
st.markdown("🎤 Speak in one language, get real-time voice output in another!")

target_lang = st.selectbox("Choose target language:", ["en", "fr", "hi", "te", "es", "de"])

if st.button("🎙 Start Translation"):
    st.info("Listening... Please speak into the mic.")
    original_text = record_voice()

    if "Error" in original_text:
        st.error(original_text)
    else:
        st.success(f"You said: `{original_text}`")
        translated = translate_text(original_text, target_lang)
        st.markdown(f"**Translated:** `{translated}`")

        speak_text(translated, lang=target_lang)
        st.success("✅ Voice output played!")
