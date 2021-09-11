import judging
import mapping
import utils

t = 0.25
T = 0.2
sample = None

def counting(video):
    r = 0
    f = []
    flag = False
    skeleton_data = utils.skeleton_extraction(video)
    for index, item in skeleton_data:
        y = mapping.test_mapping(item)
        y.append(index)
        deviation = abs(y[0])
        if flag is False and deviation >= t:
            flag = True
            f.append(y)
        elif flag is True and deviation >= t:
            f.append(y)
        elif flag is True and deviation < t:
            flag = False
            if judging.test_judging(f, judging.sin) >= T:
                r += 1
            f = []
    print(r)


if __name__ == '__main__':
    counting(sample)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
