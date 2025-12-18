import numpy as np


def sine(freq, t):
    return np.sin(2 * np.pi * freq * t)

def square(freq, t):
    return np.sign(sine(freq, t))

def saw(freq, t):
    return 2.0 * (freq * t - np.floor(freq * t + 0.5))

def triangle(freq, t):
    return 2.0 * np.abs(saw(freq, t)) - 1.0
