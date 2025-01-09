import sys
import os
import math
from pathlib import Path
from os.path import join
from tqdm import tqdm
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from ChordBassDataset import ChordBassDataset

if len(sys.argv) <= 1:
    print('Please submit path to prepared data as first argument')
    sys.exit(0)

if len(sys.argv) <= 2:
    print('Please submit directory name for checkpoint and model saving as second argument')
    sys.exit(0)

training_data_path_str = sys.argv[1]
model_save_dir_name = f"./{sys.argv[2]}"

model_to_restore = ""
if len(sys.argv) > 3:
    model_to_restore = sys.argv[3]

if not os.path.exists(training_data_path_str):
    print(f"Path {training_data_path_str} does not exist")
    sys.exit(0)
    
# Read training data
print(f"Reading dataset from {training_data_path_str}")
training_data_path = Path(training_data_path_str)
file_names = training_data_path.rglob('*.mid.txt')
file_paths = [join(training_data_path_str, f) for f in file_names]

file_paths = file_paths[:1000]

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

            data.append(content)
            
        except Exception as e:
            print(f"Failed to load {fp}")
            print(e)
            continue

    return data

# Parsing tokenized data and preparing model inputs
print(f"Reading training data files")
training_data = read_data(file_paths_training)

# Instantiate and configure model
model_name = "gpt2"  # Replace with a GPT-4 equivalent if accessible
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = GPT2LMHeadModel.from_pretrained(model_name)

training_inputs = ChordBassDataset(training_data, tokenizer)

print(f"Training on {len(file_paths_training)} files")

# Traing model
logging_dir="./logs"
training_args = TrainingArguments(
    output_dir=model_save_dir_name,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    logging_dir=logging_dir,
    logging_steps=10,
#     learning_rate=5e-5,
#     weight_decay=0.01,
#     evaluation_strategy="steps",
#     eval_steps=10,
#     per_device_eval_batch_size=4
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=training_inputs,
    processing_class=tokenizer,
)

trainer.train()

trainer.save_model(model_save_dir_name)

# Validating
print(f"Validating on {len(file_paths_validation)} files")
validation_data = read_data(file_paths_validation)

validation_inputs = ChordBassDataset(validation_data, tokenizer)

evaluator = Trainer(
    model=model,
    args=training_args,
    train_dataset=training_inputs,
    eval_dataset=validation_inputs,
    processing_class=tokenizer,
)

evaluation_results = evaluator.evaluate()
print(evaluation_results)

# Print the data

# Plot errors

# Save model for future use
