from ModelBase import ModelBase
from Constants import chord_bass_split

from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from ChordBassDatasetTokenizer import ChordBassDatasetTokenizer

class TransformerModel(ModelBase):
    def __init__(self, model_config, model_save_dir_path, model_restore_dir_path):

        self.device_map = 'cuda'
        self.model_name = model_config["name"]
        self.max_length = model_config["max_nb_tokens"]

        super().__init__(model_save_dir_path, model_restore_dir_path)

        self.training_args = TrainingArguments(
            output_dir=self.model_save_dir_path,
            num_train_epochs=3,
            per_device_train_batch_size=2,
            logging_steps=10,
            save_steps=5000,
            #     learning_rate=5e-5,
            #     weight_decay=0.01,
            #     evaluation_strategy="steps",
            #     eval_steps=10,
            #     per_device_eval_batch_size=4
        )
        
    def load_model(self):
        # Load the pre-trained model
        self.model = AutoModelForCausalLM.from_pretrained(self.model_restore_dir_path)
        # Load the tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_restore_dir_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        print(f"Model loaded from {self.model_restore_dir_path}")

    def build_model(self):
        # Instantiate model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name, device_map = self.device_map)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
    def train(self, training_data):

        self.training_inputs = ChordBassDatasetTokenizer(training_data, self.tokenizer, self.max_length)

        print("Building model trainer")
        self.trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.training_inputs,
            processing_class=self.tokenizer,
        )

        print("Launch train using trainer")
        self.trainer.train()
        print("Trainer terminated")

    def save(self):
        self.trainer.save_model(self.model_save_dir_path)

    def validate(self, validation_data):

        validation_inputs = ChordBassDatasetTokenizer(validation_data, self.tokenizer, self.max_length)

        self.training_args.output_dir = self.model_restore_dir_path + "/validation_results"
        
        evaluator = Trainer(
            model=self.model,
            args=self.training_args,
            eval_dataset=validation_inputs,
            processing_class=self.tokenizer,
        )

        return evaluator.evaluate()

    def generate_output(self, inputs):
        
        tokenized_inputs = self.tokenizer(
                inputs, return_tensors="pt",
                truncation=True,
                padding="max_length",
                max_length=self.max_length
            )
        
        outputs = self.model.generate(tokenized_inputs["input_ids"], attention_mask=tokenized_inputs["attention_mask"])
        generated_text = self.tokenizer.decode(outputs[0])
        
        print(generated_text)
        
        split_idx_1 = generated_text.find(chord_bass_split)

        split_idx_2 = generated_text.find(chord_bass_split, split_idx_1 + len(chord_bass_split))

        generated_text = generated_text[split_idx_1 + len(chord_bass_split):split_idx_2]
    
        print(generated_text)

        return generated_text
    