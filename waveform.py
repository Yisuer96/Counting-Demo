# Preset waveform function for different action processes
import math

Pi = math.pi


def basic_sine(x):
    return (math.cos(-2 * Pi * x) + 1) / 2


def pull_up_poly(x):
    return 59.37 * x ** 6 - 202.2 * x ** 5 + 256.2 * x ** 4 - 140.6 * x ** 3 + 23.61 * x ** 2 + 3.681 * x - 0.01616


def push_up_poly(x):
    if x == 1:
        return 0
    return x ** 6 * -61.66 + x ** 5 * 201.1 + x ** 4 * -243.1 + x ** 3 * 130.2 + x ** 2 * -30.71 + x * 4.069


def sit_up_poly(x):
    if x == 1:
        return 0
    return x ** 6 * 23.19 + x ** 5 * -97.8 + x ** 4 * 145.4 + x ** 3 * -96.29 + x ** 2 * 24.46 + x * 1.119
