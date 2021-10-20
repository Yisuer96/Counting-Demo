# Preset waveform function for different action processes
import math

Pi = math.pi


def basic_sine(x):
    return (math.cos(-2 * Pi * x) + 1) / 2


def pull_up_poly(x):
    return 59.37 * x ** 6 - 202.2 * x ** 5 + 256.2 * x ** 4 - 140.6 * x ** 3 + 23.61 * x ** 2 + 3.681 * x - 0.01616


def push_up_poly(x):
    if x == 1 or x == 0:
        return 0
    return x ** 6 * -160.2 + x ** 5 * 488.3 + x ** 4 * -553.4 + x ** 3 * 283 + x ** 2 * -64.73 + x * 7.051 + 0.01927


def sit_up_poly(x):
    if x == 1 or x == 0:
        return 0
    r = x ** 6 * 9.664 + x ** 5 * -29.19 + x ** 4 * 28.05 + x ** 3 * -7.352 + x ** 2 * -5.963 + x * 4.738 + 0.06725
    return r


def test():
    for i in range(21):
        j = i / 20
        print(str([j, push_up_poly(j)]))


test()
