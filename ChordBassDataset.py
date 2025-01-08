import json
import torch
from torch.utils.data import Dataset

class ChordBassDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=128):
        self.inputs = []
        self.targets = []
        self.tokenizer = tokenizer

        for item in data:
            
            # Parse the JSON string
            parsed_data = json.loads(item)

            chord = parsed_data["CHORD"]
            bass = parsed_data["BASS"]

            chord_sequence = json.dumps(chord)
            bass_sequence = json.dumps(bass)

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
    