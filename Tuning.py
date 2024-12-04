# Class used to manage a string instrument tuning
class Tuning:
    def __init__(self, idx, name, pitch):
        self.idx = idx
        self.name = name
        self.pitch = pitch

    def __str__(self):
        return f"idx: {self.idx}, name: {self.name}, pitch: {self.pitch}"
    