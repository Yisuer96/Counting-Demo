import mapping
import utils

# deciding whether the action has begun
t = 0.1
# threshold for judging whether the action is valid
sample = None
mapper = mapping.pull_up_mapping


def generate(videos):
    for video in videos:
        f = []
        p = []
        flag = [False, -1]
        skeleton_data = utils.skeleton_extraction(video)
        for item in skeleton_data:
            y = mapper(item)
            if y is not -1:
                deviation = abs(y[1])
                if flag[0] is False and deviation < t:
                    flag[1] = y[0]
                elif flag[0] is False and deviation >= t:
                    flag[0] = True
                    f.append(y)
                elif flag is True and deviation >= t:
                    f.append(y)
                elif flag is True and deviation < t:
                    f.append(y)
                    p += utils.frame_regularization(f)
                    f = []
                    flag = [False, -1]
    utils.simple_fitting(p)


if __name__ == '__main__':
    generate(sample)
