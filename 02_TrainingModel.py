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
    print('Please submit path for checkpoint and model saving directory as third argument')
    sys.exit(0)

model_name = sys.argv[1]
model_config = build_model_config(model_name)
training_data_path_str = sys.argv[2]

if not os.path.exists(training_data_path_str):
    print(f"Training dataset path {training_data_path_str} does not exist")
    sys.exit(0)

model_save_dir_path = sys.argv[3]

if not os.path.exists(model_save_dir_path):
    print(f"Model saving path {model_save_dir_path} does not exist")
    sys.exit(0)

if len(sys.argv) > 4:
    nb_files_max = int(sys.argv[4])
    print(f"Maximum number of files to load set to {nb_files_max}")

model_to_restore_path_str = ""
if len(sys.argv) > 5:
    model_to_restore_path_str = sys.argv[5]

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

if nb_files_max > 0:
    file_paths = file_paths[:nb_files_max]

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
training_data = read_data(file_paths, "training")

print(f"START Building model")
model_build_start = time.time()
model = TransformerModel(model_config, model_save_dir_path, model_to_restore_path_str)
model_build_end = time.time()
print(f"END Building model in {model_build_end - model_build_start} seconds")

print(f"START Training model on {len(file_paths)} files")
model_training_start = time.time()
model.train(training_data)
model_training_end = time.time()
print(f"END Training model in {model_training_end - model_training_start} seconds")

print(f"Saving model to {model_save_dir_path}")
model.save()

print("END training")
