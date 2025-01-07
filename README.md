# tabularium
Generate quality bass tabs of given music style based on song chords

Install python version 3.12.8 (compatible with pytorch)
  https://www.python.org/downloads/
  
You need to add the path of your pip installation to your PATH system variable

Prerequisites to install
    pip install pretty_midi
    pip install music21
    pip install plotly
    pip install termplotlib
		pip install plotext
    pip install pygame
    pip install tqdm
    pip install setuptools
      No module named 'pkg_resources'
    pip install numpy
    pip install transformers
    pip install torch torchvision torchaudio
      ERROR: Could not find a version that satisfies the requirement torch (from versions: none)
      ERROR: No matching distribution found for torch

Using the following MIDI datasets (downloaded to ./datasets)
  https://colinraffel.com/projects/lmd/
		Clean MIDI subset
		LMD-matched
		
	https://huggingface.co/datasets/projectlosangeles/Monster-MIDI-Dataset
	https://huggingface.co/datasets/asigalov61/MIDI-Loops

01_PrepareTrainingData.py
  Loading MIDI files using pretty_midi library (https://craffel.github.io/pretty-midi/)
  Extracting chords and bass lines from those files
  Preparing (tokenizing) training data (chords-bass)

  first argument: dataset path (folder or file)
  second argument: boolean if prepared data should be overriden ('y' or 'yes' accepted)

  Ex with one file: '''python .\01_PrepareTrainingData.py "E:\datasets\clean_midi\.38 Special\Fantasy Girl.mid" y'''
  Ex for all datasets: '''python .\01_PrepareTrainingData.py "E:\datasets\" y'''

  Tokenized data is saved by MIDI file into a .txt file named as follows f"{initial_midi_filename_no_extension.mid}.txt"

Tokenized data files (*.mid.txt) moved from source folder to the project folder in order to control versions in GitHub
  .\Copy_Prepared_Data.ps1 -sourceDir "E:\datasets" -targetDir "E:\tabularium\datasets"

02_TrainingModel.py
  Training a model (to choose) to create base lines in requested music style given input chords

  Reading tokenized data, supplying to the model, training the model, saving the model (how ?)

BassLineTester.py
  Testing the trained model
  Reads the MIDI file, plays, removes bass, plays, generates using pre-trained model, adds bass, plays
  
  call test_line function passing the path to MIDI file

  TDB: adapt to receive a mp3, convert to MIDI


Display results in tab form
  TabsDisplayer
