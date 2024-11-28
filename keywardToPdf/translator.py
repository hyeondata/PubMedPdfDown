from googletrans import Translator

def translate_text(text:str, dest='en', src='auto'):
    try:
        print("번역 단어:"+ str(text))
        translator = Translator()
        result = translator.translate(text, dest=dest, src=src)
        return result.text
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    text = "크론병"
    translated = translate_text(text)
    if translated:
        print(f"Original: {text}")
        print(f"Translated: {translated}")