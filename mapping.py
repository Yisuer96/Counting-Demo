# Mapping a skeleton data to a process value(2-D)

# Confidence threshold of skeleton point
# C = 0.6
import waveform

test_skeleton = [[0, 0, 0], [197.164, 161.491, 0.896455], [237.798, 158.156, 0.840285], [259.772, 124.262, 0.871383],
                 [253.03, 68.2592, 0.912764], [159.813, 161.534, 0.834573], [141.215, 125.88, 0.902222],
                 [147.987, 64.9346, 0.871515], [197.162, 288.63, 0.71238], [222.506, 288.636, 0.686935],
                 [212.342, 386.976, 0.880746], [205.54, 491.988, 0.811595], [173.407, 288.634, 0.675585],
                 [186.92, 388.62, 0.857565], [183.509, 486.939, 0.829572], [0, 0, 0], [0, 0, 0],
                 [220.871, 122.566, 0.908147], [178.456, 119.106, 0.884239], [183.535, 507.266, 0.575368],
                 [178.456, 505.561, 0.614999], [181.896, 497.058, 0.770747], [212.357, 514.067, 0.613764],
                 [212.334, 512.348, 0.639208], [203.833, 500.513, 0.782646]]


# def test_mapping(skeleton):
#     error = 0
#     for (index, item) in enumerate(skeleton):
#         if index % 3 == 2:
#             if item < 0.5:
#                 skeleton[index - 2] = skeleton[index - 1] = skeleton[index] = -1
#                 error += 0.04
#     return error

# def confident_point(point):
#     if point[2] > C:
#         return True
#     return False
def midpoint(points):
    x = 0
    y = 0
    n = len(points)
    for item in points:
        x += item[0]
        y += item[1]
    x /= n
    y /= n
    return [x, y]


# def head_center(skeleton):
#     if skeleton[0][3] >= 0.8:
#         return skeleton[0][:2]
#     elif skeleton[15][3] >= 0.6 and skeleton[16][3] >= 0.6:
#         return midpoint(skeleton[15], skeleton[16])
#     elif skeleton[17][3] >= 0.6 and skeleton[18][3] >= 0.6:
#         return midpoint(skeleton[17], skeleton[18])
#     else:
#         return -1


# simplest version mappings
def push_up_mapping(skeleton):
    return 0


def sit_up_mapping(skeleton):
    return 0


def pull_up_mapping(skeleton):
    i = abs(skeleton[4][0] - skeleton[7][0])
    # check the distance between two wrist is less than shoulder width
    if abs(skeleton[2][0] - skeleton[5][0]) * 1.5 >= i:
        p = skeleton[1][1] - midpoint([skeleton[4], skeleton[7]])[1]
        if p >= i * 1.5:
            print('Initial position.')
            return 0
        elif p <= 0:
            print('Pulled up.')
            return 1
        else:
            print(1 - p / i / 1.5)
            return 1 - p / i / 1.5
    print('Wrist distance too large.')
    return -1


pull_up_mapping(test_skeleton)
