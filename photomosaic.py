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
    # get the closest RGB value to input, based on RGB distance
    # initialize the closest match index to 0
    index = 0
    # minimum distance to infinity
    min_index = 0
    min_dist = float("inf")
    # loop through the values in the list of averages and compute the
    # distances using distance formula minus the square root to save computational time
    for val in avgs:
        dis = ((val[0] - avg[0])*(val[0] - avg[0]) +
               (val[1] - avg[1])*(val[1] - avg[1]) +
               (val[2] - avg[2])*(val[2] - avg[2]))
        # if the computed distance is less than the stored minimum distance min_dist, it's replaced with the new minimum distance
        if dis < min_dist:
            min_dist = dis
            # min_index is the index of the average RGB value from the avgs list that is closest to input_avg
            min_index = index
        index += 1
    return min_index

# qavgs is the list of average RGB values for each tile in the target image, and kdtree is the scipy KDTree object created using a list of average RGB values from the input images.
def getBestMatchIndiciesKDT(qavgs, kdtree):
    """
    return indices of best Image matches based on RGB value distance uses a k-d tree
    """
    # e.g., [array([2.]), array([9], dtype=int64)]
    # use the KDTree object's query() method to get the points in the tree that are closes to the ones in qavgs. k is the number of nearest neighbors to the queried point you want to return.
    # k=1 means we want the closest match. The return is a tuple consisting of two numpy arrays with the distances and inndices of the matches. You need indices, so pick the second value from the result.
    res = list(kdtree.query(qavgs, k=1))
    min_indicies = res[1]
    return min_indicies

# takes two parameters: list of input images you chose based on closest RGB match to the individual tiles of target image, and tuple on photomosaics dimensions (m, n).
def createImageGrid(images, dims):
    """
    given a list of images and a grid size (m, n), create a grid of images
    """
    m, n = dims
    # sanity check: see whether the number of images supplied matches the grid size
    assert m*n == lin(images)

    # get the maximum height and width of the images
    # don't assume they're all equal
    # set max width and height to the maximum of all images for a standard size
    # if image is too small, solid black will fill the space
    width = max([img.size[0] for img in images])
    height = max([img.sizw[1] for img in images])

    # create the target image to fit all images in grid
    grid_img = Image.new('RGB', (n*width, m*height))

    # paste the tile images into the image grid
    for index in range (len(images)):
        row = int(index/n)
        col = index - n*row
        # paste the appropriate image into the grid at the right position
        # the first argument is the image object to be pasted, the second
        # (col*width, row*height) is the upper-left corner of the tile
        grid_img.paste(images[index], (col*width, row*height))

    return grid_img

def createPhotomosaic(target_image, input_images, grid_size, reuse_images, use_kdt):
    """
    creates photomosaic given target and input images
    """

    print('splitting input image...')
    # split target image
    target_images = splitImage(target_image, grid_size)

    print('finding image matches...')
    # for each target image, pick one from input
    output_images = {}
    # for user feedback
    count = 0
    batch_size = int(len(target_images)/10)

    # calculate input image averages
    avgs = []
    for img in input_images:
        avgs.append(getAverageRGB(img))

    # compute target averages
    avgs_target = []
    for img in target_images:
        # target subimage average
        avgs_target.append(getAverageRGB(img))