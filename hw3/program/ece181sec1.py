"""ECE 181 Section 1 Demo"""

from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
from scipy import ndimage
from scipy import signal
from skimage import color
from skimage import filters
from skimage import io

# Loading an image into variable 'img' using the imread function.
img = io.imread('Ucsb-henley.png')

# To display the image, use:
plt.imshow(img)
plt.show()

# To check the size of the image, one can use the 'shape' method:
height, width, num_channels = img.shape
print('height:', height)
print('width:', width)
print('num_channels:', num_channels)

# Notice that Python uses the conventional Math matrix notation, i.e., the size
# is nRows x nColumns x depth and for images, the numbers of rows is the height
# of the image (Y considering the standard cartesian plane).

# To access an element of the image, it is just a matter of indexing the desired
# pixel. Note that Python indexing starts at 0.
color_blue = img[0, 0, 2]

# The above command will return the value of the third channel (blue component)
# of the pixel located at the top-left corned of the image (0,0).

# It is also possible to access multiple elements at a time using the
# vectorized/slicing notation. For example, suppose we want to get the value of
# all 4 channels (RGBA) on coordinate (10,20).
color_rgba = img[10, 20, :]

# The ":" serves to indicate "all elements", no matter the dimension.

# As we will mainly use grayscale images on this course, it is useful to know
# how to convert a color image into grayscale (which is just the average of the
# 3 RGB channels).
img_gray = color.rgb2gray(img[:, :, :3])

plt.imshow(img_gray, cmap=cm.gray)
plt.show()

height_gray, width_gray = img_gray.shape
print('height_gray:', height_gray)
print('width_gray:', width_gray)

# Notice that now num_channels is missing, as expected.

# To exercise more the vectorized notation. let's suppose we would like to
# extract an entire scanline, i.e., an entire row of the image, or an small
# patch.
scanline = img_gray[300, :]
patch = img_gray[450:650, 450:650]

plt.plot(scanline)
plt.show()

plt.imshow(patch, cmap=cm.gray)
plt.show()

# Here, the notation img_gray[300,:] means, get img_gray on line 300, and all
# its columns. The second example, we are grabing a patch that starts at point
# (50,50) and ends at (249,249).

# We can also modify the same patch to turn it all white using:
img_gray[450:650, 450:650] = 1

plt.imshow(img_gray, cmap=cm.gray)
plt.show()

# To perform a convolution operation, we can use the convolve2d function, but
# first we need to define the kernel.
h = np.array([
    [1, 0, -1],
    [1, 0, -1],
    [1, 0, -1],
])

out = signal.convolve2d(img_gray, h)

plt.imshow(out, cmap=cm.gray)
plt.show()

# You can also apply Gaussian filtering using the following syntax (default
# deviation = 1):
blurred = filters.gaussian(img_gray, sigma=0.5)

# To iteratively get image coordinates using your mouse, you can use the ginput
# function as follows (it expects 4 points to be captured):
plt.imshow(blurred, cmap=cm.gray)
#plt.title('Click on 4 points')
plt.show()
#points = plt.ginput(4)

# print('points:')
# for p in points:
#     print('x:', p[0], 'y:', p[1])

# Using this, you can click on how many points you desire to select, then close
# the window to finish.

# Lastly, to save an image, use imsave function:
io.imsave('my_image.jpg', img_gray)
