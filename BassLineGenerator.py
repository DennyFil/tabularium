class BassLineGenerator:

    ## TDB: generate bass line with the model, temporary adding back the same notes
    def generate(self, model, tokenizer, chord_sequence):
        
        inputs = tokenizer(chord_sequence, return_tensors="pt", max_length=128, truncation=True, padding="max_length")
        outputs = model.generate(inputs["input_ids"], max_length=128, num_beams=5, early_stopping=True)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
