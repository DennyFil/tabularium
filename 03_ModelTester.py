import sys
import os
import pretty_midi
from BassLineTester import BassLineTester
from Tuning import Tuning
from NoteToTabConverter import NoteToTabConverter
from TabsDisplayer import TabsDisplayer
from GPT2Model import GPT2Model

if len(sys.argv) <= 1:
    print('Please submit a model directory path as first argument')
    sys.exit(0)

if len(sys.argv) <= 2:
    print('Please submit a MIDI file path as second argument')
    sys.exit(0)

if len(sys.argv) <= 3:
    print('Please submit as third argument if music should be played during testing')
    sys.exit(0)

if len(sys.argv) <= 4:
    print('Please submit as fourth argument the interval (seconds) between played music pieces')
    sys.exit(0)

model_path_str = sys.argv[1]
file_path_str = sys.argv[2]
play_music = sys.argv[3]
interval = sys.argv[4]
interval = int(interval) if interval.isdecimal() else 3

play_music = play_music == 'y' or play_music == 'yes'

bt = BassLineTester(play_music, interval)

print(f"Loading model")
model = GPT2Model(None, model_path_str)

print(f"Generating bass line for {file_path_str}")
generated_bass_line_notes = bt.test_line(model, file_path_str)

# Define the guitar string tunings (standard tuning)
# guitar_tunings = [
#     Tuning(1, "E2", 40),
#     Tuning(2, "A2", 45),
#     Tuning(3, "D3", 50),
#     Tuning(4, "G3", 55),
#     Tuning(5, "B3", 59),
#     Tuning(6, "e4", 64)
# ]

# Define the bass string tunings (standard tuning)
bass_tunings = [
    Tuning(1, "E1", 28),
    Tuning(2, "A1", 33),
    Tuning(3, "D2", 38),
    Tuning(4, "G2", 43)
]

noteToTabConverter = NoteToTabConverter()

# Load the MIDI file
midi_data = pretty_midi.PrettyMIDI(file_path_str)

bass_tabs = noteToTabConverter.notes_to_tabs(generated_bass_line_notes, bass_tunings) # consider bass line as group of notes

tempo = 2  # Default tempo in seconds per beat (120 BPM)

tempo_times, tempo_bpm = midi_data.get_tempo_changes()
if len(tempo_bpm) > 0:
    tempo = tempo_bpm[0]/60  # First tempo found

# Get the total duration of the MIDI file in seconds
duration = midi_data.get_end_time()

measures_per_row = 4
measure_duration = 2
tabs_displayer = TabsDisplayer(measures_per_row, measure_duration)
head, fn = os.path.split(file_path_str)
tabs_displayer.display(f"Bass tabs of {fn}", tempo, duration, bass_tabs, bass_tunings)
