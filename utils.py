import shutil

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageSequence
import sys
import cv2
import os
from sys import platform
import argparse

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
def skeleton_extraction(data_type="--image_dir", path="./openpose/media/", skeleton_filter="first"):
    # test_path
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
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1]) - 1:
            next_item = args[1][i + 1]
        else:
            next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-', '')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-', '')
            if key not in params: params[key] = next_item

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
        print('Image ' + imagePath + ' is on processing...')
        opWrapper.emplaceAndPop([datum])

        # Save Image
        cv2.imwrite(f"./output_images/{f_num}.jpg", datum.cvOutputData)
        # change output format
        skt = datum.poseKeypoints[0].tolist()
        # save result
        f = open(f"./output_jsons/{f_num}.txt", "w")
        for point_list in skt:
            for point in point_list:
                f.write(str(point) + ' ')
            f.write("\n")
        f.close()
        if skeleton_filter == "first":
            skt = datum.poseKeypoints[0].tolist()
        elif skeleton_filter == "none":
            skt = datum.poseKeypoints.tolist()
        r.append([f_num, skt])
    return r


# mat_plot poly_fitting
def simple_fitting(points, degree):
    if len(points) > 0:
        x = []
        y = []
        for (index, item) in enumerate(points):
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


def parse_video(video_path):
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
            if f % 5 == 0:
                cv2.imwrite(pic_dir + "/" + str('%06d' % f) + '.jpg', frame)
            f = f + 1
        else:
            print('end')
            break
