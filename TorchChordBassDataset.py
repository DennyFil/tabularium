import json
import torch
from tqdm import tqdm
from torch.utils.data import Dataset

class TorchChordBassDataset(Dataset):
    def __init__(self, data, tokenizer, max_length):
        self.inputs = []
        self.targets = []
        self.tokenizer = tokenizer

        print("Preparing chord-bass dataset")

        pbar = tqdm(data)
        for item in pbar:
            
            # Parse the JSON string
            parsed_data = json.loads(item)

            chord_sequence = parsed_data["CHORD"]["value"]
            bass_sequence = parsed_data["BASS"]["value"]

            # Tokenize inputs and targets
            input_encoded = tokenizer(chord_sequence, max_length=max_length, truncation=True, padding="max_length")
            target_encoded = tokenizer(bass_sequence, max_length=max_length, truncation=True, padding="max_length")

            self.inputs.append(input_encoded)
            self.targets.append(target_encoded)

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        input_ids = torch.tensor(self.inputs[idx]["input_ids"])
        attention_mask = torch.tensor(self.inputs[idx]["attention_mask"])
        target_ids = torch.tensor(self.targets[idx]["input_ids"])
        return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": target_ids}
    