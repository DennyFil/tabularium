# Class used to convert MIDI notes to tabs
# Dependencies: pretty_midi
class NoteToTabConverter:
    
    def __init__(self, input_tunings):
        self.tunings = input_tunings

    def notes_to_tabs(self, note_groups):
    
        # Convert notes to tab
        tabs = []
        for notes in note_groups:
            for note in notes:
                # Find the closest string and fret for each note
                pitch = note.pitch  # MIDI pitch
                string, fret = self.__closest_guitar_fret(pitch, self.tunings)
                tabs.append(f"String: {string}, Fret: {fret}, Time: {note.start}")
        
        return tabs

    def __closest_guitar_fret(self, pitch, tunings):
        # Calculate the closest fret and string for a given pitch
        closest_string = None
        closest_fret = None
        min_distance = float('inf')

        for string_idx, tuning in enumerate(tunings):
            distance = abs(pitch - tuning)
            fret = distance
            if fret <= 12:  # We'll limit it to the first 12 frets for simplicity
                if distance < min_distance:
                    min_distance = distance
                    closest_string = string_idx + 1  # Strings are numbered from 1
                    closest_fret = fret

        return closest_string, closest_fret