import sys
import os
from pathlib import Path
from os.path import join
import pretty_midi
from NoteExtractor import NoteExtractor
from NoteToTabConverter import NoteToTabConverter
from TabsDisplayer import TabsDisplayer
from Tuning import Tuning

# Reading MIDI files from a given folder, extracting chords and bass lines, preparing and saving training data

missing_dataset_msg = 'Missing dataset path'

if len(sys.argv) <= 1:
    print(missing_dataset_msg)
    sys.exit(0)

dataset_path_str = sys.argv[1]
if not os.path.exists(dataset_path_str):
    print(f"Path {dataset_path_str} does not exist")
    sys.exit(0)

dataset_path = Path(dataset_path_str)
is_file = dataset_path.is_file()

if not is_file:
    has_files = os.listdir(dataset_path_str)
    if len(has_files) == 0:
        print(f"Folder {dataset_path_str} is empty")
        sys.exit(0)

print(f"Reading dataset from {dataset_path_str}")

if is_file:
    file_paths = [dataset_path_str]
else:
    file_paths = [join(dataset_path_str, f) for f in dataset_path.rglob('*.mid')]

print(f"Reading {len(file_paths)} files")

files_loaded = []
files_failed_to_load = []

bass_note_threshold = 60 # Assuming bass notes are below Middle C (C4 = 60)
note_extractor = NoteExtractor(bass_note_threshold)

# Define the guitar string tunings (standard tuning)
guitar_tunings = [
    Tuning(1, "E2", 40),
    Tuning(2, "A2", 45),
    Tuning(3, "D3", 50),
    Tuning(4, "G3", 55),
    Tuning(5, "B3", 59),
    Tuning(6, "e4", 64)
]

bass_tunings = [
    Tuning(1, "E1", 28),
    Tuning(2, "A1", 33),
    Tuning(3, "D2", 38),
    Tuning(4, "G2", 43)
]

noteToTabConverter = NoteToTabConverter()
measures_per_row = 4
measure_duration = 2
tabs_displayer = TabsDisplayer(measures_per_row, measure_duration)

file_paths = file_paths[:1] # temporary take 1 first files

for fp in file_paths:
    try:
        head, fn = os.path.split(fp)
        # Load the MIDI file
        print(f"Processing {fn}")
        midi_data = pretty_midi.PrettyMIDI(fp)

        # Extract chords and bass notes
        chords, bass_line = note_extractor.extract_chords_and_bass(midi_data)

        guitar_tabs = noteToTabConverter.notes_to_tabs(chords, guitar_tunings) # a chord is a group of notes

        bass_tabs = noteToTabConverter.notes_to_tabs(bass_line, bass_tunings) # consider bass line as group of notes
    
        tempo = 2  # Default tempo in seconds per beat (120 BPM)

        tempo_times, tempo_bpm = midi_data.get_tempo_changes()
        if len(tempo_bpm) > 0:
            tempo = tempo_bpm[0]/60  # First tempo found

        # Get the total duration of the MIDI file in seconds
        duration = midi_data.get_end_time()

        tabs_displayer.display(f"Guitar tabs of {fn}", tempo, duration, guitar_tabs, guitar_tunings)
        #tabs_displayer.display(f"Bass tabs of {fn}", tempo, duration, bass_tabs, bass_tunings)

        files_loaded.append(fn)
        print(f"Processed {fn}")
    except Exception as e:
        print(f"Failed to process {fp}")
        print(e)
        files_failed_to_load.append(fp)

print(f"Loaded {len(files_loaded)} files")
print(f"Failed to load {len(files_failed_to_load)} files")

def isNotBlank (myString):
    return bool(myString and myString.strip())

# Labelling data

# Storing data
    