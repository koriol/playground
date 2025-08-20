"""
photomosaic.py

Creates a photomosaic given a target image and a folder of input images.

Author: Katie O
"""

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


import os, random, argparse
from PIL import Image
import numpy as np
from scipy.spatial import KDTree
import timeit

def getAverageRGBOld(image):
    """
    given PIL Image, return average value of color as (r, g, b)
    """
    # no. of pixels in image
    npixels = image.size[0]*image.size[1]
    # get colors as [(cnt1, (r1, g1, b1)), ...]
    cols = image.getcolors(npixels)
    # get [(c1*r1, c1*g1, c1*g2), ...]
    sumRGB = [(x[0]*x[1][0], x[0]*x[1][2]) for x in cols]
    # calculate (sum(ci*ri)/np, sum(ci*bi)/np)
    # the zip gives us [(c1*r1, c2*r2, ...), (c1*g1, c1*g2, ...), ...]
    avg = tuple([int(sum(x)/npixels) for x in zip(*sumRGB)])
    return avg


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

def getImages(imageDir):
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

# inputs: target image, list of input images, the size of the generated photomosaic (rows, cols), flags for reusing images and using KDTree
def createPhotomosaic(target_image, input_images, grid_size, reuse_images, use_kdt):
    """
    creates photomosaic given target and input images
    """

    print('splitting input image...')
    # split target image into a grid of smaller image tiles
    target_images = splitImage(target_image, grid_size)

    print('finding image matches...')
    # for each target image, pick one from input
    output_images = {}
    # for user feedback
    count = 0
    # the process is lengthy so make batch_size a tenth the total number of images
    batch_size = int(len(target_images)/10)

    # calculate input image averages
    avgs = []
    # iterate through the images to compute their average RGB values
    for img in input_images:
        avgs.append(getAverageRGB(img))

    # compute target image averages of each square in grid
    avgs_target = []
    for img in target_images:
        # target subimage average
        avgs_target.append(getAverageRGB(img))

    # use k-d tree for average match?
    if use_kdt:
        # create k-d tree using the list of average RGB values from the input images
        kdtree = KDTree(avgs)
        # query k-d tree and retrieve the indices of the best matches by passing in avgs_target and the KDTree object to bestmatch function
        match_indices = getBestMatchIndicesKDT(avgs_target, kdtree)
        # process matches, iterate through all matching indices
        for match_index in match_indices:
            # find the corresponding input images, append them to the list of output_images
            output_images.append(input_images[match_index])
    else:
        # use linear search, iterate through the averages of RGB
        for avg in avgs_target:
            # for each tile, search for the closest match in the list of averages for the input images using the bestMatch function
            match_index = getBestMatchIndex(avg, avgs)
            # results returned as an index, used to retrieve the Image object and store in output_images list
            output_images.append(input_images[match_index])
            # user feedback after every batch_size (10 images)
            if count > 0 and batch_size > 10 and count % batch_size == 0:
                print('processed %d of %d...' %(count, len(target_images)))
            count += 1
            # remove selected image from input if flag set so it won't be reused
            if not reuse_images:
                input_images.remove(match)
    
    print('creating mosaic...')
    # draw mosaic to image
    mosaic_image = createImageGrid(output_images, grid_size)
    # return mosaic
    return mosaic_image

# gather our code in a main() function
def main():
    # command line args are in sys.argv[1], sys.argv[2]...
    # sys.arg[0] is the script name itself and can be ignored

    # parse arguments
    parser = argparse.ArgumentParser(description='Cretes a photomosaic from input images')
    # add arguments
    parser.add_argument('--target-image', dest='target_image', required=True)
    parser.add_argument('--input-folder', dest='input_folder', required=True)
    parser.add_argument('--grid-size', nargs=2, dest='grid_size', required=True)
    parser.add_argument('--output-file', dest='outfile', required=False)
    parser.add_argument('--kdt', action='store_true', required=False)
    
    args = parser.parse_args()

    #start timing
    start = timeit.default_timer()

    ##### INPUTS #####

    # target image
    target_image = Image.open(args.target_image)

    # input images
    print('reading input folder...')
    input_images = getImages(arg.inpu_folder)

    # check if any valid input images found
    if input_images == []
    print('No input images found in %s. Exiting.' % (args.input_folder, ))
    exit()

    # shuffle list - to get a more varied output?
    random.shuffle(input_images)

    # size of grid
    grid_size = (int(args.grid_size[0]), int(args.grid_size[1]))

    # output
    output_filename = 'mosaic.png'
    if args.outfile:
        output_filename = args.outfile

    # reuse any image in input
    reuse_images = True

    # resize the input to fit original image size?
    resize_input = True
    # use k-d trees for matching
    use_kdt = False
    if args.kdt:
        use_kdt = True

##### END INPUTS #####

    print 9'starting photomosaic creation...')

    # if images can't be reused, ensure m*n <= num_of_images
    if not reuse_images:
        if grid_size[0]*grid_size[1] > len(input_images):
            print('grid size less than number of images')
            exit()
        
    # resizing input
    if resize_input:
        print('resizing images...')
        # for given grid size, compute max dims w,h of tiles
        dims = (int(target_image.size[0]/grid_size[1]),
                int(target_image.size[1]/grid_size[0]))
        print("max tile dims: %s" % (dims,))
        # resize
        for img in input_images:
            img.thumbnail(dims)

    # setup time
    t1 = timeie.default_timer()

    # create photomosaic
    mosaic_image.save(output_filename, 'PNG')

    print("saved output to %s" % (output_filename,))
    print('done.')

    # creation time
    t2 = timeit.default_timer()

    print('Execution time:  setup: %f seconds' % (t1 - start, ))
    print('Execution time:  creation: %f seconds' % (t2 - t1, ))
    print('Execution time:  total: %f seconds' % (t2 - start, ))

# standard boilerplate to call the main() function to begin the program
if __name__ == '__main__':
    main()