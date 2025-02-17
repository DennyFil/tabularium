# Class used to manage a MIDI note which is a combination of start and a pitch
import pretty_midi

class Note:
    def __init__(self, start, pitch):
        self.pitch = pitch
        self.start = start
        self.name = pretty_midi.note_number_to_name(self.pitch)
        
    def __iter__(self):
        # Allow iteration over the notes in the chord
        return iter([self])

    def __str__(self):
        return f"name: {self.name}, start: {self.start}, pitch: {self.pitch}"

    def __eq__(self, other):
        return self.pitch==other.pitch and self.start==other.start
    
    def __hash__(self):
        return hash((self.pitch, self.start))
    