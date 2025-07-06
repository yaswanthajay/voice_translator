import speech_recognition as sr

def listen_and_convert():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Please speak.")
        audio = recognizer.listen(source, timeout=5)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"📝 Recognized: {text}")
        return text
    except sr.UnknownValueError:
        st.error("❌ Could not understand the audio.")
    except sr.RequestError:
        st.error("❌ Could not request results from the recognition service.")
    return ""

# Add a "Listen" button
if st.button("🎤 Listen"):
    input_text = listen_and_convert()
