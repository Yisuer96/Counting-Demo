# Judging a test wave is a qualified action or not
import utils
import waveform

sin = waveform.basic_sine


def ave_error_judging1d(start, sample, template):
    error = 0
    n = len(sample)
    p = sample[-1][0] - start
    for item in sample:
        basic = template((item[0] - start) / p)
        error += abs(item[1] - basic)
    error = error / n
    return error
