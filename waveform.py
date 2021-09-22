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


def push_up_poly(x):
    if x == 1:
        return 0
    return x ** 6 * -61.66 + x ** 5 * 201.1 + x ** 4 * -243.1 + x ** 3 * 130.2 + x ** 2 * -30.71 + x * 4.069

print(push_up_poly(0.5))
