"""
boids.py

An implementation of Craig Reynolds's Boids simulation using Python and Matplotlib
"""


import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial.distance import squareform, pdist
from numpy.linalg import norm

# set width and height for the screen
width, height = 640, 480

class Boids:
    """class that represents Boids simulation"""
    def __init__(self, N):
        """initialize the Boids simulation"""
        # init position & velocities
        # create a numpy array to store (x, y) of all Boids
        # displaced from the center. Creates a 1D array of 2N random 
        # numbers in the range [0,1], times 10 = [0,10]
        self.pos = [width/2.0, height/2.0] + 10*np.random.rand(2*N).reshape(N, 2)
        # normalized random velocities
        # for each boid. given an angle, the pair of numbers (x, y) lie on a 
        # circle's circumference (unit vector dependent on the angle). 
        angles = 2*math.pi*np.random.rand(N)
        # create an array of random unit vectors using cos and sin of previous 
        # calculated angles. Group coordinates (x, y) together using zip. Zip
        # joins two lists inot a list of tuples. list() is needed because just
        # calling zip will create only an iterator 
        self.vel = np.array(list(zip(np.cos(angles), np.sin(angles))))
        self.N = N
        # min dist of approach between two boids
        self.minDist = 25.0
        # max magnitude of velocities calculated by "rules." Limits how much a 
        # boid's velocity can be changed each time a sim rule is applied.
        self.maxRuleVel = 0.03
        # max magnitude of final velocity, overall boid vel limit
        self.maxVel = 2.0

    def tick(self, frameNum, pts, head):
        """update the boids for each frame of the animation"""
        # apply rules
        self.vel += self.applyRules()
        # limit the computed velocities of the boids
        self.limit(self.vel, self.maxVel)
        # compute updated positions of the boids by adding the new velocity vectors
        # to the old array of positions.
        self.pos += self.vel
        # apply boundary condition
        self.applyBC()
        # update the boid head and body position
        # apply new position with ::2 to pick out the even number elements (x-axis values)
        # and 1::2 to pick out the odd numbered elements (y-axis values)
        pts.set_data(self.pos.reshape(2*self.N)[::2],
                     self.pos.reshape(2*self.N)[1::2])
        # calculate position of head H = P + k*V, k = 10
        vec = self.pos + 10*self.vel/self.maxVel
        head.set_data(vec.reshape(2*self.N)[::2], vec.reshape(2*self.N)[1::2])

    # limit the velocities
    def limitVec(self, vec, maxVal):
        """limit the magnitude of the 2D vector"""
         # calculate the magnitude of the vector
        mag = norm(vec)
        # if it exceeds the max, scale (x,y) in proportion to vector magnitude
        # max value is self.maxRuleVel = 0.03
        if mag > maxVal:
            vec[0], vec[1] = vec[0]*maxVal/mag, vec[1]*maxVal/mag

    def limit(self, X, maxVal):
        """limit the magnitude of the 2D vector in array X to maxValue"""
        # extract velocity vectors from an array and pass it to limitVec
        for vec in X:
            self.limitVec(vec, maxVal)


    def applyBC(self):
        """apply boundary conditions"""
        # deltaR provides a slight buffer which allows the boid to move 
        # slightly outside the window before it starts coming back from 
        # the opposite direction for better visual effect.
        deltaR = 2.0
        # this method applies the tiled boundary conditions to each 
        # set of boid coordinates in pos array.
        for coord in self.pos:
            if coord[0] > width + deltaR: 
                coord[0] = - deltaR
            if coord[0] < - deltaR:
                coord[0] = width + deltaR
            if coord[1] > height + deltaR:
                coord[1] = - deltaR
            if coord[1] < - deltaR:
                coord[1] = height + deltaR

    def applyRules(self):
    # get pairwise distances between boids
        self.distMatrix = squareform(pdist(self.pos))

    # apply rule #1: separation
    # each boid is pushed away from neighboring boids within a distance 
    # of minDist (25 pixels)
        D = self.distMatrix < self.minDist
        vel = self.pos*D.sum(axis=1).reshape(self.N, 1) - D.dot(self.pos)
    # velocites are clamped/restricted to a certain max val using limit()
    # without this restriction, velocities would increase with each step
        self.limit(vel, self.maxRuleVel)

    # distance threshold for alignment (different from separation)
    # new Boolean matrix with 50 pixel threshold
        D = self.distMatrix < 50.0

    # apply rule #2: alignment
    # broad definition of flockmates. Each boid is influcence by and aligns
    # itself with the average elocity of its neighbors. average = dot product
    # of the Boolean matrix (D) and the velocity array.
        vel2 = D.dot(self.vel)
    # limit the velocities so they don't increase indefinitely
        self.limit(vel2, self.maxRuleVel)
        vel += vel2

    # apply rule #3: cohesion
    # add the positions of all the neighboring boids and subtract the position 
    # of the current boid make the velocity vector for each boid that points 
    # to the centroid of its neighbors. 
        vel3 = D.dot(self.pos) - self.pos
    # limit it so it does not continue indefinitely
        self.limit(vel3, self.maxRuleVel)
        vel += vel3

    # each rule produces its own velocity vector for each boid. Add these 
    # velocities together to produce an overall velocity vector for each 
    # boid that reflects the influence of all three simulation rules.
        return vel

    def buttonPress(self, event):
        """event handler for matplotlib button presses"""
        # left-click to add a new boid at the mouse click position
        if event.button == 1:
            # append the mouse location given by (event.xdata, event.ydata) to the
            # pos array.
            self.pos = np.concatenate((self.pos,
                                    np.array([[event.xdata, event.ydata]])), 
                                    axis=0)
            # generate a random velocity for the new boid
            angles = 2*math.pi*np.random.rand(1)
            v = np.array(list(zip(np.sin(angles), np.cos(angles))))
            # generate a random velocity for the new boid and append it to the vel array.
            self.vel = np.concatenate((self.vel, v), axis=0)
            # increment the boid count
            self.N += 1
        # right click to scatter the boids, 3 = right mouse button
        elif event.button == 3:
            # add a scattering velocity
            # change the velocity of all boids to point away from the mouse click
            # position. This will make the boids scatter away from the mouse click
            # Subtract the click position from the boid position to find the vector that
            # points away from the click position. Multiply by a small constant (0.1) to
            # control the scattering speed.
            self.vel += 0.1*(self.pos - np.array([[event.xdata, event.ydata]]))

def tick(frameNum, pts, head, boids):
    """update function for animation"""
    boids.tick(frameNum, pts, head)
    return pts, head

def main():
    # use sys.argv if needed
    print('starting boids...')

    parser = argparse.ArgumentParser(description="Implementing Craig Reynolds' Boids...")

    # add arguments
    # use the argparse module to accept command line arguments
    # --num-boids argument to set the initial number of boids
    parser.add_argument('--num-boids', dest='N', required=False)
    args = parser.parse_args()

    # set the initial number of boids if not argument is given
    N = 100
    if args.N:
        N = int(args.N)

    # create boids and set the boids in motion
    boids = Boids(N)

    # set the matplotlib figure and axes
    # P = body center, H = head center, V = velocity, k = constant distance P to H 
    fig = plt.figure()
    ax = plt.axes(xlim=(0, width), ylim=(0, height))

    # set the size and shape of the markers for the body and head
    # 'k' and 'r' for black and red. 'o' for circle marker
    # ax.plot method returns a list of matplotlib.lines.Line2D objects
    # the  , syntax picks up the first and only element in this list
    pts, = ax.plot([], [], markersize=10, c='k', marker='o', ls='None')
    head, = ax.plot([], [], markersize=4, c='r', marker='o', ls='None')
    # sets callback function tick() to be called for every frame of the animation
    # fargs specifies the arguments of the callback function
    # time interval 50 milliseconds
    anim = animation.FuncAnimation(fig, tick, fargs=(pts, head, boids), interval=50)

    # make the boids interactive by adding boids and have them respond to clicks
    # add an event handler to the matplotlib canvas. Calls a function every time 
    # a certain event happens. This handler calls buttonPress() method of the Boids
    # class with every mouse click: adds boid at the mouse click position
    cid = fig.canvas.mpl_connect('button_press_event', boids.buttonPress)

    plt.show()



# call main
if __name__ == '__main__':
    main()

    # update boid head and body position
    # calculate position of head H = P + k*V, k = 10
#    vec = self.pos + 10*self.vel/self.maxVel
    # update/reshape the matplotlib axis (set_data) with the new position values. 
    # [::2] picks out the even-numbered elements (x-axis values) from the velocity 
    # list. [1::2] picks out the odd-numbered elements (y-axis values).
#    head.set_data(vec.reshape(2*self.N)[::2], vec.reshape(2*self.N)[1::2])

    # Apply the three rules of the boids: separation, alignment, cohesion
    # Separation: traditionally we would use nested loops to calculate each
    # individual boid velocity, distance between head and body, direction, which boids
    # are flockmates and the distance between each boid at each animation step. 
    # This is how the traditional nested code would look like:

    # def test1(pos, radius):
        # fill output with zeros
        # vel = np.zeros(2*N).reshape(N, 2)
        # goes through for each pos of boid
        # for (i1, p1) in enumerate(pos):
            # velocity contribution
            # val = np.array([0.0, 0.0])
            # compute the distance between current boid and each other in array
            # for (i2, p2) in enumerate(pos):
                # if i1 != i2:
                    # calculate distance from p1
                    # dist = math.sqrt((p2[0] - p1[0])*(p2[0] - p1[0])) + 
                    #                   (p2[1] - p1[1])*(p2[1] - p1[1])
                    # apply threshold. If distance is greater than the radius,
                    # calculate displacement vector, add the result to val
                    # if dist < radius:
                        # val += (p2 - p1)
                # set velocity
                # vel[i1] = val
            # return computed velocity
            # return vel
    
    # Does the same thing as nested loops but the "numpy way," avoiding loops,
    # using scipy.spatial.module to efficiently calculate the distance between
    # def test(pos, radius):
        # get distance matrix by calculating dist between every pair of points
        # squareform gives NxN matrix of the calculated difference between points
        # distMatrix = squareform(pdist(pos))

        # apply the threshold, produces Boolean matrix
        # D = distMatrix < radius

        # compute velocity. D.sum totals True values into a column, reshape to a 
        # one-dimensional array for compatibility for multiplication with the 
        # position array. Then take the dot product (multiplication) of the 
        # Boolean matrix and array of boid positions
        # vel = pos*D.sum(axis=1).reshape(N, 1) - D.dot(pos)
        # return vel

# Experiments!
# 1. Implement obstacle avoidance by writing a new method avoidObstacle() and applying it right after 
# you apply the  three rules: self.vel += self.applyRules() , self.vel += self.avoidObstacle(). The 
# avoidObstacle method should use a predefined tuple (x, y, R) to add an additional velocity term to a 
# boid, pushing it away from the obstacle location (x, y), but only when the boid is within radius R of 
# the obstacle. Think of this as the distance at which a boid sees the obstacle and steers away from it. 
# You can specify the (x, y, R) tuple using a command line option, e.g. --obstacle 100,100,50. The obstacle 
# should be drawn as a circle on the screen using matplotlib's Circle class.
# 2. Implement a "leader" boid that is followed by the rest of the flock. The leader should be a
# boid that is controlled by the user using the arrow keys. The leader should be drawn in a different
# color and should be followed by the rest of the flock. The leader's position should be updated based on
# the arrow key presses, and the rest of the flock should follow the leader's position. You can use
# the matplotlib's event handling to capture key presses and update the leader's position accordingly.
# 3. Implement a "predator" boid that chases the flock. The predator should be a boid that is controlled
# by the user using the WASD keys. The predator should be drawn in a different color and should chase
# the flock. The predator's position should be updated based on the WASD key presses, and the flock should
# try to avoid the predator. You can use the matplotlib's event handling to capture key presses
# and update the predator's position accordingly.
# 4. Implement a "food" source that attracts the flock. The food should be a point on the screen that
# attracts the flock. The food's position should be updated based on the mouse clicks, and the flock
# should try to move towards the food. You can use the matplotlib's event handling to capture
# mouse clicks and update the food's position accordingly. The food should be drawn as a circle on the screen.
# 5. Implement a "wind" effect that pushes the flock in a certain direction. The wind should be a vector
# that pushes the flock in a certain direction. The wind's direction and magnitude should be controlled
# by the user using the arrow keys. The wind's effect should be applied to the flock's velocities.
# 6. Implement a "predator" that chases the flock. The predator should be a boid that is controlled
# by the user using the WASD keys. The predator should be drawn in a different color and should chase
# the flock. The predator's position should be updated based on the WASD key presses, and the flock should
# try to avoid the predator. You can use the matplotlib's event handling to capture key presses
# and update the predator's position accordingly.