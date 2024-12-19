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
        tokens += ", ".join([self.__build_note_token(chord.name, chord.start) for chord in chords])
        tokens = tokens[:-1] + "],"

        tokens += "BASS:["
        tokens += ", ".join([self.__build_note_token(note.name, note.start) for note in bass_notes])
        tokens = tokens[:-1] + "]"

        return tokens + "}"
    
    def __build_note_token(self, name, start):
        return "{name:" + f"'{name}',start:'{start}'" + "}"
    