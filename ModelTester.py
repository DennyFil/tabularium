import sys
from BassLineTester import BassLineTester

if len(sys.argv) <= 1:
    print('Please submit a MIDI file path as first argument')
    sys.exit(0)

if len(sys.argv) <= 2:
    print('Please submit as second argument if music should be played during testing')
    sys.exit(0)

if len(sys.argv) <= 3:
    print('Please submit as third argument the interval (seconds) between played music pieces')
    sys.exit(0)

file_path_str = sys.argv[1]
play_music = sys.argv[2]
interval = int(sys.argv[3])

play_music = play_music == 'y' or play_music == 'yes'

bt = BassLineTester(play_music, interval)
bt.test_line(file_path_str)
