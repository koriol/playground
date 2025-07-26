import turtle

# define the method, three pair of coordinates
# coordinates are the corners of the triangle
def draw_triangle(x1, y1, x2, y2, x3, y3, t):
    # pick up the pen 
    t.up()
    # put the pen at the starting position
    # the first triangle corner
    t.setpos(x1, y1)
    # put the pen down
    t.down()
    # with the pen down, draw to second position
    # the second corner of the triangle
    t.setpos(x2, y2)
    # draw to the third position
    # the last corner of the triangle
    t.setpos(x3, y3)
    # close the triangle by going to the first corner
    t.setpos(x1, y1)
    # pick up the pen and stop drawing
    t.up

def main():
    print('testing turtle graphics...')

    # create the object that does the drawing
    t = turtle.Turtle()
    # hide the object that is creating the drawing
    t.hideturtle()

    # execute the program to draw the triangle with 
    # these given parameters
    draw_triangle(-100, 0, 0, -173.2, 100, 0 , t)

    # keeps the tkinter window open after the triangle is drawn
    # tkinter is python's default GUI library
    turtle.mainloop()

# call main
if __name__ == '__main__':
    main()