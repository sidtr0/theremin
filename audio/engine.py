import sounddevice as sd
import numpy as np

class AudioEngine:
    def __init__(self, samplerate=44100):
        self.samplerate = samplerate
        self.freq = 440
        self.volume = 0.0
        self.phase = 0

        self.stream = sd.OutputStream(
            callback=self.callback,
            samplerate=samplerate,
            channels=1
        )

    def callback(self, outdata, frames, time, status):
        t = (np.arange(frames) + self.phase) / self.samplerate
        wave = np.tan(2 * np.pi * self.freq * t) + np.sin(2 * np.pi * self.freq * t)
        outdata[:] = (wave * self.volume).reshape(-1, 1)
        self.phase += frames

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()