

import turtle
import math

# draw the recursive snowflake
def drawKochSF(x1, y1, x2, y2, t):
    # d is the distance between two points
    d= math.sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))
    # r is a third of the distance
    r = d/3.0
    # h is the height or the apex of the snowflake
    h = r*math.sqrt(3)/2.0
    # p1 and p3 describe the base of the cone portion
    # p3 is the point that is two thirds of the length
    p3 = ((x1 + 2*x2)/3.0, (y1 + 2*y2)/3.0)
    # p1 is the point that is one third the length 
    p1 = ((2*x1 + x2)/3.0, (2*y1 + y2)/3.0)
    # c is the midpoint of the length
    c = (0.5*(x1 + x2), 0.5*(y1 + y2))
    # n is the unit vector perpendicular to the length
    n = ((y1 - y2)/d, (x2 - x1)/d)
    # p2 is the apex point
    p2 = (c[0] + h*n[0], c[1] + h*n[1])

    # recursion stopping criteria
    # if the length of the segment is greater than 10 pixels,
    # continue the recursion
    if d > 10:
        # flake 1
        drawKochSF(x1, y1, p1[0], p1[1], t)
        # flake 2
        drawKochSF(p1[0], p1[1], p2[0], p2[1], t)
        # flake 3
        drawKochSF(p2[0], p2[1], p3[0], p3[1], t)
        # flake 4
        drawKochSF(p3[0], p3[1], x2, y2, t)

    else:
        # draw cone
        t.up()
        t.setpos(p1[0], p1[1])
        t.down()
        t.setpos(p2[0], p2[1])
        t.setpos(p3[0], p3[1])
        # draw sides
        t.setpos(x1, y1)
        t.down()
        t.setpos(p1[0], p1[1])
        t.up()
        t.setpos(p3[0], p3[1])
        t.down()
        t.setpos(x2, y2)

def main():
    print('Drawing the Koch snowflake...')

    t = turtle.Turtle()
    t.hideturtle()

    # draw
    try:
        drawKochSF(-100, 0, 100, 0, t)
        drawKochSF(0, -173.2, -100, 0, t)
        drawKochSF(100, 0, 0, -173.2, t)
    except:
        print("Exception, exiting")
        exit(0)
# wait for user to click on screen to exit
    turtle.Screen().exitonclick()

# call main
if __name__ == '__main__':
    main()