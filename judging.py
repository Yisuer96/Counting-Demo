# Judging a test wave is a qualified action or not
import utils
import waveform

sin = waveform.basic_sine


def test_judging(sample, template):
    error = 0
    n = len(sample)
    for item in sample:
        basic = template(item[1])
        error += abs(item[0]-basic)
    error = error / n
    return error
