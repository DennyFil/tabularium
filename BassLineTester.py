import copy
import os
import time
import pretty_midi
import pygame
from Tools import is_bass, get_bass_notes_from_midi
from BassLineGenerator import BassLineGenerator

class BassLineTester:

    def __init__(self, play_music, interval):
        self.play_music = play_music
        self.interval = interval

    def test_line(self, input_file_path):
        midi_data = pretty_midi.PrettyMIDI(input_file_path)
        
        if self.play_music:
            print(f"playing input")
            self.__play_file(input_file_path)
            time.sleep(self.interval)

        print(f"bass notes nb before generation: {len(get_bass_notes_from_midi(midi_data))}")
        
        midi_data_without_bass = self.__remove_bass(midi_data)

        output_file_name_prefix, file_extension = os.path.splitext(input_file_path)
        
        # Save the modified MIDI to a new file
        file_no_bass_path = f"{output_file_name_prefix}_no_bass{file_extension}"
        midi_data_without_bass.write(file_no_bass_path)

        if self.play_music:
            print(f"playing input without bass")
            self.__play_file(file_no_bass_path)
            time.sleep(self.interval)

        generated_bass_line_notes = BassLineGenerator().generate(midi_data)
        
        # add the generated line to file and play
        midi_data_bass_added = self.__add_bass_line(midi_data_without_bass, generated_bass_line_notes)

        file_bass_added_path = f"{output_file_name_prefix}_bass_added{file_extension}"
        midi_data_bass_added.write(file_bass_added_path)

        if self.play_music:
            print(f"playing input with generated bass")
            self.__play_file(file_bass_added_path)

    def __remove_bass(self, midi_data):
        
        copied_midi = copy.deepcopy(midi_data)

        copied_midi.instruments = [
            instrument for instrument in copied_midi.instruments
            if not is_bass(instrument)
        ]
            
        return copied_midi
    
    def __add_bass_line(self, midi_data, notes):
        
        copied_midi = copy.deepcopy(midi_data)

        if len(notes) > 0:
            # at this point MIDI should not have any bass
            # adding same bass type for all given notes no matter their original bass type
            bass_program = pretty_midi.instrument_name_to_program('Electric Bass (Finger)')
            bass = pretty_midi.Instrument(program=bass_program)

            bass.notes = notes
            print(f"bass notes nb after generation: {len(bass.notes)}")

            copied_midi.instruments.append(bass)
            
        return copied_midi
        
    def __play_file(self, file_path):
        pygame.mixer.init()
        try:
            clock = pygame.time.Clock()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                # check if playback has finished
                clock.tick(30)
        finally:
            pygame.mixer.quit()
            