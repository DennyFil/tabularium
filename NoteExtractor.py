# Class used to extract chords and bass notes from MIDI data
# Dependencies: pretty_midi
from Chord import Chord
from Note import Note
from Tools import is_bass, is_guitar

class NoteExtractor:

    def extract_chords_and_bass(self, midi_data):

        # Initialize containers for chords and bass notes
        chord_notes = []
        bass_line = []

        for instrument in midi_data.instruments:
            if instrument.is_drum:  # Skip drum tracks
                continue
        
            # Extract notes from the instrument
            notes = list(sorted([Note(note.start, note.pitch) for note in instrument.notes], key=lambda note: note.start))

            # Separate bass notes and chord notes
            if is_bass(instrument):
                bass_line.extend(notes)
            elif is_guitar(instrument):
                # Chord detection can be more complex; here we just collect notes
                chord_notes.extend(notes)
                
        # Group notes played at the same time to form chords
        chords = self.__group_chords(chord_notes)

        # Remove duplicate chords
        unique_chords = sorted(set(chords), key=lambda c: c.start)
        
        return unique_chords, bass_line
        
    def __group_chords(self, notes, time_threshold=0.1):
        """
        Group notes played within a time threshold as chords.
        """
        if len(notes) < 1:
            return []

        first_note = notes[0]
        current_chord = self.__build_chord(first_note)
        chords = [current_chord]

        for note in notes[1:]:
            if abs(note.start - current_chord.start) < time_threshold:
                current_chord.addNote(note)
            else:
                # new chord
                current_chord = self.__build_chord(note)
                chords.append(current_chord)
            
        return list(filter(lambda chord: len(chord.notes) > 2, chords)) # only consider chords having 3 notes
    
    def __build_chord(self, note):
        chord = Chord(note.start, [note])
        return chord

