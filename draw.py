import tkinter as tk

class Rectangle:
    def __init__(self, canvas, start_x, start_y):
        self.canvas = canvas
        self.start_x = start_x
        self.start_y = start_y
        self.shape = self.canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='black')
    
    def update(self, end_x, end_y):
        self.canvas.coords(self.shape, self.start_x, self.start_y, end_x, end_y)

class Line:
    def __init__(self, canvas, start_x, start_y):
        self.canvas = canvas
        self.start_x = start_x
        self.start_y = start_y
        self.shape = self.canvas.create_line(start_x, start_y, start_x, start_y, fill='black')
    
    def update(self, end_x, end_y):
        self.canvas.coords(self.shape, self.start_x, self.start_y, end_x, end_y)

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=400, bg='white')
        self.canvas.pack()
        self.selected_item = None
        self.shapes = []
        self.toolbar = tk.Frame(master)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        self.rect_button = tk.Button(self.toolbar, text="Rectangle", command=self.draw_rectangle)
        self.rect_button.pack(side=tk.LEFT)
        
        self.line_button = tk.Button(self.toolbar, text="Line", command=self.draw_line)
        self.line_button.pack(side=tk.LEFT)
        
        self.canvas.bind('<Button-1>', self.start_draw)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.end_draw)
        
    def draw_rectangle(self):
        self.selected_item = Rectangle
    
    def draw_line(self):
        self.selected_item = Line
    
    def start_draw(self, event):
        if self.selected_item == Rectangle:
            self.start_x = event.x
            self.start_y = event.y
            self.shapes.append(Rectangle(self.canvas, event.x, event.y))
        elif self.selected_item == Line:
            self.start_x = event.x
            self.start_y = event.y
            self.shapes.append(Line(self.canvas, event.x, event.y))
    
    def draw(self, event):
        if self.selected_item == Rectangle or self.selected_item == Line:
            self.shapes[-1].update(event.x, event.y)
    
    def end_draw(self):
        self.selected_item = None

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
