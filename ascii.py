"""
ascii.py

A Python program that convert images to ASCII art.

Author: Mahesh Venkitachalam
"""

import sys, random, argparse
import numpy as np
import math

from PIL import Image

# grayscale level values from:
# http://paulbourke.net/dataformats/asciiart/


# Steps the program takes to generate ASCII art from an image
# 1. Convert the input image to grayscale.
# 2. Split the image into MxN  tiles.
# 3. Correct M (the number of rows) to match the image and font aspect ratio.
# 4. Compute the average brightness for each image tile and then look up a suitable ASCII character for each.
# 5. Assemble rows of ASCII character strings and print them to a file to form the final image.

# 70 levels of gray from darkest to lightest
gscale1 = "$@B8&WM#*oahkbdpqwmZOoQLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
# 10 levels of gray
gscale2 = "@%#*+=-:. "

"""Compute the average brightness"""
# image tile is passed as a PIL Image object
def getAverage(image):
    # convert the image as a numpy array, a 2D array of pixel brightness values
    im = np.array(image)
    # get the dimensions
    w,h = im.shape
    # Convert the 2D array into a flat 1D array whose length is a product of the original array's
    # width and height. Computes the average brightness level of the entire image tile.
    return np.average(im.reshape(w*h))

"""Open the image using Pillow"""
#open the file, convert to grayscale. "L" for luminance
image = Image.open(fileName).convert("L")
# store the image dimensions: width, height (measured in pixels)
W, H = image.size[0], image.size[1]
# compute the tile width for the number of columns specified
w = W/cols
# compute the tile height based on the aspect ratio and scale of the font
h = w/scale
# compute the number of rows to use in the final grid
rows = int(H/h)


"""Generating  the ASCII content from the Image"""
# an ASCII image is a list of character strings
aimg = []
# generate the list of tile dimensions. Iterate through the rows of image tiles.
for j in range(rows):
    # calculate the top and bottom y-coordinates of each image tile in a given row as y1 and y2 as integers
    y1 = int(j*h)
    y2 = int((j+1)*h)
    # correct the last tile
    if j == rows-1:
        # correct the last tile height to match the image height, ensures the bottom edge isn't truncated
        y2 = H
    # append an empty string as a compact way to represent current row
    aimg.append("")
    # iterate over all the tiles in a given row, column by column.
    for i in range(cols):
        # crop the image to fit the tile
        x1 = int(i*w)
        x2 = int ((i+1)*w)
        # correct the last tile
        if i == cols-1:
            # set the right x-coordinate to the width of the image
            x2 = W
        # crop the image to extract the tile into another Image object, extracting the tile from the complete image
        img = image.crop((x1, y1, x2, y2))
        # get the average luminance of the tile taking a PIL Image object as an argument
        avg = int(getAverage(img))
        # look up the ASCII character for grayscale value (avg)
        if moreLLevels:
            # scale the average brightness from [0,255] to [0,69]
            gsval = gscale[int((avg*69)/255)]
        else:
            # scale the average brightness from [0,255] to [0,9]
            gsval = gscale2[int((avg*9)/255)]
        # append the ASCII character to the string, loop until all rows are processed
        aimg[j] += gsval

"""Command line arguments"""
parser =  argparse.ArgumentParser(description="descStr")
# add expected arguments:
# file: specifies image file imput as required argument
# scale: sets the vertical scale factor for a font other than Courier
# out: output filename for the generated ASCII art, default out.txt
# cols: set the number of columns in the ASCII output
# morelevels: selects the 70-level grayscale ramp instead of the default 10-level ramp
parser.add_argument('--file', dest='imgFile', required=True)
parser.add_argument('--scale', dest='scale', required=False)
parser.add_argument('--out', dest='outFile', required=False)
parser.add_argument('--cols', dest="cols", required=False)
parser.add_argument('--moreLevels', dest='moreLevels', action='store_true')

"""Writing the ASCII Art strings to a text file"""
# open a new text file using the built-in open() function
f = open(outFile, 'w')
# iterate through each string in the aimg list and write it to the file
for row in aimg:
    f.write(row + '\n')
# clean up
f.close()


# Experiments!
# 1. Run the program with the command line option --scale 1.0. How does the resulting
# image look? Experiment with different calues for scale. Copy the output to a text editor 
# and try setting the text to different fixed-width fonts to see how doing so affects the
# appearance of the final image.
# 2. Add a command line option --invert to the program to invert the generated ASCII images 
# so that black appears white and vice verse. (Hint: try subtracting the tile brightness 
# value from 255 during lookup.)
# 3. Implement a command line option to pass in a different character ramp to create the
# ASCII art like so: "$ python ascii.py --map "@$%^`."" This should create the ASCII output
# using the given six-character ramp, where @ maps to a brightness value of and . maps to a value of 255