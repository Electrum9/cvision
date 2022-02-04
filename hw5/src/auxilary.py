# Author: Vikram Bhagavatula
# Date: 2022-02-03
# Description: All auxilary code to be used by the main module

# from tabulate import tabulate
from cv2 import cv2
from itertools import chain
from scipy.linalg import solve
import numpy as np
from skimage import io
from matplotlib import pyplot as plt
from matplotlib import cm

class AnnotatedImage:
    def __init__(self, image, annotations, annotation_type):
        self.image = image
        self.annotations = annotations
        self.annotation_type = annotation_type
        # At the moment, all annotations are lines/points (and of the same kind), in homogenous coordinates, and
        # are each individually represented by numpy arrays

    def getImage(self):
        return self.image

    def getAnnotations(self):
        return self.annotations

    # def __iter__(self):
    #     """
    #     Allows for pattern matching on object, to extract out its data.
    #     """
    #     return iter((self.image, self.annotations))

    def synthesize(self, annotation_type="points"):
        res = self.image
        if self.annotation_type == "points":
            for pt in map(lambda hp: hp[-1], self.annotations):
                res = cv2.circle(res, pt, 0, (255,0,0), -1)
        elif self.annotation_type == "lines":
            for line in self.annotations:
                slope = -1*line[0] / line[1]
                intercept = -1*line[2] / line[1]
                f = lambda x: slope*x + intercept

                e1 = f(-10)
                e2 = f(2*self.image.shape[1]) # picks a point outside the image

                res = cv2.line(res, e1, e2, (0,255,0), None)
        else:
            raise Exception(r'Invalid annotation type (valid types are "points" and "lines".')




def deriveFundamentalMat(aimg1, aimg2):
    """
    Intakes two annotated images (each are annotated with a list of points) and computes the fundamental matrix.
    """
    pts1 = np.array(aimg1.getAnnotations())
    pts2 = np.array(aimg2.getAnnotations())

    return cv2.findFundamentalMat(pts1, pts2, cv2.FM_8POINT) # Uses 8-point algorithm to compute fundamental matrix


def generateComposite(aimg1, aimg2, axis=1):
    """
    Intakes two annotated images, synthesizes a new image from each of them (their visualizations or representations),
    and combines them together horizontally.
    """
    img1 = aimg1.synthesize()
    img2 = aimg2.synthesize()

    return np.concatenate((img1, img2), axis)

def requestPoints(img, npoints):
    """
    Intakes image object, prompts the user to select points on the image. Returns an AnnotatedImage annotated with the points selected.
    """

    plt.imshow(img)
    points = plt.ginput(npoints, timeout=60)

    return AnnotatedImage(img, points, "points")
