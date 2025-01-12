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
    pip install transformers[torch]

Using the following MIDI datasets (downloaded to ./datasets)
  https://colinraffel.com/projects/lmd/
		Clean MIDI subset
		LMD-matched
		
	https://huggingface.co/datasets/projectlosangeles/Monster-MIDI-Dataset
	https://huggingface.co/datasets/asigalov61/MIDI-Loops

01_PrepareTrainingData.py
  Loading MIDI files using pretty_midi library (https://craffel.github.io/pretty-midi/)
  Extracting chords and bass lines from those files
  Preparing training data (chords-bass) in JSON format

  first argument: dataset path (folder or file)
  second argument: boolean if prepared data should be overriden ('y' or 'yes' accepted)

  Ex with one file: '''python .\01_PrepareTrainingData.py "E:\datasets\clean_midi\.38 Special\Fantasy Girl.mid" y'''
  Ex for all datasets: '''python .\01_PrepareTrainingData.py "E:\datasets\" y'''

  Prepared data is saved by MIDI file into a .txt file named as follows f"{initial_midi_filename_no_extension.mid}.txt"

  Ex: python .\01_PrepareTrainingData.py "E:\datasets\Monster-MIDI-Dataset-Ver-1-0-CC-BY-NC-SA\MIDIs\0\0001cd8c4da2f70f11b69e4afc8d9d49.mid" y

  NB: bass notes from all bass programs are considered together

Prepared data files (*.mid.txt) moved from source folder to the project folder in order to control versions in GitHub
  .\Copy_Prepared_Data.ps1 -sourceDir "E:\datasets" -targetDir "E:\tabularium\datasets_formatted"

02_TrainingModel.py
  Training a model to create base lines in requested music style given input chords

  Reading data, supplying to the model, training the model, saving the model, validating the model

  Ex from scratch: python .\02_TrainingModel.py "E:\tabularium\datasets_formatted\" "E:\tabularium\models_10" 10
  Ex from given model: python .\02_TrainingModel.py "E:\tabularium\datasets_formatted\" "E:\tabularium\models_100" 100 "E:\tabularium\models_10"

03_ModelTester.py
  Testing the trained model
  BassLineTester
    Reads the MIDI file, plays, removes bass, plays, generates using pre-trained model, adds bass, plays
  
    call test_line function passing the path to MIDI file

    NB: bass line is add as 'Electric Bass (Finger)'

  Ex: python .\03_ModelTester.py "E:\tabularium\models_10" "E:\datasets\MIDI-Loops-Dataset-Small-CC-BY-NC-SA\MIDIs\(Dont Fear) The Reaper___Blue Oyster Cult___loop_3___Piano___32_beats.mid" y 3

  TDB: adapt to receive a mp3, convert to MIDI


Display results in tab form
  TabsDisplayer
