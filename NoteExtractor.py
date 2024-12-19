# Class used to extract chords and bass notes from MIDI data
# Dependencies: pretty_midi
from Chord import Chord
from Note import Note
from Exceptions import ChordException, BassException
from Tools import is_bass, is_guitar

class NoteExtractor:

    def extract_chords_and_bass(self, midi_data):

        # Initialize containers for chords and bass notes
        chord_notes = []
        bass_line = []

        for instrument in midi_data.instruments:
            if instrument.is_drum:  # Skip drum tracks
                continue

            notes = self.__build_notes(instrument.notes)

            # Separate bass notes and chord notes
            if is_bass(instrument):
                bass_line.extend(notes)
            elif is_guitar(instrument):
                # Chord detection can be more complex; here we just collect notes
                chord_notes.extend(notes)
        
        if(len(bass_line) == 0):
            raise BassException("Missing bass")
        
        # Group notes played at the same time to form chords
        chords = self.__group_chords(chord_notes)

        if(len(chords) == 0):
            raise ChordException("Missing chords")

        # Remove duplicate chords and bass notes
        return sorted(set(chords), key=lambda c: c.start), sorted(set(bass_line), key=lambda c: c.start)
        
    def __group_chords(self, input_notes, time_threshold=0.1):
        """
        Group notes played within a time threshold as chords.
        """
        if len(input_notes) < 1:
            return []

        notes = sorted(input_notes, key=lambda note: note.start)
 
        chords = []
        idx = 0
        while idx < len(notes):
            current_note = notes[idx]
            chord_notes = set(list(filter(lambda note: abs(note.start - current_note.start) < time_threshold, notes)))
            nb_chord_notes = len(chord_notes)
            if nb_chord_notes > 2: # only consider chords having 3 notes
                current_chord = Chord(current_note.start, chord_notes)
                chords.append(current_chord)

            idx += nb_chord_notes

        return chords
    
    def __build_notes(self, input_notes):
        return [Note(note.start, note.pitch) for note in input_notes]
