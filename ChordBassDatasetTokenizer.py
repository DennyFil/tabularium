import json
from tqdm import tqdm

class ChordBassDatasetTokenizer():
    def __init__(self, data, tokenizer, max_length):
        self.tokenized = []

        action_str = "Preparing tokenized chord-bass dataset"
        print(f"START {action_str}")

        pbar = tqdm(data)
        for item in pbar:
            
            # Parse the JSON string
            parsed_data = json.loads(item)

            chord_sequence = parsed_data["CHORD"]["value"]
            bass_sequence = parsed_data["BASS"]["value"]
            input_sequence = chord_sequence + '/////' + bass_sequence

            # Tokenize inputs and outputs with truncation and padding
            tokenized = tokenizer(
                input_sequence,
                # chord_sequence,
                # text_target=bass_sequence,
                truncation=True,       # Ensures inputs/outputs are truncated to the model's max length
                # padding="longest"
                padding="max_length",  # Pads all sequences to the model's max length
                max_length=max_length
            )

            self.tokenized.append(tokenized)

        print(f"END {action_str}")

    def __len__(self):
        return len(self.tokenized)

    def __getitem__(self, idx):
        return self.tokenized[idx]
        