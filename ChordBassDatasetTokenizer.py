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
            
            # Clone input_ids for labels (causal LM requires this)
            tokenized["labels"] = tokenized["input_ids"][:]
            # Replace padding tokens in labels with -100
            if tokenizer.pad_token_id is not None:
                tokenized["labels"] = [
                    token if token != tokenizer.pad_token_id else -100
                    for token in tokenized["labels"]
                ]

            self.tokenized.append(tokenized)

        print(f"END {action_str}")

    def __len__(self):
        return len(self.tokenized)

    def __getitem__(self, idx):
        return self.tokenized[idx]
        