# Preset waveform function for different action processes
import math

Pi = math.pi


def basic_sine(x):
    return (math.cos(-2 * Pi * x) + 1) / 2


def pull_up_sine(x):
    if x <= 0.6:
        return (math.cos(-5 * Pi * x / 3) + 1) / 2
    if x > 0.6:
        return (math.cos(5 * Pi * (x - 0.6) / 2) + 1) / 2
