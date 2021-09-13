import math
import random
import sys

open_path = "../openpose/build/python"

#Not tested code
try:
    sys.path.append(open_path)
    from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e
params = dict()
params["model_folder"] = "./models/"
params["face"] = False
params["hand"] = False
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

def point_distance(a, b):
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))

# TODO: 返回[[x,y,c],[x,y,c],...]25个数组
def skeleton_extraction(video):
    r = []
    for i in range(25):
        r.append([i, i, random.random()])
    return r
