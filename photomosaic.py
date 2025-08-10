# This project practices the following:
# - Create images using the Python Imaging Library (PIL)
# - Cpmpute the average RGB value of an image.
# - Crop images
# - Replace part of an image by pasting in another image.
# - Compare RGB values using a measurement of average distance in three dimensions
# - Use a data structure called a k-d tree to efficiently find the image that best matches a section of the target image.

# How it works:
# 1. Read the input images, which will be drawn on to replace the tiles in the original image.
# 2. Read the target image and split it into an MxN grid opf tiles.
# 3. For each tile, find the best match from the input images
# 4. Create the final mosaic arranging the selected input images in an MxN grid.


# a k-dimensional tree divides the space into a number of non-overlapping subspaces of k dimensions.
# Once you arrange a dataset into k-d tree, you can serach through points quickly to find the nearest neighbor.

import numpy as np


def getIages(imageDir):
    """
    given a directory of images, return a list of Images
    """
    # gather the file names in the image directory
    files = os.listdir(imageDir)
    images = []
    for file in files:
        # ensures the code works with both relative and absolute paths
        filePath = os.path.abspath(os.path.join(imageDir, file))
        try:
            # explicit load so we don't run into resource crunch
            fp = open(filePath, "rb")
            im = Image.open(fp)
            images.append(im)
            # force loading the image data from file
            im.load()
            # close the file
            fp.close()
        except:
            # skip
            print("Invalid image: %s" % (filePath,))
        return images

def getAverageRGB(image):
    """
    return the average color value as (r, g, b) for each input image
    """
    # get each tile image as a numpy array
    im = np.array(image)
    # get the shape of each input image where (w,h,d) is (r,g,b) dimensions
    w,h,d = im.shape
    # get the average RGB value
    return tuple(np.average(im.reshape(w*h, d), axis=0))

def splitImage(image, size):
    """
    given the image and dimensions (rows, cols), return an m*n list of images
    """
    # gather the dimensions of the target image
    W, H = image.size[0], image.size[1]
    # find the dimensions of each tile
    m, n = size
    w, h = int(W/n), int(H/m)
    # image list
    imgs = []
    # generate a list of images, iterate through the grid dimensions and cut out and store each tile as a separate image
    for j in range(m):
        for i in range(n):
            # append cropped image
            # image.crop crops out a portion of the image using the upper-left and lower-right image coordinates as arguments
        imgs.append(image.crop((i*w, j*h, (i+1)*w, (j+1)*h)))
    # return the list of images row by row
    return imgs

def getBestMatchIndex(input_avg, avgs):
    """
    return index of the best image match based on average RGB value distance
    """

    # input image average
    avg = input_avg
    #get the closest RGB value to input, based on RGB distance
    index = 0
    min_index = 0
    min_dist = float("inf")
    for cal in avgs:
        dis = ((val[0] - avg[0])*(val[0] - avg[0]) +
               (val[1] - avg[1])*(val[1] - avg[1]) +
               (val[2] - avg[2])*(val[2] - avg[2]))
    if dist < min_dist:
        min_dist = min_dist
        min_index = index
    index += 1

return min_index

def getBestMatchIndiciesKDT(qavgs, kdtree):
    """
    return indices of best Image matches based on RGB value distance uses a k-d tree
    """
    # e.g., [array([2.]), array([9], dtype=int64)]
    res = list(kdtree.query(qavgs, k=1))
    min_indicies = res[1]