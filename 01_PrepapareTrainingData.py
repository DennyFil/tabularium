import sys
import os
from pathlib import Path
from os.path import join
from tqdm import tqdm
import pretty_midi
from NoteExtractor import NoteExtractor
from NoteToTabConverter import NoteToTabConverter
from TabsDisplayer import TabsDisplayer
from Tokenizer import Tokenizer
from Tuning import Tuning

# Reading MIDI files from a given folder, extracting chords and bass lines, preparing and saving training data

if len(sys.argv) <= 1:
    print('Please submit dataset path as first argument')
    sys.exit(0)

if len(sys.argv) <= 2:
    print('Please submit as second argument if prepared data should be overriden')
    sys.exit(0)

override_prepared_data = sys.argv[2]

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

nb_files_loaded = 0
nb_files_skipped = 0
nb_files_failed_to_load = 0
nb_files_no_chords = 0

bass_note_threshold = 55 # Assuming bass notes are below Middle C (C4 = 60)
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
tokenizer = Tokenizer()

pbar = tqdm(file_paths)
for fp in pbar:
    try:
        pbar.set_description(f"Loaded: {nb_files_loaded}, skipped: {nb_files_skipped}, without chords: {nb_files_no_chords}, failed to load: {nb_files_failed_to_load}")

        fp_for_training = f"{fp}.txt"
        # Check if tokenized training data already exists
        if os.path.exists(fp_for_training) and not override_prepared_data == 'y' and not override_prepared_data == 'yes':
            nb_files_skipped += 1
            continue

        head, fn = os.path.split(fp)
        # Load the MIDI file
        midi_data = pretty_midi.PrettyMIDI(fp)

        # Extract chords and bass notes
        chords, bass_line = note_extractor.extract_chords_and_bass(midi_data)

        if(len(chords) == 0):
            raise ValueError("Missing chords")

        # print("Chords")
        # for chord in chords:
        #     print(f"chord: {chord.name}")
        #     for n in chord.notes:
        #         print(n)

        # print("#########################")

        # Tokenize chords and bass notes
        tokens = tokenizer.get_tokens(None, chords, bass_line) # TDB: add style

        # Save tokens for training
        f = open(fp_for_training, "w")
        f.write(tokens)
        f.close()

        # print("Bass")
        # for bsn in bass_line:
        #     print(bsn)

        #guitar_tabs = noteToTabConverter.notes_to_tabs(chords, guitar_tunings) # a chord is a group of notes

        #bass_tabs = noteToTabConverter.notes_to_tabs(bass_line, bass_tunings) # consider bass line as group of notes
    
        tempo = 2  # Default tempo in seconds per beat (120 BPM)

        tempo_times, tempo_bpm = midi_data.get_tempo_changes()
        if len(tempo_bpm) > 0:
            tempo = tempo_bpm[0]/60  # First tempo found

        # Get the total duration of the MIDI file in seconds
        duration = midi_data.get_end_time()

        #tabs_displayer.display(f"Guitar tabs of {fn}", tempo, duration, guitar_tabs, guitar_tunings)
        # tabs_displayer.display(f"Bass tabs of {fn}", tempo, duration, bass_tabs, bass_tunings)

        nb_files_loaded += 1
    except ValueError as ve:
        nb_files_no_chords += 1
        continue
    except Exception as e:
        print(f"Failed to process {fp}")
        print(e)
        nb_files_failed_to_load += 1
        continue

pbar.set_description(f"Loaded: {nb_files_loaded}, skipped: {nb_files_skipped}, without chords: {nb_files_no_chords}, failed to load: {nb_files_failed_to_load}")
print(f"Number of files loaded: {nb_files_loaded}")
print(f"Number of files skipped as already processed: {nb_files_skipped}")
print(f"Number of files without chords: {nb_files_no_chords}")
print(f"Number of files failed to load: {nb_files_failed_to_load}")

def isNotBlank (myString):
    return bool(myString and myString.strip())

# Labelling data

# Storing data
    