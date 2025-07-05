from deep_translator import GoogleTranslator

def translate_text(text, target_lang='en'):
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        return f"Error translating: {e}"
