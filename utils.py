import math
import random
import sys
import numpy as np
import matplotlib.pyplot as plt

# open_path = "../openpose/build/python"

# Not tested code
# try:
#     sys.path.append(open_path)
#     from openpose import pyopenpose as op
# except ImportError as e:
#     print(
#         'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python '
#         'script in the right folder?')
#     raise e
# params = dict()
# params["model_folder"] = "./models/"
# params["face"] = False
# params["hand"] = False
# opWrapper = op.WrapperPython()
# opWrapper.configure(params)
# opWrapper.start()


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


def point_distance(a, b):
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))


# TODO: 返回[[x,y,c],[x,y,c],...]25个数组
def skeleton_extraction(video):
    r = []
    for i in range(25):
        r.append([i, i, random.random()])
    return r


# mat_plot poly_fitting
def simple_fitting(points):
    if len(points) > 0:
        x = []
        y = []
        for (index, item) in enumerate(points):
            x.append(item[0])
            y.append(item[1])
        x = np.array(x)
        y = np.array(y)
        f1 = np.polyfit(x, y, 3)
        p1 = np.poly1d(f1)
        print('p1 is :\n', p1)
        y_val = p1(x)  # 拟合y值
        print('yvals is :\n', y_val)
        # 绘图
        plot1 = plt.plot(x, y, 's', label='original values')
        plot2 = plt.plot(x, y_val, 'r', label='poly_fit values')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend(loc=4)  # 指定legend的位置右下角
        plt.title('poly_fitting')
        plt.show()
