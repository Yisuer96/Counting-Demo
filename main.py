import os
import judging
import mapping
import utils
import shutil
from absl import app, flags

# deciding whether the action has begun
import waveform

action_config = {'push_up': [mapping.push_up_mapping, waveform.push_up_poly],
                 'pull_up': [mapping.pull_up_mapping, waveform.pull_up_poly],
                 'sit_up': [mapping.sit_up_mapping, waveform.sit_up_poly]}
t = 0.1
# threshold for judging whether the action is valid
T = 0.25

for save_dir in ["./output_images", "./output_jsons"]:
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
        os.mkdir(save_dir)
    else:
        os.mkdir(save_dir)

FLAGS = flags.FLAGS
flags.DEFINE_enum("category", "sit_up", ["push_up", "pull_up", "sit_up"], "action category to be counted.")
flags.DEFINE_string("path", "test/me_sit_up.mp4", "video path to be counted.")


def counting(argv):
    path = FLAGS.path
    config = action_config[FLAGS.category]
    r = 0
    f = []
    flag = [False, -1]
    skeleton_data = utils.skeleton_extraction("--video", path)
    for item in skeleton_data:
        # TODO:map result including frame number info
        y = config[0](item)
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
                f = utils.frame_regularization(f)
                # using a simple 1D average error judging
                if judging.ave_error_judging1d(f, config[1]) <= T:
                    r += 1
                f = []
                flag = [False, y[0]]
        elif flag[0] is True:
            f.append([y[0], f[-1][1]])
    if flag[0] is True:
        f.append([f[-1][0] + 1, 0])
        f = utils.frame_regularization(f)
        if judging.ave_error_judging1d(f, config[1]) <= T:
            r += 1
    print(r)


if __name__ == '__main__':
    app.run(counting)
