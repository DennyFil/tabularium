# tabularium
Generate quality bass tabs of given music style based on song chords

Using the following MIDI datasets
    https://colinraffel.com/projects/lmd/
		Clean MIDI subset
		LMD-matched
		
	https://huggingface.co/datasets/projectlosangeles/Monster-MIDI-Dataset
	https://huggingface.co/datasets/asigalov61/MIDI-Loops

Prerequisites to install
    pip install pretty_midi
    pip install music21
        pip install plotly
    pip install termplotlib
		pip install plotext
    pip install pygame

Loading MIDI files using pretty_midi library (https://craffel.github.io/pretty-midi/)

Extracting chords and bass lines from those files

Preparing training data (style-chords-bass)

Training a model (to choose) to create base lines in requested music style given input chords

Save model (how ?)

Testing the trained model

Display results in tab form
