"""
conway.py

A simple Python/matplotlib implementation of Conway's Game of Life

Author: Katherine Oriol
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def randomGrid(N):
# set the initial conditions as random: Randomnly choose either 0 
# or 255, with (4*4=) 16 values, with a probability the first number 
# in the array appearing 10% of the time and the second number 
# appearing 90% of the time. Reshape the output to show a 4 column 
# by 4 row array.
# code: np.random.choice([0, 255], 4*4, p=[0.1, 0.9]).reshape(4, 4)
    return np.random.choice([255, 0], N*N, p=[0.2, 0.8]).reshape(N,N)

# to represent Conway's grid, 255 represents on/alive, 
# 0 represents off/dead. The array has three rows and three 
# columns. Each element is given an integer value
# x = np.array([[0, 0, 255], [255, 255, 0], [0, 255, 0]])

# A glider pattern that moves steadily across the grid using numpy 
# array with shape 3 by 3.
def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    # Use numpy splice operation to copy the glider array into the 
    # simulation's 2-D array with the pattern's top-left corner 
    # placed at the specified corner coordinate (i, j)
    grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go up by line
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute 8-neighbor sum using toroidal boundary 
            # conditions - x and y wrap around so that the 
            # simulation takes place on a toroidal surface

            # enforce boundary conditions for the torus. When j = N - 1 at the 
            # edge of the grid, the cell to the right will give (j+1)%N. This 
            # sets j back to 0, making the rightr side of the grid wrap to the 
            # left side. The same applies to the bottom wrap to the top of the 
            # grid.
            # right = grid[i, (j+1)%N]
            # bottom = grid[(i+j)%N, j]

            # implement the rules based on the number of neighboring cells that 
            # are ON or OFF. Sum and divide by 255 to find the total number of 
            # ON cells. For any given cell (i, j), sum the value of its eight 
            # neighbors, using % to account for toroidal boundary conditions. 
            # ON = 255, after total, divide by 255 to find the total number of 
            # ON cells and store as total.
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                        grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                        grid[(i-1%N, (j-1)%N)] + grid[(i-1)%N, (j+1)%N] +
                        grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]/255))
            
            # apply Conway's rules. Any ON cell is turned OFF if it has fewer than
            # 2 or more than 3 neighbors that are ON. Else, the OFF cell is turned 
            # on if exactly 3 neighbors are ON. Apply to newGrid, starts as a copy 
            # of grid. Once evaluated and updated, newGrid contains the data for 
            # the next steps. Can't change grid or the states of the cells would 
            # keep changing as you try to evaluate them
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = 0
                else:
                    if total == 3:
                        newGrid[i, j] = 255
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    # need to return a tuple here, since this callback
    # function needs to return an iterable
    return img,

def main():
    # command line arguments are in sys.argv[1], sys.argv[2], ...
    # sys.argsv[0] is the script name and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of " \
    "Life simulation.")
    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    # set animation to milliseconds
    parser.add_argument('--interval', dest='interval', required=False)
    # start simulation with a glider pattern else the ON/OFF is random
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()

    # set grid
    N = 100

    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # declare grid
    grid = np.array([])
    # check if "glider" demo flag is specified
    # set the initial condition to match a particular pattern, zero
    # out the grid first. Create an N by N array of zeros
    # grid = np.zeros(N*N).reshape(N, N)
    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(1, 1, grid)
    elif args.gosper:
        grid = np.zeros(N*N).reshape(N, N)
        addGosperGliderGun(10, 10, grid)
    else:
        # set N if specified and valid
        if args.N and int(args.N) > 8:
            N = int(args.N)
        # populate grid with random on/off - more off than on
        grid = randomGrid(N)

    # set up the animation
    fig, ax = plt.subplots()
    # Interpolation as 'nearest' to have sharp edges between squares.
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                frames = 10,
                                interval=updateInterval)
    plt.show()

# call main function
if __name__ == '__main__':
    main()

# imshow will display the current state of the grid in 
# matplotlib which represents a matrix of numbers as an image. 
# plt.imshow(x, interpolation='nearest')


# add glider pattern to the preconstructed grid with a call to the
# glider function. (1, 1) specifies the coordinate to add the glider
# near the top-left corner of the grid
# addGlider(1, 1, grid)

### Experiments to try
# - Write an addGosperGun() method to add a pattern to the grid. 
# - Write a readPattern() method that reads in an initial pattern 
# from a text file and uses it to set the initial conditions for the 
# simulation. You can use Python methods like open and file.read. The 
# first line of the file define N, the rest is NxN integers (0 or 255) 
# separated by whitespace. Add a --pattern-file command line option 
# to use this file while running the program