import json
from tqdm import tqdm

class ChordBassDatasetTokenizer():
    def __init__(self, data, tokenizer, max_length):
        self.tokenized = []

        print("Preparing chord-bass dataset")

        pbar = tqdm(data)
        for item in pbar:
            
            # Parse the JSON string
            parsed_data = json.loads(item)

            chord_sequence = parsed_data["CHORD"]["value"]
            bass_sequence = parsed_data["BASS"]["value"]

            # Tokenize inputs and outputs with truncation and padding
            tokenized = tokenizer(
                chord_sequence,
                text_target=bass_sequence,
                truncation=True,       # Ensures inputs/outputs are truncated to the model's max length
                # padding="longest"
                padding="max_length",  # Pads all sequences to the model's max length
                max_length=max_length
            )

            self.tokenized.append(tokenized)

    def __len__(self):
        return len(self.tokenized)

    def __getitem__(self, idx):
        return self.tokenized[idx]
        