import sys
import os
import time
from pathlib import Path
from os.path import join
from tqdm import tqdm
from TransformerModel import TransformerModel
from ModelConfigFactory import build_model_config

if len(sys.argv) <= 1:
    print('Please submit model name as first argument')
    sys.exit(0)

if len(sys.argv) <= 2:
    print('Please submit path to prepared dataset directory as second argument')
    sys.exit(0)

if len(sys.argv) <= 3:
    print('Please submit path to trained model directory as third argument')
    sys.exit(0)

model_name = sys.argv[1]
model_config = build_model_config(model_name)
validation_data_path_str = sys.argv[2]

if not os.path.exists(validation_data_path_str):
    print(f"Validation dataset path {validation_data_path_str} does not exist")
    sys.exit(0)

model_path_str = sys.argv[3]
if not os.path.exists(model_path_str):
    print(f"Trained model path {model_path_str} does not exist")
    sys.exit(0)

training_files_stats_file_name = 'files_used_training.txt'
training_files_stats_path_str = model_path_str + '/' + training_files_stats_file_name
if not os.path.exists(training_files_stats_path_str):
    print(f"Trained model folder should contain {training_files_stats_file_name}")
    sys.exit(0)

if len(sys.argv) > 3:
    nb_files_max = int(sys.argv[4])
    print(f"Maximum number of files to load set to {nb_files_max}")
    
print(f"Reading dataset from {validation_data_path_str}")
validation_data_path = Path(validation_data_path_str)
file_names = validation_data_path.rglob('*.mid.txt')
file_paths = [join(validation_data_path_str, f) for f in file_names]

file_paths = file_paths[:nb_files_max]

def read_data(file_paths, action_type):
    f_used = open(f"{model_path_str}/files_used_{action_type}.txt", "w")
    
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

print(f"Reading data files for validation")
validation_data = read_data(file_paths, "validation")

print(f"Reading training dataset from {training_files_stats_path_str}")
training_file_paths = []
with open(training_files_stats_path_str, 'r') as file:
    # Read each line in the file
    for line in file:
        training_file_paths.append(line.strip())

print(f"Reading training data files for validation")
training_data = read_data(training_file_paths, "training_for_validation")

print(f"START Building model")
model_build_start = time.time()
model = TransformerModel(model_config, None, model_path_str)
model_build_end = time.time()
print(f"END Building model in {model_build_end - model_build_start} seconds")

# Validating
print(f"Validating model on {len(file_paths)} files")
evaluation_results = model.validate(validation_data, training_data)

print(evaluation_results)

print("END training")
