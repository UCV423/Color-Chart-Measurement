import cv2
import numpy as np
from utils import *
#####  The data from https://www.xrite.com/service-support/new_color_specifications_for_colorchecker_sg_and_classic_charts
# CIE_lab_24 = [[37.54, 14.37, 14.92], [64.66, 19.27, 17.5], [49.32, -3.82, -22.54], [43.46, -12.74, 22.72], [54.94, 9.61, -24.79], [70.48, -32.26, -0.37],
#               [62.73, 35.83, 56.5], [39.43, 10.75, -45.17], [50.57, 48.64, 16.67], [30.1, 22.54, -20.87], [71.77, -24.13, 58.19], [71.51, 18.24, 67.37],
#               [28.37, 15.42, -49.8], [54.38, -39.72, 32.27], [42.43, 51.05, 28.62], [81.8, 2.67, 80.41], [50.63, 51.28, -14.12], [49.57, -29.71, -28.32],
#               [95.19, -1.03, 2.93], [81.29, -0.57, 0.44], [66.89, -0.75, -0.06], [50.76, -0.13, 0.14], [35.63, -0.46, -0.48], [20.64, 0.07, -0.46]]
#
# def rgb2lab(rgb):
#     r = rgb[0] / 255.0  # rgb range: 0 ~ 1
#     g = rgb[1] / 255.0
#     b = rgb[2] / 255.0
#
#     # gamma 2.2
#     if r > 0.04045:
#         r = pow((r + 0.055) / 1.055, 2.4)
#     else:
#         r = r / 12.92
#
#     if g > 0.04045:
#         g = pow((g + 0.055) / 1.055, 2.4)
#     else:
#         g = g / 12.92
#
#     if b > 0.04045:
#         b = pow((b + 0.055) / 1.055, 2.4)
#     else:
#         b = b / 12.92
#
#     # sRGB
#     X = r * 0.436052025 + g * 0.385081593 + b * 0.143087414
#     Y = r * 0.222491598 + g * 0.716886060 + b * 0.060621486
#     Z = r * 0.013929122 + g * 0.097097002 + b * 0.714185470
#
#     # XYZ range: 0~100
#     X = X * 100.000
#     Y = Y * 100.000
#     Z = Z * 100.000
#
#     # Reference White Point
#
#     ref_X = 96.4221
#     ref_Y = 100.000
#     ref_Z = 82.5211
#
#     X = X / ref_X
#     Y = Y / ref_Y
#     Z = Z / ref_Z
#
#     # Lab
#     if X > 0.008856:
#         X = pow(X, 1 / 3.000)
#     else:
#         X = (7.787 * X) + (16 / 116.000)
#
#     if Y > 0.008856:
#         Y = pow(Y, 1 / 3.000)
#     else:
#         Y = (7.787 * Y) + (16 / 116.000)
#
#     if Z > 0.008856:
#         Z = pow(Z, 1 / 3.000)
#     else:
#         Z = (7.787 * Z) + (16 / 116.000)
#
#     Lab_L = round((116.000 * Y) - 16.000, 2)
#     Lab_a = round(500.000 * (X - Y), 2)
#     Lab_b = round(200.000 * (Y - Z), 2)
#
#     return Lab_L, Lab_a, Lab_b


def color_difference(measure, ref):
    L = abs(measure[0] - ref[0])
    a = abs(measure[1] - ref[1])
    b = abs(measure[2] - ref[2])
    C = (a ** 2 + b ** 2) ** 0.5
    E = (a ** 2 + b ** 2 + L ** 2) ** 0.5
    return C, E


def draw_rect(img, lt, rb):
    point_color = (0, 255, 0)  # BGR
    thickness = 2
    lineType = 4
    result = cv2.rectangle(img, lt, rb, point_color, thickness, lineType)
    return result

def load_std_ref_LAB(c_type):
    global REF_LAB
    REF_LAB = []
    if c_type == "24":
        REF_LAB = CIE_lab_24
    else:
        assert True, "type error"

def cc_task(cc_img, scale=0.5):
    #####  The data from https://www.xrite.com/service-support/new_color_specifications_for_colorchecker_sg_and_classic_charts
    load_std_ref_LAB("24")
    h, w = cc_img.shape[0], cc_img.shape[1]

    h_block = (h / 4)
    w_block = (w / 6)
    center_points = []
    for y in range(1, 5):
        for x in range(1, 7):
            center_points.append([x * w_block, y * h_block])
    img_rect = cc_img
    img_rect_ = img_rect.copy()
    count = 0
    mean_C = 0
    mean_E = 0
    for c in center_points:
        c_w = c[0] - w_block / 2
        c_h = c[1] - h_block / 2
        lt = (int(c_w - (w_block / 2) * scale), int(c_h - (h_block / 2) * scale))
        rb = (int(c_w + (w_block / 2) * scale), int(c_h + (h_block / 2) * scale))

        img_rect_ = draw_rect(img_rect_, lt, rb)
        # print("lt, rb", lt, rb)
        cc_block = img_rect[lt[1]: rb[1], lt[0]: rb[0]]

        R_mean = int(np.mean(cc_block[:, :, 0]))
        G_mean = int(np.mean(cc_block[:, :, 1]))
        B_mean = int(np.mean(cc_block[:, :, 2]))

        RGB_m = [R_mean, G_mean, B_mean]
        LAB_m = rgb2lab(RGB_m)
        #print("LAB_m: ", LAB_m, "REF_LAB: ", REF_LAB[count])

        C, E = color_difference(LAB_m, REF_LAB[count])

        mean_C += C
        mean_E += E

        count += 1
    mean_C /= 24
    mean_E /= 24
    # print("C:{} | E:{} ".format(mean_C, mean_E))
    #print(mean_C, mean_E)
    return mean_C, mean_E, img_rect_