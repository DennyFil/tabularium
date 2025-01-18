
def build_model_config(model_name): 
	# Return an object with model config based on its name
	if model_name == "llama":
		return {
			"name": "meta-llama/Llama-3.2-1B",
			"max_nb_tokens": 128 #128000
        }
		
	if model_name == "gpt":
		return {
			"name": "gpt2",
			"max_nb_tokens": 128 #128000
        }
		
	if model_name == "qwen":
		return {
			"name": "Qwen/Qwen1.5-0.5B",
			"max_nb_tokens": 128 #128000
        }
	
	raise Exception("Unsupported model")
