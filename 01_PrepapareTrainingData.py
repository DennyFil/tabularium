import sys
import os
from pathlib import Path
from os.path import join
import pretty_midi
from NoteExtractor import NoteExtractor
from TabsDisplayer import TabsDisplayer

# Reading MIDI files from a given folder, extracting chords and bass lines, preparing and saving training data

missing_dataset_msg = 'Missing dataset folder path'

if len(sys.argv) <= 1:
    print(missing_dataset_msg)
    sys.exit(0)

dataset_folder = sys.argv[1]
if not os.path.exists(dataset_folder):
    print(f"Folder {dataset_folder} does not exist")
    sys.exit(0)

has_files = os.listdir(dataset_folder)

if len(has_files) == 0:
    print(f"Folder {dataset_folder} is empty")
    sys.exit(0)

print(f"Reading dataset from {dataset_folder}")

files_loaded = []
files_failed_to_load = []
file_paths = [join(dataset_folder, f) for f in Path(dataset_folder).rglob('*.mid')]
print(f"Reading {len(file_paths)} files")

bass_note_threshold = 60 # Assuming bass notes are below Middle C (C4 = 60)
note_extractor = NoteExtractor(bass_note_threshold)

# Define the guitar string tunings (standard tuning)
guitar_tunings = [40, 45, 50, 55, 59, 64] # E2 A2 D3 G3 B3 e4 (from low E to high e)
guitar_tabs_displayer = TabsDisplayer(guitar_tunings)
bass_tunings = [28, 33, 38, 43] # E1 A1 D2 G2
bass_tabs_displayer = TabsDisplayer(bass_tunings)

file_paths = file_paths[:10] # temporary take 10 first files

for fp in file_paths:
    try:
        # Load the MIDI file
        midi_data = pretty_midi.PrettyMIDI(fp)
        # Extract chords and bass notes
        chords, bass_line = note_extractor.extract_chords_and_bass(midi_data)

        guitar_tabs_displayer.display(chords) # a chord is a group of notes
        bass_tabs_displayer.display([bass_line]) # consider bass line as group of notes

        files_loaded.append(fp)
    except Exception as e:
        print(fp)
        print(e)
        files_failed_to_load.append(fp)

print(f"Loaded {len(files_loaded)} files")
print(f"Failed to load {len(files_failed_to_load)} files")

def isNotBlank (myString):
    return bool(myString and myString.strip())

# Labelling data

# Storing data
    