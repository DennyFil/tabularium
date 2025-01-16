# Tabularium

Generate quality bass tabs of given music style based on given song chords

## Prerequisites to install
Install python version 3.12.8 (compatible with pytorch) from https://www.python.org/downloads/
Add the python path to your PATH system variable

**TODO: check what is not needed**
```
pip install pretty_midi
pip install music21
pip install plotly
pip install termplotlib
pip install plotext
pip install pygame
pip install tqdm
pip install setuptools (No module named 'pkg_resources')
pip install numpy
pip install transformers
pip install torch torchvision torchaudio
pip install transformers[torch]
pip install sentencepiece
pip install protobuf
Create an account on HuggingFace.co, add access token, add token to environment variable
Visit https://huggingface.co/meta-llama/Llama-3.2-1B to ask for access.
```

## Datasets
Downloaded MIDI the following MIDI datasets
* Clean MIDI subset ( http://hog.ee.columbia.edu/craffel/lmd/clean_midi.tar.gz )
* LMD-matched ( http://hog.ee.columbia.edu/craffel/lmd/lmd_matched.tar.gz )
* https://huggingface.co/datasets/asigalov61/MIDI-Loops

## Prepare training data (~24h for all datasets)
* Script 01_PrepareTrainingData.py
  * Arguments
    * first argument: dataset path (folder or file)
    * second argument: boolean if prepared data should be overriden ('y' or 'yes' accepted)
  * Loading MIDI files using pretty_midi library (https://craffel.github.io/pretty-midi/)
  * Extracting chords and bass lines from those files (NoteExtractor)
  * Preparing training data (chords-bass pairs) in JSON format

  Ex with one file: ```python .\01_PrepareTrainingData.py "E:\datasets\clean_midi\.38 Special\Fantasy Girl.mid" y```

  Ex for all datasets: ```python .\01_PrepareTrainingData.py "E:\datasets\" y```

  For every MIDI file prepared data is saved into a .txt file named as follows f"{initial_midi_filename_no_extension.mid}.txt"

  NB: bass notes from all bass programs are considered together

  Some *.mid.txt files removed due to very long path

  Prepared data files (*.mid.txt) were moved from dataset source folder into the GitHub folder in order to version-control
  * ```.\Copy_Prepared_Data.ps1 -sourceDir "E:\datasets" -targetDir "E:\tabularium\datasets_formatted"```

## Training model (~ h for all datasets)
* Script 02_TrainingModel.py
  * Arguments
    * first argument: prepared dataset path (folder)
    * second argument: path to save the model
    * third argument: number of files to consider for training
    * forth argument: path to model if restoring
  * Reading data, supplying to the model, training the model, saving the model, validating the model

  Login to HuggingFace before launching the training ```huggingface-cli login --token $HF_TOKEN --add-to-git-credential```

  Ex from scratch: python .\02_TrainingModel.py "E:\tabularium\datasets_formatted\" "E:\tabularium\models_10" 10
  
  Ex from given model: python .\02_TrainingModel.py "E:\tabularium\datasets_formatted\" "E:\tabularium\models_100" 100 "E:\tabularium\models_10"

## Testing model
* Script 03_ModelTester.py
  * Testing the trained model
  * Arguments
    * first argument: path to model (folder, model class will read itself the file needed)
    * second argument: path to MIDI file to be tested
    * third argument: boolean if should be played during testing ('y' or 'yes' accepted)
    * forth argument: interval in seconds to use between playing different variations of submitted file
  * Use BassLineTester
    * read the MIDI file and play it
    * remove bass and play it again
    * generate the new bass line using the pre-trained model
    * add this bass line and play
  * Use TabsDisplayer to display the generated bass tabs in console
  
  NB: bass line is added as 'Electric Bass (Finger)'

  Ex: python .\03_ModelTester.py "E:\tabularium\models_10" "E:\datasets\MIDI-Loops-Dataset-Small-CC-BY-NC-SA\MIDIs\(Dont Fear) The Reaper___Blue Oyster Cult___loop_3___Piano___32_beats.mid" y 3

  TDB: adapt to receive a mp3, convert to MIDI
