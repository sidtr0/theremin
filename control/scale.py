import math

# Semitone offsets from root (C = 0)
SCALES = {
    "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "major":     [0, 2, 4, 5, 7, 9, 11],
    "minor":     [0, 2, 3, 5, 7, 8, 10],
    "pentatonic":[0, 2, 4, 7, 9],
    "blues":     [0, 3, 5, 6, 7, 10],
}

A4_FREQ = 440.0
A4_MIDI = 69


def freq_to_midi(freq: float) -> float:
    return A4_MIDI + 12 * math.log2(freq / A4_FREQ)


def midi_to_freq(midi: float) -> float:
    return A4_FREQ * (2 ** ((midi - A4_MIDI) / 12))


def quantize_freq(freq: float, scale="major", root=60):
    midi = freq_to_midi(freq)
    octave = int(midi // 12) * 12

    allowed = []
    for step in SCALES[scale]:
        allowed.append(octave + step + (root % 12))

    nearest = min(allowed, key=lambda x: abs(x - midi))
    return midi_to_freq(nearest)
