from Tools import get_bass_from_midi

class BassLineGenerator:

    ## TDB: generate bass line with the model, temporary adding back the same notes
    def generate(self, midi_data):
        bass = get_bass_from_midi(midi_data)

        generated_bass_line_notes = []

        if(bass):
            generated_bass_line_notes = bass.notes

        return generated_bass_line_notes
