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
pip install accelerate
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
    - clean_midi/Alpentrio Tirol/Alpentrio Hitmix_ Alpentrio-Medley   Hast a bisserl Zeit fur mi   Tepperter Bua   Hallo kleine Traumfrau   Vergiss die Liebe nicht   Ich freu' mich schon auf dich   Ich hab was ganz lieb's traumt von dir   Geheimnis der Johannesnacht   Engel v. Ma.mid.txt
    - clean_midi/Rush/Cygnus X-1, Book II_ Hemispheres_ I. Prelude   II. Apollo_ Bringer of Wisdom   III. Dionysus_ Bringer of Love   IV. Armageddon_ The Battle of Heart and Mind   V. Cygnus_ Bringer of Balance   VI. The Sphere_ A Kind of Dream.mid.txt
    - clean_midi/Rush/The Fountain of Lamneth_ I. In the Valley   II. Didacts and Narpets   III. No One at the Bridge   IV. Panacea   V. Bacchus Plateau   VI. The Fountain.mid.txt
    - MIDI-Loops-Dataset-Small-CC-BY-NC-SA/MIDIs/Cygnus X-1, Book II_ Hemispheres_ I. Prelude   II. Apollo_ Bringer of Wisdom   III. Dionysus_ Bringer of Love   IV. Armageddon_ ___Rush___loop_0___Piano___32_beats.mid.txt': Filename too long
    - MIDI-Loops-Dataset-Small-CC-BY-NC-SA/MIDIs/Cygnus X-1, Book II_ Hemispheres_ I. Prelude   II. Apollo_ Bringer of Wisdom   III. Dionysus_ Bringer of Love   IV. Armageddon_ ___Rush___loop_1___Drums___32_beats.mid.txt': Filename too long
    - MIDI-Loops-Dataset-Small-CC-BY-NC-SA/MIDIs/Cygnus X-1, Book II_ Hemispheres_ I. Prelude   II. Apollo_ Bringer of Wisdom   III. Dionysus_ Bringer of Love   IV. Armageddon_ ___Rush___loop_2___Piano___32_beats.mid.txt': Filename too long
    - MIDI-Loops-Dataset-Small-CC-BY-NC-SA/MIDIs/Cygnus X-1, Book II_ Hemispheres_ I. Prelude   II. Apollo_ Bringer of Wisdom   III. Dionysus_ Bringer of Love   IV. Armageddon_ ___Rush___loop_3___Piano___32_beats.mid.txt': Filename too long
    - MIDI-Loops-Dataset-Small-CC-BY-NC-SA/MIDIs/Get Busy Living or Get Busy Dying Do Your Part to Save the Scene and Stop Going to Shows___Fall Out Boy___loop_0___Piano___32_beats.mid.txt
    - MIDI-Loops-Dataset-Small-CC-BY-NC-SA/MIDIs/Il mare impetuoso al tramonto sali sulla luna e dietro una tendina di stelle....2___Zucchero___loop_0___Piano___32_beats.mid.txt
    - MIDI-Loops-Dataset-Small-CC-BY-NC-SA/MIDIs/Il mare impetuoso al tramonto sali sulla luna e dietro una tendina di stelle....3___Zucchero___loop_0___Drums___32_beats.mid.txt
    - MIDI-Loops-Dataset-Small-CC-BY-NC-SA/MIDIs/Il mare impetuoso al tramonto sali sulla luna e dietro una tendina di stelle....3___Zucchero___loop_0___Piano___32_beats.mid.txt

  Prepared data files (*.mid.txt) were moved from dataset source folder into the GitHub folder in order to version-control
  * ```.\Copy_Prepared_Data.ps1 -sourceDir "E:\datasets" -targetDir "E:\tabularium\datasets_formatted"```

  **NB: datasets are version controlled, NO need to launch 01_PrepareTrainingData.py multiple times, launch training on files of datasets_formatted folder**

## Training model
* Script 02_TrainingModel.py
  * Arguments
    * first argument: name of the model to train
    * second argument: prepared dataset path (folder)
    * third argument: path to save the model
    * forth argument: number of files to consider for training
    * fifth argument: path to model if restoring
  * Reading data, supplying to the model, training the model, saving the model

  Login to HuggingFace before launching the training ```huggingface-cli login --token $HF_TOKEN --add-to-git-credential```

  Ex from scratch: python .\02_TrainingModel.py qwen "E:\tabularium\datasets_formatted\for_training" "E:\tabularium\models_10" 10
  
  Ex from given model: python .\02_TrainingModel.py qwen "E:\tabularium\datasets_formatted\for_training" "E:\tabularium\models_100" 100 "E:\tabularium\models_10"

## Validating model
* Script 02b_ValidatingModel.py
  * Arguments
    * first argument: name of the model to train
    * second argument: prepared dataset path (folder)
    * third argument: path to trained model
    * forth argument: number of files to consider for validation
  * Reading data, restoring model, validating model

  Login to HuggingFace before launching the validation ```huggingface-cli login --token $HF_TOKEN --add-to-git-credential```

  Ex from scratch: python .\02b_ValidatingModel.py qwen "E:\tabularium\datasets_formatted\for_validation" "E:\tabularium\models_10" 10
  
## Testing model
* Script 03_ModelTester.py
  * Testing the trained model
  * Arguments
    * first argument: name of the model to test
    * second argument: path to model (folder, model class will read itself the file needed)
    * third argument: path to MIDI file to be tested
    * forth argument: boolean if should be played during testing ('y' or 'yes' accepted)
    * fifth argument: interval in seconds to use between playing different variations of submitted file
  * Use BassLineTester
    * read the MIDI file and play it
    * remove bass and play it again
    * generate the new bass line using the pre-trained model
    * add this bass line and play
  * Use TabsDisplayer to display the generated bass tabs in console
  
  NB: bass line is added as 'Electric Bass (Finger)'

  Ex: python .\03_ModelTester.py qwen "E:\tabularium\models_10" "E:\datasets\MIDI-Loops-Dataset-Small-CC-BY-NC-SA\MIDIs\(Dont Fear) The Reaper___Blue Oyster Cult___loop_3___Piano___32_beats.mid" y 3
  