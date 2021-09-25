# Mapping a skeleton data to a process value(2-D)

# Confidence threshold of skeleton point
# C = 0.6
import waveform
import math
import math

test_skeleton = [7,
                 [[0, 0, 0], [197.164, 161.491, 0.896455], [237.798, 158.156, 0.840285], [259.772, 124.262, 0.871383],
                  [253.03, 68.2592, 0.912764], [159.813, 161.534, 0.834573], [141.215, 125.88, 0.902222],
                  [147.987, 64.9346, 0.871515], [197.162, 288.63, 0.71238], [222.506, 288.636, 0.686935],
                  [212.342, 386.976, 0.880746], [205.54, 491.988, 0.811595], [173.407, 288.634, 0.675585],
                  [186.92, 388.62, 0.857565], [183.509, 486.939, 0.829572], [0, 0, 0], [0, 0, 0],
                  [220.871, 122.566, 0.908147], [178.456, 119.106, 0.884239], [183.535, 507.266, 0.575368],
                  [178.456, 505.561, 0.614999], [181.896, 497.058, 0.770747], [212.357, 514.067, 0.613764],
                  [212.334, 512.348, 0.639208], [203.833, 500.513, 0.782646]]]

pull_up_flag = False
max_angle = 0
min_angle = 180
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


def point_distance(a, b):
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))


# def head_center(skeleton):
#     if skeleton[0][3] >= 0.8:
#         return skeleton[0][:2]
#     elif skeleton[15][3] >= 0.6 and skeleton[16][3] >= 0.6:
#         return midpoint([skeleton[15], skeleton[16]])
#     elif skeleton[17][3] >= 0.6 and skeleton[18][3] >= 0.6:
#         return midpoint([skeleton[17], skeleton[18]])
#     else:
#         return -1


# simplest version mappings
def push_up_mapping(skeleton):
    print('Confidence:' + str(skeleton[1][8][2]) + ',' + str(skeleton[1][21][2]) + ',' + str(skeleton[1][24][2]))
    if skeleton[1][8][2] > 0:
        fulcrum = skeleton[1][8]
    elif skeleton[1][21][2] > 0 and skeleton[1][24][2] > 0:
        fulcrum = midpoint([skeleton[1][21], skeleton[1][24]])
    else:
        return [skeleton[0], -1]
    h = abs(fulcrum[1] - skeleton[1][1][1])
    k = point_distance(fulcrum, skeleton[1][1])
    i = h / k
    if i >= 0.25:
        print([skeleton[0], 0])
        return [skeleton[0], 0]
    elif i <= 0.05:
        print([skeleton[0], 1])
        return [skeleton[0], 1]
    else:
        print([skeleton[0], 1 - i / 0.25])
        return [skeleton[0], 1 - i / 0.25]


def sit_up_mapping(skeleton):
    # if one people captured by
    if len(skeleton[1][0]) == 3 and sit_up_pose(skeleton[1]) is False:
        return [skeleton[0], -1]
    elif len(skeleton[1]) == 2:
        if sit_up_pose(skeleton[1][0]):
            skeleton = [skeleton[0], skeleton[1][0]]
        elif sit_up_pose(skeleton[1][1]):
            skeleton = [skeleton[0], skeleton[1][1]]
        else:
            return [skeleton[0], -1]
    else:
        return [skeleton[0], -1]
    h = skeleton[1][8][1] - skeleton[1][1][1]
    k = point_distance(skeleton[1][8], skeleton[1][1])
    i = h / k
    if i <= 0:
        return [skeleton[0], 0]
    elif i >= 0.9:
        return [skeleton[0], 1]
    else:
        return [skeleton[0], i]


def pull_up_mapping(skeleton):
    global pull_up_flag, max_angle, min_angle
    # print(skeleton)
    i = abs(skeleton[1][4][0] - skeleton[1][7][0])
    # check the distance between two wrist is less than shoulder width
    if abs(skeleton[1][2][0] - skeleton[1][5][0]) * 3 >= i:
        p = skeleton[1][1][1] - midpoint([skeleton[1][4], skeleton[1][7]])[1]
        angle = compute_angle(skeleton[1][3], skeleton[1][2], skeleton[1][3], skeleton[1][4])
        max_angle = max(max_angle, angle)
        min_angle = min(min_angle, angle)
        # print("p: ", p)
        if angle > 150:
            pull_up_flag = False
            print('Initial position.')
            return [skeleton[0], 0]
        elif angle <= 50:
            if pull_up_flag is False:
                pull_up_flag = True
                print('Pulled up.')
                return [skeleton[0], 1]
            else:
                return [skeleton[0], 1]
        else:
            pull_up_flag = False
            # print(1 - angle / max_angle)
            return [skeleton[0], 1 - (angle - 50) / 100]
    print('Wrist distance too large.')
    return -1


# pull_up_mapping(test_skeleton)
def sit_up_pose(skeleton):
    if skeleton[8][2] > 0:
        h = skeleton[8]
    elif skeleton[9][2] * skeleton[12][2] > 0:
        h = midpoint([skeleton[9], skeleton[12]])
    else:
        return False
    if skeleton[10][2] * skeleton[13][2] > 0:
        i = midpoint([skeleton[10], skeleton[13]])
    else:
        return False
    for j in [[skeleton[11], skeleton[14]], [skeleton[21], skeleton[24]], [skeleton[19], skeleton[22]],
              [skeleton[20], skeleton[23]]]:
        if j[0][2] * j[1][2] > 0:
            j = midpoint([j[0], j[1]])
            break
        elif j == [skeleton[20], skeleton[23]]:
            return False
    if point_distance(h, j) / abs(h[1] - j[1]) < 10:
        return False
    if (h[0] - i[0]) * (i[0] - j[0]) < 0:
        return False
    if 1 <= abs(h[1] - j[1]) / abs(i[0] - (h[0] + j[0]) / 2) <= 4:
        return True
    return False


def compute_angle(p1, p2, p3, p4):
    dx1 = p2[0] - p1[0]
    dy1 = p2[1] - p1[1]
    dx2 = p4[0] - p3[0]
    dy2 = p4[1] - p3[1]
    angle1 = math.atan2(dy1, dx1)
    angle1 = int(angle1 * 180/math.pi)
    # print(angle1)
    angle2 = math.atan2(dy2, dx2)
    angle2 = int(angle2 * 180/math.pi)
    # print(angle2)
    if angle1*angle2 >= 0:
        included_angle = abs(angle1-angle2)
    else:
        included_angle = abs(angle1) + abs(angle2)
        if included_angle > 180:
            included_angle = 360 - included_angle
    return included_angle

