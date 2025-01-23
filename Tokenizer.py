# Class used to tokenize MIDI data
# Dependencies: pretty_midi

class Tokenizer:

    # "<STYLE:Jazz> <CHORD:C4,E4,G4> <BASS:C2> <CHORD:F4,A4,C5> <BASS:F2>"
    # suppose chords and bass line are always available
    def get_tokens(self, style, chords, bass_notes):

        if len(chords) == 0 or len(bass_notes) == 0:
            raise ValueError("Missing notes, cannot generate tokens")

        # limit input to 30 seconds
        chords = filter(lambda c: c.start <= 30, chords)
        bass_notes = filter(lambda b: b.start <= 30, bass_notes)

        tokens = "{"
        if style:
            tokens += f"\"STYLE:\"{style}\","

        tokens += "\"CHORD\":{\"value\":\""
        tokens += ",".join([self.__build_note_token(chord.name, chord.start) for chord in chords])
        tokens += "\"},"

        tokens += "\"BASS\":{\"value\":\""
        tokens += ",".join([self.__build_note_token(note.name, note.start) for note in bass_notes])
        tokens += "\"}"

        return tokens + "}"
    
    def __build_note_token(self, name, start):
        return "[" + f"'{name}',{start}" + "]"
    