# Class used to manage a MIDI note which is a combination of start and a pitch
class Note:
    def __init__(self, start, pitch):
        self.pitch = pitch
        self.start = start
        