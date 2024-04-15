import pandas as pd
from neo4j import GraphDatabase

# Neo4j AuraDB connection URI, username, and password
uri = "bolt://localhost:7687"
user = "neo4j"
password = "mahak@123"

# Function to create a Neo4j session
def get_neo4j_session(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver.session()

# Function to load data from CSV and create nodes and relationships in Neo4j
def load_csv_to_neo4j(session, csv_file):
    # Load CSV data into a DataFrame
    df = pd.read_csv(csv_file)

    # Cypher query to create nodes and relationships
    query = """
    UNWIND $data as row
    MERGE (n:Node {id: row.id})
    ON CREATE SET n += row.properties
    """

    # Run the query with parameters
    session.run(query, data=df.to_dict('records'))

csv_file_path = r"C:\Users\gupta\Downloads\gemini Resume application\resume_data.csv"

# Connect to Neo4j AuraDB
with get_neo4j_session(uri, user, password) as session:
    # Load CSV data to Neo4j
    load_csv_to_neo4j(session, csv_file_path)

print("CSV data loaded into Neo4j AuraDB.")
