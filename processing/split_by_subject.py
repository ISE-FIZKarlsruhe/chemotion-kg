import sys
import os
from rdflib import Graph

# Arguments: input_file, output_dir, number_of_splits
if len(sys.argv) != 4:
    print("Usage: python split_by_subject.py input_file.n3 output_dir 10")
    sys.exit(1)

input_file = sys.argv[1]
output_dir = sys.argv[2]
num_splits = int(sys.argv[3])

# Load graph
print(f"Loading RDF graph from {input_file} ...")
g = Graph()
g.parse(input_file, format="n3")

# Group triples by subject
print("Grouping triples by subject ...")
from collections import defaultdict
subject_groups = defaultdict(list)
for s, p, o in g:
    subject_groups[s].append((s, p, o))

# Distribute subject groups into N buckets
print(f"Distributing subjects into {num_splits} chunks ...")
buckets = [Graph() for _ in range(num_splits)]
for i, (subject, triples) in enumerate(subject_groups.items()):
    bucket_index = i % num_splits
    for triple in triples:
        buckets[bucket_index].add(triple)

# Write out each bucket
os.makedirs(output_dir, exist_ok=True)
for i, bucket in enumerate(buckets):
    out_path = os.path.join(output_dir, f"chunk_{i}.n3")
    print(f"Writing chunk {i} with {len(bucket)} triples to {out_path}")
    bucket.serialize(destination=out_path, format="n3")

print("✅ Done.")
