import os
import glob
import re
import time
from rdflib import Graph, URIRef, BNode, RDF

# Define base directories
input_dir = "data"
output_dir = "output"
base_iri = "https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/resources/"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Dictionary to store unique IDs for blank nodes
blank_node_ids = {}
blank_counter = 0  # Ensures unique IDs across the graph

# Dictionary to track unique persons, organizations, and datasets
person_registry = {}
organization_registry = {}
dataset_registry = {}

def get_unique_id():
    """Generate a unique identifier."""
    global blank_counter
    blank_counter += 1
    return str(int(time.time() * 1000)) + f"_{blank_counter}"

def extract_orcid_id(uri):
    """Extract ORCID ID from a full path."""
    match = re.search(r"(\d{4}-\d{4}-\d{4}-\d{3}[\dX])$", uri)
    return match.group(1) if match else None

def convert_to_orcid(uri):
    """Convert extracted ORCID ID to a proper ORCID URI."""
    orcid_id = extract_orcid_id(uri)
    return URIRef(f"https://orcid.org/{orcid_id}") if orcid_id else URIRef(uri)

def get_person_id(g, person_node, year, month):
    """Handle person deduplication and assign a unique IRI."""
    given_name = g.value(person_node, URIRef("https://schema.org/givenName"))
    family_name = g.value(person_node, URIRef("https://schema.org/familyName"))
    
    if given_name and family_name:
        person_key = (str(given_name), str(family_name))
        if person_key not in person_registry:
            person_registry[person_key] = URIRef(f"{base_iri}{year}/{month}/person/{get_unique_id()}")
        return person_registry[person_key]
    
    if person_node not in blank_node_ids:
        blank_node_ids[person_node] = URIRef(f"{base_iri}{year}/{month}/person/{get_unique_id()}")
    return blank_node_ids[person_node]

def get_organization_id(g, org_node, year, month):
    """Handle organization deduplication and assign a unique IRI."""
    org_name = g.value(org_node, URIRef("https://schema.org/name"))
    
    if org_name:
        org_key = str(org_name)
        if org_key not in organization_registry:
            organization_registry[org_key] = URIRef(f"{base_iri}{year}/{month}/organization/{get_unique_id()}")
        return organization_registry[org_key]
    
    if org_node not in blank_node_ids:
        blank_node_ids[org_node] = URIRef(f"{base_iri}{year}/{month}/organization/{get_unique_id()}")
    return blank_node_ids[org_node]

# Create a global graph
global_graph = Graph()

# Process each year directory
for year in os.listdir(input_dir):
    year_path = os.path.join(input_dir, year)
    if not os.path.isdir(year_path) or not year.isdigit():
        continue  # Skip non-year folders
    
    # Process each month
    for month in os.listdir(year_path):
        month_path = os.path.join(year_path, month)
        if not os.path.isdir(month_path):
            continue  # Skip if not a directory
        
        jsonld_files = glob.glob(os.path.join(month_path, "*.jsonld"))
        for jsonld_file in jsonld_files:
            temp_graph = Graph()
            try:
                temp_graph.parse(jsonld_file, format="json-ld")
            except Exception as e:
                print(f"Skipping {jsonld_file} due to parsing error: {e}")
                continue

            # Replace file-based IRIs with example.com base and ensure correct deduplication
            for subj, pred, obj in temp_graph:
                if isinstance(subj, URIRef):
                    subj = URIRef(str(subj).replace("file:///" + os.path.abspath(input_dir).replace("\\", "/"), base_iri[:-1]))
                elif isinstance(subj, BNode):
                    if temp_graph.value(subj, URIRef("https://schema.org/givenName")) and temp_graph.value(subj, URIRef("https://schema.org/familyName")):
                        subj = get_person_id(temp_graph, subj, year, month)
                    elif temp_graph.value(subj, URIRef("https://schema.org/name")):
                        subj = get_organization_id(temp_graph, subj, year, month)
                    else:
                        if subj not in blank_node_ids:
                            blank_node_ids[subj] = URIRef(f"{base_iri}{year}/{month}/blank/{get_unique_id()}")
                        subj = blank_node_ids[subj]
                
                if isinstance(obj, URIRef):
                    obj = URIRef(str(obj).replace("file:///" + os.path.abspath(input_dir).replace("\\", "/"), base_iri[:-1]))
                elif isinstance(obj, BNode):
                    if temp_graph.value(obj, URIRef("https://schema.org/givenName")) and temp_graph.value(obj, URIRef("https://schema.org/familyName")):
                        obj = get_person_id(temp_graph, obj, year, month)
                    elif temp_graph.value(obj, URIRef("https://schema.org/name")):
                        obj = get_organization_id(temp_graph, obj, year, month)
                    else:
                        if obj not in blank_node_ids:
                            blank_node_ids[obj] = URIRef(f"{base_iri}{year}/{month}/blank/{get_unique_id()}")
                        obj = blank_node_ids[obj]

                global_graph.add((subj, pred, obj))

# Save the global graph in one file
output_file = os.path.join(output_dir, "merged_data.n3")
global_graph.serialize(destination=output_file, format="nt")  # Save in N-Triples format
global_graph.serialize(destination=os.path.join(output_dir, "merged_data.ttl"), format="turtle") 

# Calculate statistics
num_triples = len(global_graph)
num_instances = len(set(global_graph.subjects()))
num_persons = len(person_registry)
num_organizations = len(organization_registry)
num_datasets = len(set(global_graph.subjects(RDF.type, URIRef("https://schema.org/Dataset"))))

# Print statistics
print("Statistics:")
print(f"Total triples: {num_triples}")
print(f"Total instances: {num_instances}")
print(f"Total persons: {num_persons}")
print(f"Total organizations: {num_organizations}")
print(f"Total datasets: {num_datasets}")

print("Conversion complete!")
