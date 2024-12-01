from NoteToTabConverter import NoteToTabConverter

# Class used to display chords and bass notes as tabs
class TabsDisplayer:

    def __init__(self, input_tunings):
        self.tunings = input_tunings

    def display(self, note_groups):

        n2tConverter = NoteToTabConverter(self.tunings)
        tabs = n2tConverter.notes_to_tabs(note_groups)
        print(tabs)
        