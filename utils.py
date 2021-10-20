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


# TODO: 支持通过data_type选择数据的格式为video or image_dir
def skeleton_extraction(data_type="--image_dir", path="./openpose/media/"):
    # test_path
    dt = time.strftime("%Y_%m_%d_%H_%M", time.localtime())
    log = Logger(dt + '_extract.log', level='debug')
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
        # Save Image
        cv2.imwrite(f"./output_images/{f_num}.jpg", datum.cvOutputData)
        # change output format
        skt_list = datum.poseKeypoints.tolist()
        # save result
        f = open(f"./output_jsons/{f_num}.txt", "w")
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


def load_skeletons():
    res = []
    frame = []
    skt = []
    for root, dirs, files in os.walk("./output_jsons"):
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


trapezoidal_fitting([[0.0, 0], [0.027777777777777776, 0.22865113226106148], [0.05555555555555555, 0.2462913107639152],
                     [0.08333333333333333, 0.2639415078646734], [0.1111111111111111, 0.2817156195140196],
                     [0.1388888888888889, 0.3228756567128276], [0.16666666666666666, 0.3332867102434083],
                     [0.19444444444444445, 0.38201334472837767], [0.2222222222222222, 0.41259080173385776],
                     [0.25, 0.46758996252914553], [0.2777777777777778, 0.5138624018182933],
                     [0.3055555555555556, 0.562204282238249], [0.3333333333333333, 0.6105465580762421],
                     [0.3611111111111111, 0.6539667015376911], [0.3888888888888889, 0.7206647864457756],
                     [0.4166666666666667, 0.7419042402572067], [0.4444444444444444, 0.8041099869346701],
                     [0.4722222222222222, 0.8331573576161039], [0.5, 1], [0.5277777777777778, 1],
                     [0.5555555555555556, 1], [0.5833333333333334, 0.816665854973857],
                     [0.6111111111111112, 0.7915669336971238], [0.6388888888888888, 0.7456495720855176],
                     [0.6666666666666666, 0.703490844793719], [0.6944444444444444, 0.655269703394147],
                     [0.7222222222222222, 0.6184718496736847], [0.75, 0.5778881016702412],
                     [0.7777777777777778, 0.5233619406275448], [0.8055555555555556, 0.46766894268866177],
                     [0.8333333333333334, 0.4108778421413818], [0.8611111111111112, 0.38809019044852244],
                     [0.8888888888888888, 0.333170687368359], [0.9166666666666666, 0.322760514375086],
                     [0.9444444444444444, 0.2873543139493414], [0.9722222222222222, 0.2611814040809157], [1.0, 0]], 6)
