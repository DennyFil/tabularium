# Class used to manage a MIDI chord which is a list of all notes
from music21 import chord

class Chord:
    def __init__(self, start, notes):
        self.start = start
        self.notes = notes
        self.__set_chord_name()

    def addNote(self, note):
        if not any(n.start == note.start and n.pitch == note.pitch for n in self.notes):
            self.notes.append(note)
            self.__set_chord_name()

    def __iter__(self):
        # Allow iteration over the notes in the chord
        return iter(self.notes)
    
    def __set_chord_name(self):
        pitches = [n.pitch for n in self.notes]
        
        ch = chord.Chord(pitches)

        try:
            root = ch.root()
            quality = ch.quality  # Get the chord quality (e.g., major, minor)
            self.name = f"{root.name}{'m' if quality == 'minor' else ''}"
        except Exception as e:
            self.name = ch.pitchedCommonName  # Fall back to a generic name if simplification fails

    def __eq__(self, other):
        return self.name==other.name and self.start==other.start
    
    def __hash__(self):
        return hash((self.name, self.start))
        