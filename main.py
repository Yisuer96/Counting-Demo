import os
import judging
import mapping
import utils
import shutil
from absl import app, flags
import waveform

action_config = {'push_up': [mapping.push_up_mapping, waveform.push_up_poly, "first"],
                 'pull_up': [mapping.pull_up_mapping, waveform.pull_up_poly, "first"],
                 'sit_up': [mapping.sit_up_mapping, waveform.test_wave, "none"]}

# Threshold for detecting whether the action has begun
t = 0.1
# threshold for judging whether the action is valid
T = 0.25

FLAGS = flags.FLAGS
# Choose the action category to be counted
flags.DEFINE_enum("category", "sit_up", ["push_up", "pull_up", "sit_up"], "action category to be counted.")
# Choose video path(only video file is supported by now)
flags.DEFINE_string("path", "test/me_sit_up.mp4", "video path to be counted.")


def counting(argv):
    path = FLAGS.path
    config = action_config[FLAGS.category]
    mapping_function = config[0]
    waveform_function = config[1]
    skt_filter = config[2]
    r = 0
    f = []
    flag = [False, -1]
    # DEBUG: Use cached skeleton data
    skeleton_data = utils.load_skeletons()
    # DEBUG: To extract new skeletons
    # for save_dir in ["./output_images", "./output_jsons"]:
    #     if os.path.exists(save_dir):
    #         shutil.rmtree(save_dir)
    #         os.mkdir(save_dir)
    #     else:
    #         os.mkdir(save_dir)
    # skeleton_data = utils.skeleton_extraction("--video", path, skt_filter)
    # skeleton fetched
    for item in skeleton_data:
        y = mapping_function(item)
        print("Mapped result: " + str(y))
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
                if judging.ave_error_judging1d(f, waveform_function) <= T:
                    r += 1
                    print(str(r) + ": " + str(f))
                print(str(judging.ave_error_judging1d(f, waveform_function)) + ": " + str(f))
                f = []
                flag = [False, y[0]]
        elif flag[0] is True:
            f.append([y[0], f[-1][1]])
    if flag[0] is True:
        f.append([f[-1][0] + 1, 0])
        f = utils.frame_regularization(f)
        if judging.ave_error_judging1d(f, waveform_function) <= T:
            r += 1
    print(r)


if __name__ == '__main__':
    app.run(counting)
