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


def push_up_trapezoidal(x=-1):
    if x == -1:
        return []
    if x == 0 or x == 1:
        return 0
    elif 0.5 <= x <= 5 / 9:
        return 1
    elif 0 < x < 0.5:
        return x ** 6 * -892.6 + x ** 5 * 1973 + x ** 4 * -1580 + x ** 3 * 585.5 + x ** 2 * -101.6 + x * 8.453 + 0.01701
    else:
        return x ** 6 * -2595.86 + x ** 5 * 10783.28 + x ** 4 * -18231.43 + x ** 3 * 15981.01 + x ** 2 * -7603.91 + x * 1838.06 + -171.127


def sit_up_trapezoidal(x=-1):
    if x == -1:
        return []
    if x == 0 or x == 1:
        return 0
    elif 0.304348 <= x <= 0.617647:
        return 1
    elif 0 < x < 0.304348:
        return x ** 6 * -71303.5 + x ** 5 * 72999.67 + x ** 4 * -28683.69 + x ** 3 * 5391.68 + x ** 2 * -492.011 + x * 21.9812 + -0.011
    else:
        return x ** 6 * -4665.52 + x ** 5 * 22197.315 + x ** 4 * -43730.55 + x ** 3 * 45662.286 + x ** 2 * -26659.22 + x * 8253.5 + -1057.787

# def test():
#     for i in range(21):
#         j = i / 20
#         print(str([j, sit_up_trapezoidal(j)]))
#
#
# test()
