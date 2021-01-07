import random
import math

import numpy as np

def distance(x, y, a, b, c):
    return abs(a * x + b * y + c) / math.sqrt(a * a + b * b)


def get_coefficients(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1

    return a, b, c


def ransac(input_data, iterations=10, threshold=0.1):
    inliers = []
    outliers = []
    a, b, c = 0, 0, 0

    iteration_number = 0

    while iteration_number < iterations:
        tmp_inliers = []
        tmp_outliers = []

        data = input_data.copy()
        random.shuffle(data)

        random_point_1 = data.pop()
        random_point_2 = data.pop()

        tmp_a, tmp_b, tmp_c = get_coefficients(random_point_1[0],
                           random_point_1[1],
                           random_point_2[0],
                           random_point_2[1])

        for point in data:
            d = distance(point[0], point[1], tmp_a, tmp_b, tmp_c)

            if d < threshold:
                tmp_inliers.append(point)
            else:
                tmp_outliers.append(point)

        if len(inliers) < len(tmp_inliers):
            inliers = tmp_inliers
            outliers = tmp_outliers
            a, b, c =  tmp_a,tmp_b, tmp_c

        iteration_number += 1

    return a, b, c, inliers, outliers
