#!/usr/local/bin/python3

# Author: Vikram Bhagavatula
# Date: 2022-02-03
# Description: Homework 5 for Computer Vision

import sys
from tabulate import tabulate
from cv2 import cv2
from itertools import chain
from scipy.linalg import solve
import numpy as np
from skimage import io
from matplotlib import pyplot as plt
from matplotlib import cm

def drawEpipolarLine(point, right_image, fmat):
    hc_point = np.append(np.array(point), 1) # same point in homogenous coordinates

    print(f"{hc_point.shape=}")

    epiline = fmat @ hc_point # epiline in homogenous coordinates
    a, b, c = tuple(epiline[:3])

    slope = -a / b
    intercept = -c / b

    f = lambda x: slope*x + intercept

    # pair of endpoints outside the image
    y1 = int(f(0))
    y2 = int(f(right_image.shape[1])) # picks a point outside the image

    p1 = (0, y1)
    p2 = (int(right_image.shape[1]), y2)

    res = cv2.line(right_image, p1, p2, (0,255,0), 2)
    return res

def requestPoints(images, npoints, timeout=60):
    """
    Intakes in a collection of image objects, returns a routine that intakes a number of points,
    requests it from each image, and then yields the points from the image, one by one. The points are
    saved between runs, so if the same image pops up again in the collection on a separate run, the saved
    points are used instead of requesting them again.
    Example usage:

    >>> pt_collection = list(requestPoints([img1, img2], 8))
    >>> pts_img1 = pt_collection[0]
    >>> pts_img2 = pt_collection[2]
    
    """
    for img in images:
        plt.imshow(img)
        yield plt.ginput(npoints, timeout)

def epiline(file1, file2):
    img1 = io.imread(file1)
    img2 = io.imread(file2)

    pts1, pts2 = tuple(requestPoints((img1, img2), 8))[:2]

    fmat = cv2.findFundamentalMat(np.array(pts1), np.array(pts2), cv2.FM_8POINT)[0] # Uses 8-point algorithm to compute fundamental matrix
    print(fmat)

    pt = list(requestPoints([img1], 1))[0][0] # list() captures the list of points yielded by requestPoints, then we extract out the first element using [0] again
    pt = (int(pt[0]), int(pt[1]))
    print(pt)
    img2_eline = drawEpipolarLine(pt, img2, fmat)

    img1 = cv2.circle(img1, pt, radius=0, color=(0,255,0), thickness=2) # image annotated with point chosen

    res = np.concatenate((img1, img2_eline), 1)
    plt.imsave("result.jpg", res)
    # plt.imshow(np.concatenate((img1, res), 1))

def main():
    f1, f2 = sys.argv[1:3]
    res = epiline(f1, f2)

if __name__=="__main__":
    main()
