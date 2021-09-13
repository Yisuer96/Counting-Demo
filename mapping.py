# Mapping a skeleton data to a process value(2-D)
#Confidence threshold of skeleton point
C = 0.6

# def test_mapping(skeleton):
#     error = 0
#     for index, item in skeleton:
#         if index % 3 == 2:
#             if item < 0.5:
#                 skeleton[index - 2] = skeleton[index - 1] = skeleton[index] = -1
#                 error += 0.04
#     return error

def confident_point(point):
    if point[2]>C:
        return True
    return False

def headcenter(skeleton):
    head = [skeleton[0],skeleton[15],skeleton[16],skeleton[17],skeleton[18]]



def push_up_mapping(skeleton):
    return 0


def sit_up_mapping(skeleton):
    return 0


def pull_up_mapping(skeleton):
    return 0
