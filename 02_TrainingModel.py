import sys
import os
import math
from pathlib import Path
from os.path import join
from tqdm import tqdm
import ast
import json
import re

if len(sys.argv) <= 1:
    print('Please submit path to prepared data as first argument')
    sys.exit(0)

training_data_path_str = sys.argv[1]

if not os.path.exists(training_data_path_str):
    print(f"Path {training_data_path_str} does not exist")
    sys.exit(0)
    
# Read training data
print(f"Reading dataset from {training_data_path_str}")
training_data_path = Path(training_data_path_str)
file_names = training_data_path.rglob('*1cd8c4da2f70f11b69e4afc8d9d49.mid.txt')
file_paths = [join(training_data_path_str, f) for f in file_names]
nb_available_files = len(file_paths)
print(f"Reading {nb_available_files} files")

# Split data into training and validation dataset
nb_training_files = math.floor(0.75*nb_available_files)
file_paths_training = file_paths[:nb_training_files]
print(f"Training on {len(file_paths_training)} files")
file_paths_validation = file_paths[nb_training_files+1:]
print(f"Validating on {len(file_paths_validation)} files")

file_paths_training = file_paths[:10]

# Instantiate and configure model

# Traing model
training_data = []
pbar = tqdm(file_paths_training)
for fp in pbar:
    try:
        with open(fp, "r") as file:
            content = file.read()
            
        # Parse the JSON string
        parsed_data = json.loads(content)

        chord = parsed_data["CHORD"]
        bass = parsed_data["BASS"]
        

    except Exception as e:
        print(f"Failed to load {fp}")
        print(e)
        continue

# Print the data

# Plot errors

# Save model for future use