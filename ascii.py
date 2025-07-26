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
