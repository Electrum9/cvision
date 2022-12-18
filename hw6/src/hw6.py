#!/usr/local/bin/python3

# Author: Vikram Bhagavatula
# Date: 2022-02-18
# Description: Homework 6 program

import sys
from cv2 import cv2
from itertools import *
from functools import *
import numpy as np
from skimage import io
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter
from matplotlib import pyplot as plt
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

# New type defined so I can have a priority queue for points, priority being the output of the Harris CRF
@dataclass(order=True)
class PrioritizedPoint:
    priority: float
    point: Any=field(compare=False)

    def toPoint(self):
        return self.point

def harris_corner_detector(img, num_candidates):
    """
    Finds the top n candidate corner points in the given grayscale image.
    """
    num_candidates = int(num_candidates)
    def corner_response(ls_mtx, k=0.05):
        """
        Computes the CRF (corner response function) for a given local structure
        matrix (ls_mtx).
        """
        return np.linalg.det(ls_mtx) - k*(np.trace(ls_mtx)**2)

    print(f"{np.shape(img)=}")
    (rows, cols) = np.shape(img)

    # Differentiation stage
    print("Differentiation stage")
    derivative_x = cv2.convertScaleAbs(cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize = 3))
    derivative_y = cv2.convertScaleAbs(cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize = 3))

    # Corner detection stage
    print("Corner detection stage")
    # corner_candidates = np.zeros((rows, cols))
    corner_candidates = PriorityQueue() # priority queue for storing all candidates
    best = []
    for i in range(0, rows):
        for j in range(0, cols):
            # ls_mtx = np.zeros((2,2)) # local structure matrix
            # for u in range(-1,2): # sweep around in 3x3 window
            #     for v in range(-1,2):
            dx = derivative_x[i][j]
            dy = derivative_y[i][j]
            ls_mtx =  np.array([[dx**2, dx*dy],
                                [dx*dy, dy**2]])
            cr = corner_response(ls_mtx)

            print(f"{cr=}")
            if cr > 0: # corner response must be positive
                print(f"{(j,i)=}")
                corner_candidates.put(PrioritizedPoint(-cr, (j,i)))
                # best.append((j,i))
                # corner_candidates.put(PrioritizedPoint(-cr, (j,i)))

    # Find N corner candidates
    # best = sorted(pts, lambda p: p[0], reverse=True)
    for i in range(num_candidates):
        if corner_candidates.empty():
            break
        best.append(corner_candidates.get().toPoint())

    print(f"{best=}")
    return best

def iterate(f, seed):
    """
    Repeatedly applies f to seed, producing a stream of values x, f(x), f(f(x)), f(f(f(x))), ...
    """
    curr = seed
    while True:
        yield curr
        curr = f(curr)

def gaussian_pyramid(file, layers=4):
    # img = cv2.GaussianBlur(img, (3,3),0)
    img = cv2.imread(file)
    gray = np.float32(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    smooth_and_sub = lambda x: cv2.resize(cv2.GaussianBlur(x, (3,3), 0), (0,0), fx=0.5, fy=0.5)
    pyramid = iterate(smooth_and_sub, gray)
    return dict(zip(map(str, range(layers)), islice(pyramid, layers)))

def laplacian_pyramid(file, layers=5):
    # img = cv2.imread(file)
    img = cv2.imread(file)
    gray = np.float32(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

    pyramid = [gray]

    for i in range(layers):
        blurred = cv2.GaussianBlur(gray, (3,3), 0)
        last = gray - blurred
        pyramid.append(last)
        gray = cv2.resize(blurred, (0,0), fx=0.5, fy=0.5)

    labels = map(str, range(layers))
    cropped = pyramid[:layers]
    return dict(zip(labels, cropped))

def corner_detector(file, num_candidates=20):
    # img = cv2.cvtColor(cv2.imread(file, cv2.IMREAD_COLOR), cv2.COLOR_BGR2GRAY)
    img = cv2.imread(file)
    img = cv2.GaussianBlur(img, (3,3),0)
    filename = file.split('.')[0] # split around file extension, get name
    # plt.imshow(img)

    print(f"reading in {filename}")

    try:
        corners = np.load(f"{filename}_corners.npy")
    except Exception as e:
        print(e)
        # (p1, p2) = requestPoints((img1, img2), 8) # presents both given image and blank image
        gray = np.float32(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        corners = harris_corner_detector(gray, num_candidates)
        savename = f"{filename}_corners.npy"
        np.save(savename, np.array(corners))
    for c in corners:
        img = cv2.circle(img, c, radius=0, color=(0,255,0), thickness=5) # image annotated with point chosen

    return {"Result": img}

def displayImages(labeled_images):
    for (label, img) in labeled_images.items():
        plt.figure(label)
        plt.imshow(img, cmap='Greys_r')
    plt.show()

def main():
    """
    Usage: ./hw3.py [routine alias] [arg1] [arg2] [number of points=8]
    The program will save the points you select into *.npy files, so on subsequent runs it will load from these files and will not request user input.
    To manually input the points again, you need to delete the *.npy files (use `make clean` to remove all *.npy files).
    """

    routine = { "cd" : (corner_detector, 2),
                "gp" : (gaussian_pyramid, 2),
                "lp" : (laplacian_pyramid, 2),
              }
    # Dictionary that maps routine alias to (function, number of args)

    (curr_routine, args) = routine[sys.argv[1]]
    params = tuple(sys.argv[2:2+args])
    labeled_images = curr_routine(*params)
    displayImages(labeled_images)

if __name__=="__main__":
    main()
