from Constants import bass_instrument_name

def get_bass_from_midi(midi_data):
    return next((ins for ins in midi_data.instruments if ins.name.strip() == bass_instrument_name), None)