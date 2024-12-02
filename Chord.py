# Class used to manage a MIDI chord which is a list of all notes
from Note import Note

class Chord:
    def __init__(self, start, notes):
        self.start = start
        self.notes = notes

    def addNote(self, start, pitch):
        note = Note(start, pitch)
        self.notes.append(note)

    def __iter__(self):
        # Allow iteration over the notes in the chord
        return iter(self.notes)