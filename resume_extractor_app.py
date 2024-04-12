import os
import re
import spacy # type: ignore
from spacy.matcher import Matcher # type: ignore
import pdfplumber # type: ignore

# Load the English language model for SpaCy
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        # Open the PDF file using pdfplumber
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from {pdf_file}: {e}")
    return text

def extract_candidate_name(resume_text):
    doc = nlp(resume_text)
    matcher = Matcher(nlp.vocab)
    pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]
    matcher.add("NAME_PATTERN", [pattern])
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text

    return "Name Not Found"

def extract_candidate_info(resume_text):
    candidate_info = {}
    
    # Extract Candidate Name
    candidate_info["Name"] = extract_candidate_name(resume_text)

    # Extract Technical Skills
    skills_pattern = r"(TECHNICAL|PROFESSIONAL|OTHER)?\s*SKILLS\n(.*?)\n[A-Z]+\n"
    match = re.search(skills_pattern, resume_text, re.DOTALL)
    candidate_info["Technical Skills"] = match.group(1).strip() if match else "Skills Not Found"

    # Extract Education Details
    education_pattern = r"EDUCATION\n(.*?)\n[A-Z]+\n"
    match = re.search(education_pattern, resume_text, re.DOTALL)
    candidate_info["Education"] = match.group(1).strip() if match else "Education Not Found"

    # Extract Experience Details
    experience_pattern = r"EXPERIENCE\n(.*?)\n[A-Z]+\n"
    match = re.search(experience_pattern, resume_text, re.DOTALL)
    candidate_info["Experience"] = match.group(1).strip() if match else "Experience Not Found"

    # Extract Personal Projects
    projects_pattern = r"PERSONAL PROJECTS\n(.*?)\n[A-Z]+\n"
    match = re.search(projects_pattern, resume_text, re.DOTALL)
    candidate_info["Personal Projects"] = match.group(1).strip() if match else "Projects Not Found"

    # Extract Achievements and Certificates
    achievements_pattern = r"ACHIEVEMENTS AND CERTIFICATES\n(.*?)\n[A-Z]+\n"
    match = re.search(achievements_pattern, resume_text, re.DOTALL)
    candidate_info["Achievements/Certificates"] = match.group(1).strip() if match else "Achievements/Certificates Not Found"

    return candidate_info

def process_resume(resume_file):
    resume_text = extract_text_from_pdf(resume_file)
    candidate_info = extract_candidate_info(resume_text)

    # Print extracted information
    for key, value in candidate_info.items():
        print(f"{key}: {value}")
        print("-" * 30)

# Directory containing resumes
resumes_dir = r"C:\Users\gupta\OneDrive\Desktop\Resume"

# Process all resumes in the directory
for resume_file in os.listdir(resumes_dir):
    if resume_file.endswith(".pdf"):
        print(f"Processing Resume: {resume_file}")
        process_resume(os.path.join(resumes_dir, resume_file))

print("Resume processing completed.")
