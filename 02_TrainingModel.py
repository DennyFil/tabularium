import sys
import os
import math
import time
from pathlib import Path
from os.path import join
from tqdm import tqdm
from TansformerModel import TansformerModel
from ModelConfigFactory import build_model_config

if len(sys.argv) <= 1:
    print('Please submit path to prepared data directory as first argument')
    sys.exit(0)

if len(sys.argv) <= 2:
    print('Please submit path for checkpoint and model saving directory as second argument')
    sys.exit(0)

training_data_path_str = sys.argv[1]

if not os.path.exists(training_data_path_str):
    print(f"Training data path {training_data_path_str} does not exist")
    sys.exit(0)

model_save_dir_path = sys.argv[2]

if not os.path.exists(model_save_dir_path):
    print(f"Model saving path {model_save_dir_path} does not exist")
    sys.exit(0)

if len(sys.argv) > 3:
    nb_files_max = int(sys.argv[3])
    print(f"Maximum number of files to load set to {nb_files_max}")

model_to_restore_path_str = ""
if len(sys.argv) > 4:
    model_to_restore_path_str = sys.argv[4]

    if not os.path.exists(model_to_restore_path_str):
        print(f"Model restore path {model_to_restore_path_str} does not exist")
        sys.exit(0)
    
    print(f"Model will be restored from {model_to_restore_path_str}")
    
print("START training")

# Read training data
print(f"Reading dataset from {training_data_path_str}")
training_data_path = Path(training_data_path_str)
file_names = training_data_path.rglob('*.mid.txt')
file_paths = [join(training_data_path_str, f) for f in file_names]

file_paths = file_paths[:nb_files_max]

nb_available_files = len(file_paths)

# Split data into training and validation dataset
nb_training_files = math.floor(0.75*nb_available_files)
file_paths_training = file_paths[:nb_training_files]
file_paths_validation = file_paths[nb_training_files:]

def read_data(file_paths, action_type):
    f_used = open(f"{model_save_dir_path}/files_used_{action_type}.txt", "w")
    
    data = []

    pbar = tqdm(file_paths)
    for fp in pbar:
        
        f_used.write(fp+'\n')

        try:
            with open(fp, "r") as file:
                content = file.read()

            data.append(content)
            
        except Exception as e:
            print(f"Failed to load {fp}")
            print(e)
            continue
        
    f_used.close()

    return data

print(f"Reading data files for training")
training_data = read_data(file_paths_training, "training")

print(f"START Building model")
model_build_start = time.time()
model_config = build_model_config("qwen")
model = TansformerModel(model_config, model_save_dir_path, model_to_restore_path_str)
model_build_end = time.time()
print(f"END Building model in {model_build_end - model_build_start} seconds")

print(f"START Training model on {len(file_paths_training)} files")
model_training_start = time.time()
model.train(training_data)
model_training_end = time.time()
print(f"END Training model in {model_training_end - model_training_start} seconds")

print(f"Saving model to {model_save_dir_path}")
model.save()

print(f"Reading data files for validation")
validation_data = read_data(file_paths_validation, "validation")

# Validating
print(f"Validating model on {len(file_paths_validation)} files")
evaluation_results = model.validate(validation_data)

print(evaluation_results)

print("END training")

# Print the data

# Plot errors

# Save model for future use
