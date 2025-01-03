import sys
import os
import math
from pathlib import Path
from os.path import join
from tqdm import tqdm
import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments

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
file_names = training_data_path.rglob('*.mid.txt')
file_paths = [join(training_data_path_str, f) for f in file_names]
nb_available_files = len(file_paths)
print(f"Reading {nb_available_files} files")

# Split data into training and validation dataset
nb_training_files = math.floor(0.75*nb_available_files)
file_paths_training = file_paths[:nb_training_files]
file_paths_validation = file_paths[nb_training_files+1:]

def read_data(file_paths):
    data = []
    pbar = tqdm(file_paths)
    for fp in pbar:
        try:
            with open(fp, "r") as file:
                content = file.read()
                
            # Parse the JSON string
            parsed_data = json.loads(content)

            data.append(parsed_data)
            # chord = parsed_data["CHORD"]
            # bass = parsed_data["BASS"]
            
        except Exception as e:
            print(f"Failed to load {fp}")
            print(e)
            continue

    return data

# Parsing tokenized data and preparing model inputs
print(f"Training on {len(file_paths_training)} files")
training_data = read_data(file_paths_training)

# Instantiate and configure model
model_name = "gpt2"  # Replace with a GPT-4 equivalent if accessible
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name)

# training_inputs = tokenizer(training_data, return_tensors="pt", padding=True, truncation=True)

# # Traing model
# training_args = TrainingArguments(
#     output_dir="./gpt_fine_tuned",
#     num_train_epochs=3,
#     per_device_train_batch_size=4,
#     save_steps=10_000,
#     save_total_limit=2,
# )
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=training_inputs,
#     tokenizer=tokenizer,
# )
# trainer.train()

# Validating
print(f"Validating on {len(file_paths_validation)} files")
validation_data = read_data(file_paths_validation)

# validation_inputs = tokenizer(validation_data, return_tensors="pt", padding=True, truncation=True)
# evaluator = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=training_inputs,
#     eval_dataset=validation_inputs,
#     tokenizer=tokenizer,
# )

# evaluation_results = evaluator.evaluate()
# print(evaluation_results)

# Print the data

# Plot errors

# Save model for future use
