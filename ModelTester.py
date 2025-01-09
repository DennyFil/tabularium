import sys
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from BassLineTester import BassLineTester

if len(sys.argv) <= 1:
    print('Please submit a model file path as first argument')
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

model = GPT2LMHeadModel.from_pretrained(model_path_str)
tokenizer = GPT2Tokenizer.from_pretrained(model_path_str)
bt.test_line(model, tokenizer, file_path_str)
