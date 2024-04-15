import os
import fitz  # PyMuPDF
import re
import spacy
from spacy.matcher import Matcher
import csv

# Load the English language model for SpaCy
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_file)
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text += page.get_text()
        pdf_document.close()
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

def extract_technical_skills(resume_text):
    skills_pattern = r"TECHNICAL SKILLS\n(.*?)(?=\n[A-Z]+\n|\Z)"
    match = re.search(skills_pattern, resume_text, re.DOTALL)
    return match.group(1).strip() if match else "Skills Not Found"

def extract_education(resume_text):
    education_pattern = r"EDUCATION\n(.*?)\n[A-Z]+\n"
    match = re.search(education_pattern, resume_text, re.DOTALL)
    return match.group(1).strip() if match else "Education Not Found"

def extract_experience(resume_text):
    experience_pattern = r"EXPERIENCE\n(.*?)(?=\n[A-Z]+\n|\Z)"
    match = re.search(experience_pattern, resume_text, re.DOTALL)
    return match.group(1).strip() if match else "Experience Not Found"

def extract_personal_projects(resume_text):
    projects_pattern = r"PERSONAL PROJECTS\n(.*?)(?=\n[A-Z]+\n|\Z)"
    match = re.search(projects_pattern, resume_text, re.DOTALL)
    return match.group(1).strip() if match else "Projects Not Found"

def extract_achievements(resume_text):
    achievements_pattern = r"ACHIEVEMENTS\n(.*?)(?=\n[A-Z]+\n|\Z)"
    match = re.search(achievements_pattern, resume_text, re.DOTALL)
    return match.group(1).strip() if match else "Achievements/Certificates Not Found"

def process_resume(resume_file, output_csv):
    resume_text = extract_text_from_pdf(resume_file)
    
    # Extract information
    candidate_name = extract_candidate_name(resume_text)
    technical_skills = extract_technical_skills(resume_text)
    education = extract_education(resume_text)
    experience = extract_experience(resume_text)
    personal_projects = extract_personal_projects(resume_text)
    achievements = extract_achievements(resume_text)

    # Append extracted information to CSV file
    with open(output_csv, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([candidate_name, technical_skills, education, experience, personal_projects, achievements])

# Directory containing resumes
resumes_dir = r"C:\Users\gupta\OneDrive\Desktop\Resume"
output_csv = "resume_data.csv"

# Write header to CSV file
with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Candidate Name", "Technical Skills", "Education", "Experience", "Personal Projects", "Achievements/Certificates"])

# Process all resumes in the directory
for resume_file in os.listdir(resumes_dir):
    if resume_file.endswith(".pdf"):
        resume_path = os.path.join(resumes_dir, resume_file)
        process_resume(resume_path, output_csv)

print("Resume processing completed and CSV exported.")