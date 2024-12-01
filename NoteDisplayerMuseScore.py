from music21 import stream, note, chord, environment
us = environment.UserSettings()
us['musescoreDirectPNGPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'  # Set to the path of the MuseScore executable

# Class used to display chords and bass notes using MuseScore
# Dependencies: music21, MuseScore
class NoteDisplayerMuseScore:

    def display_notes(self, chords, bass_line):

        score = self.__convert_to_music21(chords, bass_line)

        # Show the score (e.g., in MuseScore or another notation software)
        #score.show('graph') # music21's Built-In Viewer
        #score.show('plotly')
        score.show()  # Opens the default music notation software

    def __convert_to_music21(self, chords, bass_line):
        # Create separate parts for bass and chords
        bass_part = stream.Part()
        chord_part = stream.Part()

        # Add bass notes to bass part
        for start_time, pitch in bass_line:
            n = note.Note(pitch)
            n.quarterLength = 1  # Adjust duration as needed
            bass_part.append(n)

        # Add chords to chord part
        for chord_notes in chords:
            c = chord.Chord(chord_notes)
            c.quarterLength = 1  # Adjust duration as needed
            chord_part.append(c)

        # Combine parts into a score
        score = stream.Score()
        score.append(bass_part)
        score.append(chord_part)

        return score
