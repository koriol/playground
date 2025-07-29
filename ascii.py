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

"""Generating  the ASCII content from the Image"""
# an ASCII image is a list of character strings
aimg = []
# generate the list of tile dimensions
for j in range(rows):
    y1 = int(j*h)
    y2 = int ((j+1)*h)
    # correct the last tile
    if j == rows-1:
        y2 = H
    # append an empty string
    aimg.append("")
    for i in range(cols):
        # crop the image to fit the tile
        x1 = int(i*w)
        x2 = int ((i+1)*w)
        # correct the last tile
        if i == cols-1:
            x2 = W
        # crop the image to textract the tile into another Image object
        img = image.crop((x1, y1, x2, y2))
        # get the average luminance
        avg = int(getAverage(img))
        # look up the ASCII character for grayscale value (avg)
        if moreLLevels:
            gsval = gscale[int((avg*69)/255)]
        else:
            gsval = gscale2[int((avg*9)/255)]
        # append the ASCII character to the string
        aimg[j] += gsval