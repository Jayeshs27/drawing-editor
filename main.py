from tkinter import *

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
      

class marker:
    def __init__(self):
        self.prevPoint = point(-1,-1)
        self.currPoint = point(-1,-1)
        self.color = 'white'
        self.lineWidth = IntVar()
        # self.lineWidth.set(6)

    def set_current_point(self, x, y):
        self.currPoint.x = x
        self.currPoint.y = y

    def set_previous_point(self, x, y):
        self.prevPoint.x = x
        self.prevPoint.y = y
    
    def reset_marker(self, event):
        self.prevPoint = point(-1,-1)
        self.currPoint = point(-1,-1)

    def set_color(self, color):
        self.color = color

    def set_lineWidth(self, width):
        self.lineWidth.set(width)


root = Tk()
root.title("Drawing Editor")
root.geometry("1000x600")
pen = marker()

upper_frame = Frame(root, height=150,width=1000, bg='#7a96c4')
upper_frame.grid(row=0,column=0)

bottom_frame = Frame(root, height=450, width=1000, bg='blue')
bottom_frame.grid(row=1,column=0)

canvas = Canvas(bottom_frame, height=450, width=1000, bg='#ffffff')
canvas.grid(row=1,column=0)

tools_frame = Frame(upper_frame, height=150, width=300, bg='white')
tools_frame.grid(row=0,column=0)

size_frame = Frame(upper_frame, height=150, width=300, bg='white')
size_frame.grid(row=0,column=1)



def use_pencil():
    pen.set_lineWidth(6)
    pen.set_color('black')

def use_eraser():
    pen.set_lineWidth(24)
    pen.set_color('white')
    canvas["cursor"] = DOTBOX


pencil = Button(tools_frame, text='Pencil',width=10,command=use_pencil)
pencil.grid(row=0, column=0)

eraser = Button(tools_frame, text='Eraser',width=10,command=use_eraser)
eraser.grid(row=1, column=0)

sizeDropDownbutton = Label(size_frame,text='size',width=10)
sizeDropDownbutton.grid(row=2, column=0)

options= [6, 8, 10, 12, 14]

sizeList = OptionMenu(size_frame, pen.lineWidth, *options)
sizeList.grid(row=1,column=0)


# stroke_color = StringVar()
# stroke_color.set('white')

def paint(event):
    x = event.x
    y = event.y
    pen.set_current_point(x, y)
    # canvas.create_oval(x, y,x + 1, y + 1, fill='black')

    if pen.prevPoint.x > 0 and pen.prevPoint.y > 0:
        canvas.create_polygon(pen.prevPoint.x, pen.prevPoint.y, pen.currPoint.x, pen.currPoint.y, outline=pen.color, width=pen.lineWidth.get(),fill=pen.color)
    pen.set_previous_point(x, y)

canvas.bind('<B1-Motion>',paint)
canvas.bind('<ButtonRelease-1>',pen.reset_marker)
root.mainloop()

