

import turtle
import math
import random, argparse
import random
from datetime import datetime


class Spiro:
    # constructor
    def __init__(self, xc, yc, col, R, r, l):
        # create the turtle object for individual spiros
        # allows multiple spiros at once
        self.t = turtle.Turtle()
        # set the cursor shape, the angle requirement
        self.t.shape('turtle')
        # set the step in degrees
        self.step = 5
        # set the drawing complete flag to indicate it's done
        self.drawingComplete = False

        # set the parameters
        self.setparams(xc, yc, col, R, r, l)

        # initialize the drawing
        self.restart()

    def setparams(self, xc, yc, col, R, r, l):
        # the Spirograph parameters
        # store the spiro coordinates with (xc, yc)
        self.xc = xc
        self.yc = yc
        # convert each radius to an integer
        self.R = int(R)
        self.r = int(r)
        # l defines the pen position
        self.l = l
        # determine the color
        self.col = col
        # reduce r/R to its smallest form by dividing with the GCD
        gcdVal = math.gcd(self.r, self.R)
        # the periodicity of the curve
        self.nRot = self.r//gcdVal
        # get ratio of radii
        self.k = r/float(R)
        # set the color
        self.t.color(*col)
        # store the current angle
        # set the starting angle value to 0
        self.a = 0 

    def restart(self):
        # resets the drawing parameters and gets into position
        # makes it possible to reuse, restarts per spiro
        # set the flag, indicates it's ready
        self.drawingComplete = False
        # show the turtle
        self.t.showturtle()
        # got to the first point
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        # compute the curve's starting point
        x = R*((1 - k)*math.cos(a) + l*k*math.cos((1 - k)*a/k))
        y = R*((1 - k)*math.sin(a) - l*k*math.sin((1 - k)*a/k))
        # place the pen at the computed starting point
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    def draw(self):
        # draw the rest of the points
        R, k, l = self.R, self.k, self.l
        # iterate through the entire range of a complete spiro
        for i in range(0, 360*self.nRot + 1, self.step):
            a = math.radians(i)
            # compute the (x,y) for each iteration
            x = R*((1 - k)*math.cos(a) + l*k*math.cos((1 - k)*a/k))
            y = R*((1 - k)*math.sin(a) - l*k*math.sin((1 - k)*a/k))

            try:
                # draw the line from each point to the next
                self.t.setpos(self.xc + x, self.yc + y)
            except:
                print("Exception, exiting")
                exit(0)
            # drawing is now done so hide the turtle cursor
            self.t.hideturtle()

    def update(self):
        # this function makes the drawing animation possible
        # skip the rest of the steps if done
        if self.drawingComplete:
            return
        # increment the angle
        self.a += self.step
        # draw a step
        R, k, l = self.R, self.k, self.l
        # set the angle
        a = math.radians(self.a)
        x = self.R*((1 - k)*math.cos(a) + l*k*math.cos((1 - k)*a/k))
        y = self.R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))

        try:
            self.t.setpos(self.xc + x, self.yc + y)
        except:
            print("Exception, exiting")
            exit(0)
        # if drawing is complete, set the flag
        if self.a >= 360*self.nRot:
            self.drawingComplete = True
            # drawing is now complete, hide the turtle cursor
            self.t.hideturtle()

class SpiroAnimator:
    # constructor
    def __init__(self, N):
        # set the timer value in milliseconds
        self.deltaT = 10
        # get the window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        # restarting
        self.restarting = False
        # create the Spiro objects
        self.spiros = []
        for i in range(N):
            # generate random parameters
            rparams = self.genRandomParams()
            # set the spiro parameters
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
        # call timer
        turtle.ontimer(self.update, self.deltaT)
    
    def genRandomParams(self):
        # generate random parameters that fit within the window
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        # random number within a uniform distribution
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)
        # random color for red, blue and green
        col = (random.random(),
               random.random(),
               random.random())
        return (xc, yc, col, R, r, l)
    
    def restart(self):
        # restart animation to draw a new spiro set
        # ignore restart if already restarting
        if self.restarting:
            return
        else:
            self.restarting = True
            # if/else prevents calling this method before it's complete
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters
            rparams = self.genRandomParams()
            # set the spiro parameters
            spiro.setparams(*rparams)
            # restart drawing
            spiro.restart()
        # done restarting
        self.restarting = False
        # reset flag so next restart won't be ignored

    def update(self):
        # allows for animation through incremental updates
        # update all spiros
        nComplete = 0
        for spiro in self.spiros:
            # update list of spiros
            spiro.update()
            # count completed spiros
            if spiro.drawingComplete:
                nComplete += 1
        # restart if all spiros are complete
        if nComplete == len(self.spiros):
            self.restart()
        # call the timer
        try:
            turtle.ontimer(self.update, self.deltaT)
        except:
            print("Exception, exiting.")
            exit(0)

    def toggleTurtles(self):
        # toggle cursor on/off to draw faster
        for spiro in self.spiros:
            if spiro.t.invisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()

def saveDrawing():
    # hide turtle cursoor
        turtle.hideturtle()
        # generate unique filenames
        dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
        fileName = 'spiro-' + dateStr
        print('saving drawing to {}.eps/png'.format(fileName))
        # get the tkinter canvas
        canvas = turtle.getcanvas()
        # save the drawing as a embedded postscript image
        canvas.postscript(file = fileName + '.eps')
        # use the Pillow module to convert the postscript image file to PNG
        # PNG is more versatile than eps
        img = Image.open(fileName + '.eps')
        img.save(fileName + '.png', 'png')
        # show the turtle cursor
        turtle.showturtle()

# main() function
def main():
    # use. sys.argv if needed
    print('generating spirograph...')
    # create parser
    descStr = """This program draws spirgraphs using the Turtle module.
     When run with no arguments, this program draws random Spirographs.
     
     Terminology:
     R: radius of outer circle.
     r: radius of inner circle.
     l: ratio of hole distance to r.
     """
    # manage command line arguments
    parser = argparse.ArgumentParser(description=descStr)

    # add R, r, l arguments, assign to destination of sparams
    # not required as there is a function for random params
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False, 
                        help="The three arguments in sparams: R, r, l.")
    
    # parse args
    args = parser.parse_args()

    # set the width of the drawing window to 80% of the screen
    turtle.setup(width=0.8)

    # set the cursor shape to turtle
    turtle.shape('turtle')

    # set the title
    turtle.title("Spirographs!")
    # add the key handler to save drawings with s key press
    turtle.onkey(saveDrawing, "s")
    # start listening for user inputs
    turtle.listen()

    # hide the main turtle cursor
    turtle.hideturtle()

    # check for any arguments sent to --sparams and draw the Spirograph
    if args.sparams:
        params = [float(x) for x in args.sparams]
        # draw the Spirograph with the given parameters
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        # create the animator object
        spiroAnim = SpiroAnimator(4)
        # add a key handler to toggle the turtle cursor
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        # add a key handler to restart the animation
        turtle.onkey(spiroAnim, "space")

    # start the turtle main loop
    turtle.mainloop()

# call main
if __name__ == '__main__':
    main()

### Experiments to try
# - write a program to draw random spirals. Find the 
# equation for a logarthmic spiral in parametric form and 
# then use it to draw the spirals

# - orient the turtle so that as the curve is being drawn, 
# it faces in the direction of drawing. (Hint: calculate 
# the direction vector between successive points for every 
# step and reorient the turtle using turtle.setheading() method)