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

def homography(p1, p2):
    def getSysEqns(a, b):
        """
        Returns back pair of system of equations (rows of a matrix) 
        corresponding to the point pair.
        """
        (xa, ya) = a
        (xb, yb) = b

        row1 = [xa, ya, 1, 0, 0, 0, -xb*xa, -ya*xb]
        row2 = [0, 0, 0, xa, ya, 1, -xa*yb, -ya*yb]

        return [row1, row2]

    concatMap = lambda f, x: list(chain.from_iterable(map(f, x)))
    # Maps over x, producing a bunch of iterables (lists) and 
    # then chain will yield the values from each one in the given order
    point_pairs = zip(p1, p2)

    A = np.array(concatMap(lambda p: getSysEqns(*p), point_pairs)) 
    # Entire system of eqns assembled from pairs of systems of 
    # equations for each point pair
    b = np.array(concatMap(list, p2))
    # p2 consists of points (x', y') and the like, 
    # so we convert all pairs to lists, concatenate them, and form an array
    h = np.append(np.linalg.lstsq(A, b)[0], 1)
    H = np.reshape(h, (3, 3))
    print("H matrix")
    print(tabulate(H, tablefmt="latex"))
    return H

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
    """
    for img in images:
        plt.imshow(img)
        yield plt.ginput(npoints, timeout)

def epiline(file1, file2):
    img1 = io.imread(file1)
    img2 = io.imread(file2)

    filename1 = file1.split('.')[0] # split around file extension, get name
    filename2 = file2.split('.')[0] # split around file extension, get name

    try:
        zipped_pts = np.load(f"{filename1}_epi_{filename2}.npy") # zipped_points is an array with two rows consisting of tuples (requires enabling pickling to save them)
        pts1 = zipped_pts[0]
        pts2 = zipped_pts[1]
    except Exception as e:
        print(e)
        # (p1, p2) = requestPoints((img1, img2), 8) # presents both given image and blank image
        pts1, pts2 = tuple(requestPoints((img1, img2), 8))[:2]
        savename = f"{filename1}_epi_{filename2}.npy"
        np.save(savename, np.array([pts1, pts2]), allow_pickle=True)


    fmat = cv2.findFundamentalMat(np.array(pts1), np.array(pts2), cv2.FM_8POINT)[0] # Uses 8-point algorithm to compute fundamental matrix
    print(fmat)

    pt = list(requestPoints([img1], 1))[0][0] # list() captures the list of points yielded by requestPoints, then we extract out the first element using [0] again
    pt = (int(pt[0]), int(pt[1]))
    print(pt)
    img2_eline = drawEpipolarLine(pt, img2, fmat)

    img1 = cv2.circle(img1, pt, radius=0, color=(0,255,0), thickness=5) # image annotated with point chosen

    res = np.concatenate((img1, img2_eline), 1)
    # plt.imsave("result.jpg", res)
    return {"Result": res}
    # plt.imshow(np.concatenate((img1, res), 1))

def convertPerspective(file1, file2, npoints="8"):
    """
    Performs "convert perspective" routine for part 2 of the homework.
    """
    npoints = int(npoints)
    img1 = io.imread(file1)
    img2 = io.imread(file2)

    filename1 = file1.split('.')[0] # split around file extension, get name
    filename2 = file2.split('.')[0] # split around file extension, get name

    try:
        zipped_pts = np.load(f"{filename1}_to_{filename2}.npy") # zipped_points is an array with two rows consisting of tuples (requires enabling pickling to save them)
        pl = zipped_pts[0]
        pr = zipped_pts[1]
    except Exception as e:
        print(e)
        (pl, pr) = tuple(requestPoints((img1, img2), npoints))[:2] # presents both given image and blank image
        print(f"{pl=}")
        np.save(f"{filename1}_to_{filename2}.npy", np.array([pl, pr]), allow_pickle=True)

    print("Points")
    # print(tabulate(np.array([pl, pr]), tablefmt="latex"))
    print(np.array([pl, pr]))
    H21 = homography(pl, pr)
    res = cv2.warpPerspective(img1, H21, (img1.shape[1], img1.shape[0]))

    return {"Source": img1,
            "Target": img2,
            "Result": res}

def main():
    f1, f2 = sys.argv[1:3]
    res = epiline(f1, f2)

def displayImages(labeled_images):
    for (label, img) in labeled_images.items():
        plt.figure(label)
        plt.imshow(img)
    plt.show()

def main():
    """
    Usage: ./hw3.py [routine alias] [arg1] [arg2] [number of points=8]
    The program will save the points you select into *.npy files, so on subsequent runs it will load from these files and will not request user input.
    To manually input the points again, you need to delete the *.npy files (use `make clean` to remove all *.npy files).
    """

    routine = { "ep" : (epiline, 2),
                "cp" : (convertPerspective, 2),
              }
    # Dictionary that maps routine alias to (function, number of args)

    (curr_routine, args) = routine[sys.argv[1]]
    params = tuple(sys.argv[2:2+args])
    labeled_images = curr_routine(*params)
    displayImages(labeled_images)

if __name__=="__main__":
    main()
