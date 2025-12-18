import math

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

A4_NOTE = 440.0
A4_MIDI = 69

def freq_to_midi(freq: float) -> int | None:
    if freq <= 0:
        return None
    midi = A4_NOTE + 12 * math.log2(freq / A4_NOTE)
    return int(round(midi))

def midi_to_note(midi: int) -> str:
    name = NOTES[midi % 12]
    octave = (midi // 12) - 1
    return f"{name}{octave}"

def freq_to_note(freq: float) -> str | None:
    midi = freq_to_midi(freq)
    if midi is None:
        return None
    else:
        return midi_to_note(midi)