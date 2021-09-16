import judging
import mapping
import utils

# deciding whether the action has begun
t = 0.1
# threshold for judging whether the action is valid
T = 0.15
sample = None
mapper = mapping.pull_up_mapping


def counting(video):
    r = 0
    f = []
    flag = [False, -1]
    # TODO:make sure openpose python works
    skeleton_data = utils.skeleton_extraction(video)
    for item in skeleton_data:
        # TODO:map result including frame number info
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
                # using a simple 1D average error judging
                if judging.ave_error_judging1d(flag[1], f, judging.sin) >= T:
                    r += 1
                f = []
                flag = [False, -1]
    print(r)


if __name__ == '__main__':
    counting(sample)
