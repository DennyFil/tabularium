class ModelBase:
    def __init__(self, model_save_dir_path, model_restore_dir_path):
        self.model_save_dir_path = model_save_dir_path
        self.model_restore_dir_path = model_restore_dir_path

        if model_restore_dir_path:
            print(f"Loading model from {model_restore_dir_path}")
            self.load_model()
        else:
            self.build_model()

    def build_model(self):
        print("train not implemented")

    def load_model(self):
        print("load_model not implemented")

    def train(self):
        print("train not implemented")

    def validate(self):
        print("validate not implemented")

    def save(self):
        print("save not implemented")

    def generate_output(self):
        print("generate_output not implemented")
