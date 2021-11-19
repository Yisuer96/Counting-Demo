import shutil

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageSequence
import sys
import cv2
import os
from sys import platform
import argparse
from logger import Logger
import time

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/openpose/Release')
            os.environ['PATH'] = os.environ[
                                     'PATH'] + ';' + dir_path + '/openpose/x64/Release;' + dir_path + '/openpose/bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../python');
            from openpose import pyopenpose as op
    except ImportError as e:
        print(
            'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e


except Exception as e:
    print(e)
    sys.exit(-1)


def reformat_skeleton(skeleton):
    r = []
    t = []
    if len(skeleton) == 75:
        for index, item in enumerate(skeleton):
            t.append(item)
            if index % 3 == 2:
                r.append(t)
                t = []
        return r
    return -1


def skeleton_extraction(data_type="--image_dir", path="./openpose/media/", task=0):
    # test_path
    if os.path.exists('./logs/extract') is False:
        os.makedirs('./logs/extract')
    dt = time.strftime("./logs/extract/%Y_%m_%d_%H_%M", time.localtime())
    log = Logger(dt + '_extract.logs', level='debug')
    r = []
    # Flags
    parser = argparse.ArgumentParser()
    if data_type == '--video':
        parse_video(path)
        data_type = "--image_dir"
        path = path.split('.')[0]
    parser.add_argument(data_type, default=path,
                        help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")

    args = parser.parse_known_args()

    # Custom Params
    params = dict()
    params["model_folder"] = "./openpose/models/"

    # Add others in path?
    # for i in range(0, len(args[1])):
    #     curr_item = args[1][i]
    #     if i != len(args[1]) - 1:
    #         next_item = args[1][i + 1]
    #     else:
    #         next_item = "1"
    #     if "--" in curr_item and "--" in next_item:
    #         key = curr_item.replace('-', '')
    #         if key not in params:  params[key] = "1"
    #     elif "--" in curr_item and "--" not in next_item:
    #         key = curr_item.replace('-', '')
    #         if key not in params: params[key] = next_item

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Read frames on directory
    imagePaths = op.get_images_on_directory(args[0].image_dir)
    for f_num, imagePath in enumerate(imagePaths):
        # Process Image
        datum = op.Datum()
        imageToProcess = cv2.imread(imagePath)
        datum.cvInputData = imageToProcess
        log.logger.info(imagePath + ' is being extracted...')
        tick = time.time()
        opWrapper.emplaceAndPop([datum])

        tick = (time.time() - tick) * 1000
        log.logger.info(imagePath + ' has been extracted,took ' + str(tick) + 'ms.')
        save_prefix = "./count_cache/" if task == 1 else "./generate_cache/"
        # Save Image
        cv2.imwrite(save_prefix + f"output_images/{f_num}.jpg", datum.cvOutputData)
        # change output format
        skt_list = datum.poseKeypoints.tolist()
        # save result
        f = open(save_prefix + f"output_jsons/{f_num}.txt", "w")
        for skt in skt_list:
            for point_list in skt:
                for point in point_list:
                    f.write(str(point) + ' ')
                f.write("\n")
            f.write("\n")
        f.close()
        skt = datum.poseKeypoints.tolist()
        r.append([f_num, skt])
    return r


def load_skeletons(task):
    res = []
    frame = []
    skt = []
    save_prefix = "./count_cache/" if task == 1 else "./generate_cache/"
    for root, dirs, files in os.walk(save_prefix + "output_jsons"):
        f_sum = len(files)
        for f in range(f_sum):
            frame.append(f)
            temp = []
            f = open(root + '/' + str(f) + '.txt')
            for line in f.readlines():
                cos = line.split(" ")
                if len(cos) == 4:
                    skt.append([float(cos[0]), float(cos[1]), float(cos[2])])
                else:
                    temp.append(skt)
                    skt = []
            frame.append(temp)
            f.close()
            res.append(frame)
            frame = []
    return res


# mat_plot poly_fitting
def simple_fitting(points, degree):
    if len(points) > 0:
        x = []
        y = []
        for index, item in enumerate(points):
            x.append(item[0])
            y.append(item[1])
        x = np.array(x)
        y = np.array(y)
        f1 = np.polyfit(x, y, degree)
        p1 = np.poly1d(f1)
        print('p1 is :\n', p1)
        y_val = p1(x)  # 拟合y值
        print('y_val is :\n', y_val)
        # 绘图
        plot1 = plt.plot(x, y, 's', label='original values')
        plot2 = plt.plot(x, y_val, 'r', label='poly_fit values')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend(loc=4)  # 指定legend的位置右下角
        plt.title('poly_fitting')
        plt.show()


def trapezoidal_fitting(points, degree):
    if len(points) > 0:
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        flag = 0
        for index, item in enumerate(points):
            if item[1] < 1 and flag == 0:
                x1.append(item[0])
                y1.append(item[1])
            elif item[1] == 1 and flag == 0:
                print("Inflection 1: " + str(item[0]) + ".")
                x1.append(item[0])
                y1.append(item[1])
                flag = 1
            elif item[1] == 1 and flag == 1:
                if points[index + 1][1] != 1:
                    print("Inflection 1: " + str(item[0]) + ".")
                    x2.append(item[0])
                    y2.append(item[1])
                    flag = 2
            else:
                x2.append(item[0])
                y2.append(item[1])
        if len(x2) == 0:
            simple_fitting(points, degree)
            return
        x1 = np.array(x1)
        y1 = np.array(y1)
        x2 = np.array(x2)
        y2 = np.array(y2)
        f1 = np.polyfit(x1, y1, degree)
        f2 = np.polyfit(x2, y2, degree)
        p1 = np.poly1d(f1)
        p2 = np.poly1d(f2)
        print('p1 is :\n', p1)
        print('p2 is :\n', p2)
        y_val1 = p1(x1)
        y_val2 = p2(x2)
        plot1 = plt.plot(x1, y1, 's', label='original values 1')
        plot2 = plt.plot(x1, y_val1, 'r', label='poly_fit values 1')
        plot3 = plt.plot(x2, y2, 's', label='original values 2')
        plot4 = plt.plot(x2, y_val2, 'r', label='poly_fit values 2')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend(loc=4)  # 指定legend的位置右下角
        plt.title('trapezoidal_fitting')
        plt.show()


def frame_regularization(points):
    start = points[0][0]
    ratio = points[-1][0] - start
    for point in points:
        point[0] = (point[0] - start) / ratio
    return points


def parse_gif(gif_path):
    im = Image.open(gif_path)
    frames = ImageSequence.Iterator(im)
    file_name = gif_path.split(".")[0]
    index = 1
    pic_dir = "{0}".format(file_name)
    if os.path.isdir(pic_dir):
        shutil.rmtree(pic_dir)
    os.makedirs(pic_dir)
    for frame in frames:
        print("image %d: mode %s, size %s" % (index, frame.mode, frame.size))
        frame.save("%s/frame%d.png" % (file_name, index))
        index += 1


def parse_video(video_path, compress=True):
    video_capture = cv2.VideoCapture(video_path)
    f = 0
    file_name = video_path.split(".")[0]
    index = 1
    pic_dir = "{0}".format(file_name)
    if os.path.isdir(pic_dir):
        shutil.rmtree(pic_dir)
    os.makedirs(pic_dir)
    while True:
        res, frame = video_capture.read()
        if res:
            # sampling every 5 frames
            if f % 5 == 0:
                # resize to a lower 480p frame
                if compress:
                    s = frame.shape
                    if s[0] > 640 and s[1] > 480:
                        frame = cv2.resize(frame, (640, 480))
                path = pic_dir + '/' + str('%06d' % f) + '.jpg'
                cv2.imwrite(path, frame)
            f = f + 1
        else:
            video_capture.release()
            break


def insert_points(origin, new):
    res = []
    fo = 0
    fn = 0
    origin = origin[1:-1]
    while fo < len(origin) and fn < len(new):
        if origin[fo][0] < new[fn][0]:
            res.append(origin[fo])
            fo += 1
        else:
            res.append(new[fn])
            fn += 1
    for i in range(fn, len(new)):
        res.append(new[i])
    return res


def pic_avg_diff(img1, img2):
    img1 = cv2.imread(img1)
    img2 = cv2.imread(img2)
    # CV difference function, optimized but slower
    err = cv2.absdiff(img1, img2)
    # err = np.maximum(img1 - img2, img2 - img1)
    diff = np.sum(err)
    cv2.imshow('err', err)
    # print(dif f)
    cv2.waitKey(0)
    # plt.imshow(err)
    # plt.show()
    avg_diff = diff / (err.shape[0] * err.shape[1])
    return avg_diff
