# Class used to convert MIDI notes to tabs for string instruments based on tunings
# Dependencies: pretty_midi

from Tab import Tab
from Note import Note

class NoteToTabConverter:

    # Map notes to strings and frets
    def notes_to_tabs(self, note_groups, input_tunings):

        tabs = []

        for notes in note_groups:
            
            for child_note in sorted(notes, key=lambda note: note.start):
                # Find the closest string and fret for each note
                tuning, fret = self.__closest_guitar_fret(child_note.pitch, input_tunings)
                if tuning:
                    tabs.append(Tab(tuning, fret, Note(notes.start or child_note.start, child_note.pitch)))

        return tabs

    def __closest_guitar_fret(self, pitch, tunings):
        # Calculate the closest fret and string for a given pitch
        closest_tuning = None
        closest_fret = None
        min_distance = float('inf')

        for idx, tuning in enumerate(tunings):
            distance = pitch - tuning.pitch
            fret = distance
            if fret >= 0 and fret <= 12:  # We'll limit it to the first 12 frets for simplicity
                if distance < min_distance:
                    min_distance = distance
                    closest_tuning = tuning
                    closest_fret = fret

        return closest_tuning, closest_fret
    