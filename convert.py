from rdflib import Graph

# Load the N3 file
input_file = "data/chemotion-kg.n3"
output_file = "data/chemotion-kg.ttl"

# Create an RDF graph
g = Graph()

# Parse the N3 file
g.parse(input_file, format="n3")

# Serialize and save as TTL
g.serialize(destination=output_file, format="turtle")

print(f"Conversion complete: {output_file}")
