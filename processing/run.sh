#!/bin/bash

INPUT="merged_data.n3"
CHUNK_DIR="chunks_by_subject" #"chunks"
OUT_DIR="outputs"
LOG_DIR="logs"
SPLITS=100
FINAL_OUTPUT="output_merged.n3"

mkdir -p "$CHUNK_DIR" "$OUT_DIR" "$LOG_DIR"

# Step 1: Split input into $SPLITS chunks
echo "Step 1: Split input into $SPLITS chunks"
#python3 split_by_subject.py "merged_data.n3" "$CHUNK_DIR" $SPLITS
#split -n l/$SPLITS "$INPUT" "$CHUNK_DIR/chunk_"

# Step 2: Run process_rdf.py on each chunk in parallel
for file in $CHUNK_DIR/chunk_*; do
    # Extract just the filename (e.g., chunk_5.n3)
    filename=$(basename "$file")

    # Extract number from chunk_5.n3 → 5
    i="${filename#chunk_}"
    i="${i%.n3}"

    echo "🔄 Running job $i on $file ..."
    
    python3 all-nfdicore.py "$file" "$OUT_DIR/out_$i.n3" > "$LOG_DIR/job_$i.log" 2>&1 &
done

# Step 3: Wait for all jobs to finish
echo "⏳ Waiting for all jobs to finish ..."
wait
echo "✅ All jobs done."

# Step 4: Merge all output files
rm -f "$FINAL_OUTPUT"

cat outputs/out_*.n3 > output_merged.n3 
#cat "$OUT_DIR"/out_*.n3 > "$FINAL_OUTPUT"

echo "✅ All done! Output saved to $FINAL_OUTPUT"
