import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    return [token.text.lower() for token in doc if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop]
