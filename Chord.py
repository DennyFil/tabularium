# Class used to manage a MIDI chord which is a list of all notes
from Note import Note
from music21 import chord

class Chord:
    def __init__(self, start, notes):
        self.start = start
        self.notes = notes
        self.__set_chord_name()

    def addNote(self, start, pitch):
        note = Note(start, pitch)
        if not any(n.start == start and n.pitch == pitch for n in self.notes):
            self.notes.append(note)
            self.__set_chord_name()

    def __iter__(self):
        # Allow iteration over the notes in the chord
        return iter(self.notes)
    
    def __set_chord_name(self):
        pitches = [n.pitch for n in self.notes]
        self.name = chord.Chord(pitches).pitchedCommonName
    