# Class used to manage a MIDI chord which is a list of all notes
from music21 import chord, pitch

class Chord:
    def __init__(self, start, notes):
        self.start = start
        self.notes = sorted(notes, key=lambda note: note.pitch) # order by pitch in order for the tonic to be the lowest
        self.name = self.__get_name()

    def __iter__(self):
        # Allow iteration over the notes in the chord
        return iter(self.notes)
    
    def __get_name(self):
        
        pitches = [pitch.Pitch(n.pitch) for n in self.notes]
        ch = chord.Chord(pitches)

        try:
            root = ch.root()
            quality = ch.quality  # Get the chord quality (e.g., major, minor)
            return f"{root.name}{'m' if quality == 'minor' else ''}"
        except Exception as e:
            return ch.pitchedCommonName  # Fall back to a generic name if simplification fails

    def __eq__(self, other):
        return self.__get_name()==other.__get_name() and self.start==other.start
    
    def __hash__(self):
        return hash((self.__get_name(), self.start))
        