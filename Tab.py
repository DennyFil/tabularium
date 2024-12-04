# Class used to represent a string instrument tab with related note
class Tab:
    def __init__(self, tuning, fret_idx, note):
        self.tuning = tuning
        self.fret_idx = fret_idx
        self.note = note

    def __str__(self):
        return f"tuning: {self.tuning.name}, fret: {self.fret_idx}, pitch: {self.note.pitch}"
        