import copy
import os
import json
import time
import re
import pretty_midi
import pygame
from Note import Note
from NoteExtractor import NoteExtractor
from Tokenizer import Tokenizer
from Tools import is_bass, get_bass_notes_from_midi

class BassLineTester:

    def __init__(self, play_music, interval):
        self.play_music = play_music
        self.interval = interval

    def test_line(self, model, input_file_path):
        midi_data = pretty_midi.PrettyMIDI(input_file_path)
        
        if self.play_music:
            print(f"Playing input")
            self.__play_file(input_file_path)
            time.sleep(self.interval)

        print(f"Bass notes nb before generation: {len(get_bass_notes_from_midi(midi_data))}")

        note_extractor = NoteExtractor()
        chords, original_bass_line = note_extractor.extract_chords_and_bass(midi_data)
        
        print("Removing bass line and saving file")
        midi_data_without_bass = self.__remove_bass(midi_data)

        output_file_name_prefix, file_extension = os.path.splitext(input_file_path)
        
        # Save the modified MIDI to a new file
        file_no_bass_path = f"{output_file_name_prefix}_no_bass{file_extension}"
        midi_data_without_bass.write(file_no_bass_path)

        if self.play_music:
            print(f"Playing input without bass")
            self.__play_file(file_no_bass_path)
            time.sleep(self.interval)

        tokenizer = Tokenizer()
        tokens = tokenizer.get_tokens(None, chords, original_bass_line)
        parsed_data = json.loads(tokens)
        chord_sequence = parsed_data["CHORD"]["value"]

        generated_bass_line_notes_str = model.generate_output(chord_sequence) # parsed_data["BASS"]["value"]

        print("Generated bass line")
        print(generated_bass_line_notes_str)
        # Convert the generated string to a list of notes
        # generated: "['D#2',36.190439999999995],['D#2',36.66663],['D#2',37.14281999999999],['D#2',37.380914999999995]"
        generated_bass_line_notes_split = [[key, float(value)] for key, value in re.findall(r"\['(.*?)',([\d\.]+)\]", generated_bass_line_notes_str)]

        default_velocity = 64

        # convert bass notes to pretty_midi.Note, let the note sound until the next one starts
        generated_bass_line_notes = []
        for idx in range(len(generated_bass_line_notes_split)-1):
            # current note
            note = generated_bass_line_notes_split[idx]
            # note is formated as an array ['name', start]
            # start
            start = float(note[1])
            next_note = generated_bass_line_notes_split[idx+1]
            # end current note at the same time the next note starts
            end = float(next_note[1])

            generated_bass_line_notes.append(pretty_midi.Note(default_velocity, pretty_midi.note_name_to_number(note[0]), start, end))

        # add the last note with short duration
        generated_bass_line_notes.append(pretty_midi.Note(default_velocity, pretty_midi.note_name_to_number(next_note[0]), end, end + 1))

        # add the generated line to file and play
        print("Adding generated bass line and saving file")
        midi_data_bass_added = self.__add_bass_line(midi_data_without_bass, generated_bass_line_notes)

        file_bass_added_path = f"{output_file_name_prefix}_bass_added{file_extension}"
        midi_data_bass_added.write(file_bass_added_path)

        if self.play_music:
            print(f"Playing input with generated bass")
            self.__play_file(file_bass_added_path)

        return[Note(n.start, n.pitch) for n in generated_bass_line_notes]

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
            
