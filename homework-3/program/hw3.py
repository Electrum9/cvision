#!/usr/local/bin/python3

# Author: Vikram Bhagavatula
# Date: 2022-01-18
# Description: Homework 3

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

def requestPoints(img1, img2, npoints):
    """
    Intakes two image objects, prompts the user to select points on each image.
    """

    plt.imshow(img1)
    points_left = plt.ginput(npoints, timeout=60)

    plt.imshow(img2)
    points_right = plt.ginput(npoints, timeout=60)

    return (points_left, points_right)

def perspectiveCorrection(file, npoints="8"):
    """
    Performs "perspective correction" routine for part 1 of the homework.
    """
    npoints = int(npoints)
    img1 = io.imread(file)
    img2 = np.zeros(np.shape(img1)) # blank image takes on same dimensions/shape as img1
    
    filename = file.split('.')[0] # split around file extension, get name
    try:
        zipped_pts = np.load(f"{filename}.npy")
        
        pl = list(zipped_pts[0]) 
        pr = list(zipped_pts[1])
    except Exception as e:
        print(e)
        (pl, pr) = requestPoints(img1, img2, npoints) 
        # presents both given image and blank image
        np.save(f"{filename}.npy", np.array([pl, pr]), allow_pickle=True)
        
    print("Points")
    print(tabulate([pl, pr], tablefmt="latex"))
    H21 = homography(pl, pr)
    res = cv2.warpPerspective(img1, H21, (img1.shape[1], img1.shape[0]))
    
    return {"Original": img1, 
            "Result": res}

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
        (pl, pr) = requestPoints(img1, img2, npoints) # presents both given image and blank image
        print(f"{pl=}")
        np.save(f"{filename1}_to_{filename2}.npy", np.array([pl, pr]), allow_pickle=True)
    
    print("Points")
    print(tabulate(np.array([pl, pr]), tablefmt="latex"))
    H21 = homography(pl, pr)
    res = cv2.warpPerspective(img1, H21, (img1.shape[1], img1.shape[0]))
    
    return {"Source": img1, 
            "Target": img2, 
            "Result": res}

def displayImages(labeled_images):
    for (label, img) in labeled_images.items():
        plt.figure(label)
        plt.imshow(img)
    plt.show()
        
def main():
    """
    Usage: ./hw3.py [routine alias] [arg1] [arg2] [number of points=8]
    Examples: ./hw3.py cp 1.jpg 2.jpg 8
              ./hw3.py cp 1.jpg 2.jpg
              ./hw3.py pc 1.jpg 8
              ./hw3.py pc 1.jpg
    
    The number of points need not be specified -- it is by default 8.
    The program will save the points you select into *.npy files, so on subsequent runs it will load from these files and will not request user input. 
    To manually input the points again, you need to delete the *.npy files (use `make clean` to remove all *.npy files).
    """ 
    
    routine = { "pc" : (perspectiveCorrection, 2),
                "cp" : (convertPerspective, 3), 
              }
    # Dictionary that maps routine alias to (function, number of args)

    (curr_routine, args) = routine[sys.argv[1]]
    params = tuple(sys.argv[2:2+args])
    labeled_images = curr_routine(*params)
    displayImages(labeled_images)

if __name__== "__main__":
    main()
