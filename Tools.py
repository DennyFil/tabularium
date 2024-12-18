from Constants import bass_midi_program_ids, guitar_midi_program_ids

def get_bass_notes_from_midi(midi_data):
    
    notes = []

    for ins in [ins for ins in midi_data.instruments if is_bass(ins)]:
        for note in ins.notes:
            notes.append(note)

    return notes

def is_bass(instrument):
    return any(p == instrument.program for p in bass_midi_program_ids)

def is_guitar(instrument):
    return any(p == instrument.program for p in guitar_midi_program_ids)
