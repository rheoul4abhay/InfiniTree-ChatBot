import textract

def extract_text_from_file(filepath):
    try:
        return textract.process(filepath).decode('utf-8')
    except Exception as e:
        return f"Could not extract text from this file: {str(e)}"