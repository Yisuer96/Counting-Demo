import os
import judging
import mapping
import utils
import shutil
from absl import app, flags
import waveform
from logger import Logger
import time

action_config = {'push_up': [mapping.push_up_mapping, waveform.push_up_poly],
                 'pull_up': [mapping.pull_up_mapping, waveform.pull_up_poly],
                 'sit_up': [mapping.sit_up_mapping, waveform.sit_up_poly]}

# Threshold for detecting whether the action has begun
t = 0.1
# threshold for judging whether the action is valid
T = 0.3

FLAGS = flags.FLAGS
# Choose the action category to be counted
flags.DEFINE_enum("category", "sit_up", ["push_up", "pull_up", "sit_up"], "action category to be counted.")
# Choose video path(only video file is supported by now)
flags.DEFINE_string("path", "test/me_sit_up.mp4", "video path to be counted.")


def counting(argv):
    dt = time.strftime("%Y_%m_%d_%H_%M", time.localtime())
    log = Logger(dt + '_count.log', level='debug')
    path = FLAGS.path
    config = action_config[FLAGS.category]
    mapping_function = config[0]
    waveform_function = config[1]
    r = 0
    f = []
    flag = [False, -1]
    # DEBUG: Use cached skeleton data
    skeleton_data = utils.load_skeletons(1)
    # DEBUG: To extract new skeletons
    # for save_dir in ["./count_cache/output_images", "./count_cache/output_jsons"]:
    #     if os.path.exists(save_dir):
    #         shutil.rmtree(save_dir)
    #         os.makedirs(save_dir)
    #     else:
    #         os.makedirs(save_dir)
    # tick = time.time()
    # log.logger.info('Start skeleton extraction.')
    # skeleton_data = utils.skeleton_extraction("--video", path, 1)
    # tick = (time.time() - tick) * 1000
    # log.logger.info('Skeleton fetched, spent ' + str(tick) + 'ms.')

    tick = time.time()
    log.logger.info('Counting start.')
    for item in skeleton_data:
        y = mapping_function(item)
        log.logger.debug('Frame ' + str(y[0]) + ' mapped, status value = ' + str(y[1]))
        if y[1] is not -1:
            deviation = abs(y[1])
            if flag[0] is False and deviation < t:
                flag[1] = y[0]
            elif flag[0] is False and deviation >= t:
                log.logger.debug('Action ' + str(r + 1) + ' started.')
                flag[0] = True
                f.append([flag[1], 0])
                f.append(y)
            elif flag[0] is True and deviation >= t:
                f.append(y)
            elif flag[0] is True and deviation < t:
                f.append([y[0], 0])
                log.logger.debug('Action' + str(r + 1) + ' ended, judging...')
                f = utils.frame_regularization(f)
                # using a simple 1D average error judging
                e = judging.ave_error_judging1d(f, waveform_function)
                if e <= T:
                    r += 1
                    log.logger.debug(
                        'Action ' + str(r) + ' is valid with error:' + str(e) + ', count+1.\nProcess set: ' + str(f))
                else:
                    log.logger.debug(
                        'Action ' + str(r + 1) + ' is invalid with error = ' + str(e) + '.\nProcess set: ' + str(f))
                f = []
                flag = [False, y[0]]
        elif flag[0] is True:
            log.logger.debug(
                'Skeleton of frame ' + str(y[0]) + ' missed during an action, follows last valid status value:' + str(
                    f[-1][1]))
            f.append([y[0], f[-1][1]])
    if flag[0] is True:
        f.append([f[-1][0] + 1, 0])
        f = utils.frame_regularization(f)
        if judging.ave_error_judging1d(f, waveform_function) <= T:
            r += 1
            log.logger.debug(
                'At the end of this video, an action is basically finished, so we count on this one.\n' + str(
                    r) + ': ' + str(f))
    log.logger.info('Counting result is ' + str(r) + '.')
    tick = (time.time() - tick) * 1000
    log.logger.info('Counting process spent ' + str(tick) + 'ms.')


if __name__ == '__main__':
    app.run(counting)
