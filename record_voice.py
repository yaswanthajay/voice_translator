import speech_recognition as sr

def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Recognized:", text)
        return text
    except Exception as e:
        return f"Error recognizing speech: {e}"
