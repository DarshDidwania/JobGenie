import re
import spacy
import pdfplumber
import docx
import os

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_email(text):
    match = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    return match[0] if match else None

def extract_phone(text):
    match = re.findall(r'\+?\d[\d\s()-]{8,}', text)
    return match[0] if match else None

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_skills(text, skill_keywords=None):
    if not skill_keywords:
        skill_keywords = ['python', 'java', 'machine learning', 'sql', 'c++', 'react', 'excel', 'flask', 'django']
    text_lower = text.lower()
    return list(set([skill for skill in skill_keywords if skill in text_lower]))

def parse_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif ext == '.docx':
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported format")

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }
