import sounddevice as sd
import numpy as np
from . import oscillators


class AudioEngine:
    def __init__(self, samplerate=44100):
        self.freq = 440.0
        self.volume = 0.0
        self.phase = 0
        self.samplerate = samplerate
        self.waveform_fn = oscillators.saw

        self.stream = sd.OutputStream(
            callback=self.callback,
            samplerate=samplerate,
            channels=1
        )

    def set_waveform(self, name: str):
        if name == "sine":
            self.waveform_fn = oscillators.sine
        elif name == "square":
            self.waveform_fn = oscillators.square
        elif name == "saw":
            self.waveform_fn = oscillators.saw
        elif name == "triangle":
            self.waveform_fn = oscillators.triangle
        else:
            raise ValueError(f"Unknown waveform: {name}")

    def callback(self, outdata, frames, time, status):
        t = (np.arange(frames) + self.phase) / self.samplerate

        wave = self.waveform_fn(self.freq, t)  # ✅ always callable
        # wave = np.tanh(wave)                   # soft clip

        outdata[:] = (wave * self.volume).reshape(-1, 1)
        self.phase += frames

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()
