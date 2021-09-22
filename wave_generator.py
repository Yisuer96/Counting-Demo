import os

import mapping
import utils

# deciding whether the action has begun
t = 0.1
# threshold for judging whether the action is valid
sample = "temp"
mapper = mapping.push_up_mapping


def generate(videos):
    for dir_path, dir_names, file_names in os.walk(videos):
        for path in dir_names:
            f = []
            p = []
            flag = [False, -1]
            skeleton_data = utils.skeleton_extraction(videos + "/" + path)
            for item in skeleton_data:
                y = mapper(item)
                if y[1] is not -1:
                    deviation = abs(y[1])
                    if flag[0] is False and deviation < t:
                        flag[1] = y[0]
                    elif flag[0] is False and deviation >= t:
                        flag[0] = True
                        f.append([flag[1], 0])
                        f.append(y)
                    elif flag[0] is True and deviation >= t:
                        f.append(y)
                    elif flag[0] is True and deviation < t:
                        f.append([y[0], 0])
                        p += utils.frame_regularization(f)
                        print(p)
                        f = []
                        flag = [False, -1]
                elif flag[0] is True:
                    f.append([y[0], f[-1][1]])
            # utils.simple_fitting(p, 4)
    utils.simple_fitting(p, 6)


if __name__ == '__main__':
    generate(sample)
