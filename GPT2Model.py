from ModelBase import ModelBase

from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from TorchChordBassDataset import TorchChordBassDataset

class GPT2Model(ModelBase):
    def __init__(self, model_save_dir_path, model_restore_dir_path):
        self.model_name = "gpt2"  # Replace with a GPT-4 equivalent if accessible

        super().__init__(model_save_dir_path, model_restore_dir_path)
        self.tokenized_max_length = 128

        self.training_args = TrainingArguments(
            output_dir=self.model_save_dir_path,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            logging_steps=10,
            #     learning_rate=5e-5,
            #     weight_decay=0.01,
            #     evaluation_strategy="steps",
            #     eval_steps=10,
            #     per_device_eval_batch_size=4
        )

        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def load_model(self):
        # Load the pre-trained model
        self.model = GPT2LMHeadModel.from_pretrained(self.model_restore_dir_path)
        print(f"Model loaded from {self.model_restore_dir_path}")
        
        # Load the tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_restore_dir_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def build_model(self):
        # Instantiate and configure model
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        
    def train(self, training_data):

        self.training_inputs = TorchChordBassDataset(training_data, self.tokenizer, self.tokenized_max_length)

        self.trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.training_inputs,
            processing_class=self.tokenizer,
        )

        self.trainer.train()

    def save(self):
        self.trainer.save_model(self.model_save_dir_path)

    def validate(self, validation_data):
        validation_inputs = TorchChordBassDataset(validation_data, self.tokenizer, self.tokenized_max_length)

        evaluator = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.training_inputs,
            eval_dataset=validation_inputs,
            processing_class=self.tokenizer,
        )

        return evaluator.evaluate()

    def generate_output(self, inputs):
        tokenized_inputs = self.tokenizer(inputs, return_tensors="pt", max_length=self.tokenized_max_length, truncation=True, padding="max_length")
        outputs = self.model.generate(tokenized_inputs["input_ids"], max_length=self.tokenized_max_length, num_beams=5, early_stopping=True)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
