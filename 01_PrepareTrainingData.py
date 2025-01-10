import sys
import os
from pathlib import Path
from os.path import join
from tqdm import tqdm
import pretty_midi
from NoteExtractor import NoteExtractor
from Tokenizer import Tokenizer
from Exceptions import ChordException, BassException

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
f_loaded = open(f"{dataset_path_str}_loaded.txt", "w")
nb_files_skipped = 0
f_skipped = open(f"{dataset_path_str}_skipped.txt", "w")
nb_files_failed_to_load = 0
f_failed_to_load = open(f"{dataset_path_str}_failed_to_load.txt", "w")
nb_files_no_chords = 0
f_no_chords = open(f"{dataset_path_str}_no_chords.txt", "w")
nb_files_no_bass = 0
f_no_bass = open(f"{dataset_path_str}_no_bass.txt", "w")

note_extractor = NoteExtractor()
tokenizer = Tokenizer()

pbar = tqdm(file_paths)
for fp in pbar:
    try:
        pbar.set_description(f"Loaded: {nb_files_loaded}, skipped: {nb_files_skipped}, without chords: {nb_files_no_chords}, without bass: {nb_files_no_bass}, failed to load: {nb_files_failed_to_load}")

        fp_for_training = f"{fp}.txt"
        # Check if tokenized training data already exists
        if os.path.exists(fp_for_training) and not override_prepared_data == 'y' and not override_prepared_data == 'yes':
            nb_files_skipped += 1
            f_skipped.write(fp+'\n')
            continue

        head, fn = os.path.split(fp)
        # Load the MIDI file
        midi_data = pretty_midi.PrettyMIDI(fp)

        # Extract chords and bass notes
        chords, bass_line = note_extractor.extract_chords_and_bass(midi_data)

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

        nb_files_loaded += 1
        f_loaded.write(fp+'\n')
    except ChordException as ve:
        nb_files_no_chords += 1
        f_no_chords.write(fp+'\n')
        continue
    except BassException as ve:
        nb_files_no_bass += 1
        f_no_bass.write(fp+'\n')
        continue
    except Exception as e:
        print(f"Failed to process {fp}")
        print(e)
        nb_files_failed_to_load += 1
        f_failed_to_load.write(fp+'\n')
        continue

pbar.set_description(f"Loaded: {nb_files_loaded}, skipped: {nb_files_skipped}, without chords: {nb_files_no_chords}, failed to load: {nb_files_failed_to_load}")

f_loaded.close()
f_skipped.close()
f_failed_to_load.close()
f_no_chords.close()
f_no_bass.close()

print(f"Number of files loaded: {nb_files_loaded}")
print(f"Number of files skipped as already processed: {nb_files_skipped}")
print(f"Number of files without chords: {nb_files_no_chords}")
print(f"Number of files without bass: {nb_files_no_bass}")
print(f"Number of files failed to load: {nb_files_failed_to_load}")

def isNotBlank (myString):
    return bool(myString and myString.strip())
