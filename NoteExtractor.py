# Class used to extract chords and bass notes from MIDI data
# Dependencies: pretty_midi
from Chord import Chord
from Note import Note

class NoteExtractor:

    def __init__(self, input_bass_note_threshold):
        self.bass_note_threshold = input_bass_note_threshold

    def extract_chords_and_bass(self, midi_data):

        # Initialize containers for chords and bass notes
        chord_notes = []
        bass_line = []

        for instrument in midi_data.instruments:
            if instrument.is_drum:  # Skip drum tracks
                continue

            # Extract notes from the instrument
            notes = sorted(instrument.notes, key=lambda note: note.start)

            # Separate bass notes (lowest pitch) and chord notes
            for note in notes:
                if note.pitch < self.bass_note_threshold:
                    bass_line.append(Note(note.start, note.pitch))
                else:
                    # Chord detection can be more complex; here we just collect notes
                    chord_notes.append(Note(note.start, note.pitch))

        # Group notes played at the same time to form chords
        chords = self.__group_chords(chord_notes)

        return chords, bass_line
        
    def __group_chords(self, notes, time_threshold=0.1):
        """
        Group notes played within a time threshold as chords.
        """
        last_start = None
        current_chord = Chord([])
        chords = [current_chord]

        for note in notes:
            if last_start is None or abs(note.start - last_start) < time_threshold:
                current_chord.addNote(note.start, note.pitch)
            else:
                # new chord
                current_chord = Chord([])
                current_chord.addNote(note.start, note.pitch)
                chords.append(current_chord)
                
            last_start = note.start
            
        return chords
