# This project practices the following:
# - Create images using the Python Imaging Library (PIL)
# - Cpmpute the average RGB value of an image.
# - Crop images
# - Replace part of an image by pasting in another image.
# - Compare RGB values using a measurement of average distance in three dimensions
# - Use a data structure called a k-d tree to efficiently find the image that best matches a section of the target image.

# How it works:
# 1. Read the input images, which will be drawn on to replace the tiles in the original image.
# 2. Read the target image and split it into an MxN grid opf tiles.-