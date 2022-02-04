# Author: Vikram Bhagavatula
# Date: 2022-02-03
# Description: Program for homework 5

import sys
from auxilary import *

def drawEpipolarLine(left_aimg, right_img, fmat):
    """
    Intakes the left annotated image, and the right (normal) image, finds their fundamental matrix, and then
    determines the epipolar line in the right image corresponding to the left annotated image. The final
    result returned is the annotated version of the right image -- annotated with the epipolar line.
    """
    # (annotations, img) = left_aimg
    # TODO: Add check to make sure type of annotation is that of a point
    point = left_aimg.getAnnotations()[0] # gets the first element of the annotations, assumed to be a point
    epiline = fmat @ point

    return AnnotatedImage(right_img, epiline, "lines")

def epiline(file1, file2):
    """
    Runs epiline routine for part 1 of the homework.
    """
    img1, img2 = io.imread(file1), io.imread(file2)

    aimg1 = requestPoints(img1, 8)
    aimg2 = requestPoints(img2, 8)

    fmat = deriveFundamentalMat(aimg1, aimg2)

    aimg1_pt = requestPoints(img1, 1) # annotated image with one point selected
    res = drawEpipolarLine(aimg1_pt, aimg2, fmat) # annotated image with epipolar line as annotation

    return generateComposite(aimg1_pt, res)

def homography():
    """
    Runs homography routine for part 2 of the homework.
    """
    return

def displayImages(labeled_images):
    for (label, img) in labeled_images.items():
        plt.figure(label)
        plt.imshow(img)
    plt.show()

def main():
    file1 = input()
    file2 = input()

    epiline(file1, file2)

if __name__=="__main__":
    main()
