# Class used to tokenize MIDI data
# Dependencies: pretty_midi

class Tokenizer:

    # "<STYLE:Jazz> <CHORD:C4,E4,G4> <BASS:C2> <CHORD:F4,A4,C5> <BASS:F2>"
    # suppose chords and bass line are always available
    def get_tokens(self, style, chords, bass_notes):

        if len(chords) == 0 or len(bass_notes) == 0:
            raise ValueError("Missing notes, cannot generate tokens")

        tokens = "{"
        if style:
            tokens += f"STYLE:'{style}',"

        tokens += "CHORD:["
        for chord in chords:
            tokens += self.__build_note_token(chord.name, chord.start) + ","
        tokens = tokens[:-1] + "],"

        tokens += "BASS: ["
        for note in bass_notes:
            tokens += self.__build_note_token(note.name, note.start) + ","
        tokens = tokens[:-1] + "]"

        return tokens + "}"
    
    def __build_note_token(self, name, start):
        return "{name:" + f"'{name}',start:'{start}'" + "}"
    