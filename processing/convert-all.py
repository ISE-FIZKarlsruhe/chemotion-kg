import os
import glob
import re
import time
from rdflib import Graph, URIRef, BNode

# Define base directories
input_dir = "data"
output_dir = "output"
base_iri = "https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/resources/"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Dictionary to store unique IDs for blank nodes
blank_node_ids = {}
blank_counter = 0  # Ensures unique IDs across the graph

# Dictionary to track unique persons and organizations
person_registry = {}
organization_registry = {}

def get_unique_id():
    global blank_counter
    blank_counter += 1
    return str(int(time.time() * 1000)) + f"_{blank_counter}"  # Ensuring unique ID

# Function to extract ORCID ID from a full path
def extract_orcid_id(uri):
    match = re.search(r"(\d{4}-\d{4}-\d{4}-\d{3}[\dX])$", uri)
    return match.group(1) if match else None

# Function to convert extracted ORCID ID to a proper ORCID URI
def convert_to_orcid(uri):
    orcid_id = extract_orcid_id(uri)
    return URIRef(f"https://orcid.org/{orcid_id}") if orcid_id else URIRef(uri)

# Function to handle person deduplication
def get_person_id(g, person_node):
    given_name = g.value(person_node, URIRef("https://schema.org/givenName"))
    family_name = g.value(person_node, URIRef("https://schema.org/familyName"))
    
    if given_name and family_name:
        person_key = (str(given_name), str(family_name))
        if person_key not in person_registry:
            person_registry[person_key] = URIRef(base_iri + get_unique_id())
        return person_registry[person_key]
    
    if person_node not in blank_node_ids:
        blank_node_ids[person_node] = URIRef(base_iri + get_unique_id())
    return blank_node_ids[person_node]

# Function to handle organization deduplication
def get_organization_id(g, org_node):
    org_name = g.value(org_node, URIRef("https://schema.org/name"))
    
    if org_name:
        org_key = str(org_name)
        if org_key not in organization_registry:
            organization_registry[org_key] = URIRef(base_iri + get_unique_id())
        return organization_registry[org_key]
    
    if org_node not in blank_node_ids:
        blank_node_ids[org_node] = URIRef(base_iri + get_unique_id())
    return blank_node_ids[org_node]

# Process each year directory
for year in os.listdir(input_dir): #["2025"]:
    year_path = os.path.join(input_dir, year)
    if not os.path.isdir(year_path) or not year.isdigit():
        continue  # Skip non-year folders
    
    # Create a named graph for the year
    named_graph_iri = f"{base_iri}{year}/"
    g = Graph(identifier=URIRef(named_graph_iri))
    
    # Find all JSON-LD files in YEAR/MONTH/*
    for month in os.listdir(year_path):
        month_path = os.path.join(year_path, month)
        if not os.path.isdir(month_path):
            continue  # Skip if not a directory
        
        jsonld_files = glob.glob(os.path.join(month_path, "*.jsonld"))
        for jsonld_file in jsonld_files:
            #print(f"Processing {jsonld_file} into graph {named_graph_iri}")
            temp_graph = Graph()
            #temp_graph.parse(jsonld_file, format="json-ld")
            try:
                temp_graph.parse(jsonld_file, format="json-ld")
            except Exception as e:
                print(f"Skipping {jsonld_file} due to parsing error: {e}")
                continue

            
            # Replace file-based IRIs with example.com base
            for subj, pred, obj in temp_graph:
                if isinstance(subj, URIRef):
                    subj = URIRef(str(subj).replace("file:///" + os.path.abspath(input_dir).replace("\\", "/"), base_iri[:-1]))
                elif isinstance(subj, BNode):
                    if (temp_graph.value(subj, URIRef("https://schema.org/givenName")) and temp_graph.value(subj, URIRef("https://schema.org/familyName"))):
                        subj = get_person_id(temp_graph, subj)
                    elif temp_graph.value(subj, URIRef("https://schema.org/name")):
                        subj = get_organization_id(temp_graph, subj)
                    else:
                        if subj not in blank_node_ids:
                            blank_node_ids[subj] = URIRef(base_iri + get_unique_id())
                        subj = blank_node_ids[subj]
                
                if isinstance(obj, URIRef):
                    obj = URIRef(str(obj).replace("file:///" + os.path.abspath(input_dir).replace("\\", "/"), base_iri[:-1]))
                elif isinstance(obj, BNode):
                    if (temp_graph.value(obj, URIRef("https://schema.org/givenName")) and temp_graph.value(obj, URIRef("https://schema.org/familyName"))):
                        obj = get_person_id(temp_graph, obj)
                    elif temp_graph.value(obj, URIRef("https://schema.org/name")):
                        obj = get_organization_id(temp_graph, obj)
                    else:
                        if obj not in blank_node_ids:
                            blank_node_ids[obj] = URIRef(base_iri + get_unique_id())
                        obj = blank_node_ids[obj]
                
                g.add((subj, pred, obj))

            #print("file:///C:/Users/eno/Documents/Git_repo/ebrahimnorouzi_github/chemotion-kg/data/2014/05/0000-0003-4845-3191".replace("file:///" + os.path.abspath(input_dir).replace("\\", "/"), base_iri[:-1]))
            #for i, (subj, pred, obj) in enumerate(g):
                #print(f"{subj} {pred} {obj}")
            #exit()
    
    # Save the year's graph in output/YEAR.n3
    output_file = os.path.join(output_dir, f"{year}.n3")
    g.serialize(destination=output_file, format="nt")  # Save in N-Triples format
    print(f"Saved {output_file}")

print("Conversion complete!")
