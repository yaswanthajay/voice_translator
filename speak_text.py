from gtts import gTTS
import os
import platform

def speak_text(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")

    # Play the mp3 file
    if platform.system() == "Windows":
        os.system("start output.mp3")
    elif platform.system() == "Darwin":  # macOS
        os.system("afplay output.mp3")
    else:  # Linux
        os.system("mpg123 output.mp3")
