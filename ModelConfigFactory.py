
def build_model_config(model_name): 
	# Return an object with model config based on its name
	if model_name == "llama":
		return {
			"name": "meta-llama/Llama-3.2-1B",
			"max_nb_tokens": 128 #128000
        }
	
	# "Qwen/Qwen1.5-0.5B"
	
	raise Exception("Unsupported model")
