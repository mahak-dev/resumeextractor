from neo4j import GraphDatabase
import os
from pdfminer.high_level import extract_text # type: ignore

# Neo4j connection details
url = "bolt://localhost:7687"
username = "neo4j"
password = "fWuii2EL5YCvFowJZ75saoK4vC7ubwJgZOJXzi7C5Kg"

driver = GraphDatabase.driver(url, auth=(username, password))

# Function to process and insert data from a resume
def process_resume(resume_file):
    resume_text = extract_text(resume_file)

    # Parse resume_text to extract candidate info, degrees, certifications, etc.

    # Example query to insert data into Neo4j
    with driver.session() as session:
        session.run(
            """
            CREATE (c:Candidate {name: $name, degrees: $degrees, certifications: $certifications})
            """,
            {"name": "John Doe", "degrees": ["B.Sc. in Computer Science", "MBA"], "certifications": ["CompTIA A+ certified (2012)", "AWS Certified Solutions Architect"]}
        )

# Directory containing resumes
resumes_dir = "path/to/resumes/directory"

# Process all resumes in the directory
for resume_file in os.listdir(resumes_dir):
    if resume_file.endswith(".pdf"):
        process_resume(os.path.join(resumes_dir, resume_file))

print("Database population completed.")
