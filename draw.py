import tkinter as tk

class Rectangle:
    def __init__(self, canvas, start_x, start_y):
        self.canvas = canvas
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = start_x
        self.end_y = start_y
        self.shape = self.canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='black')
    
    def update(self, end_x, end_y):
        self.end_x = end_x
        self.end_y = end_y
        self.canvas.coords(self.shape, self.start_x, self.start_y, self.end_x, self.end_y)

    def get_coords(self):
        return self.start_x, self.start_y, self.end_x, self.end_y

    def intersect(self, x1, y1, x2, y2):
        return not (x2 < self.start_x or x1 > self.end_x or y2 < self.start_y or y1 > self.end_y)

class Line:
    def __init__(self, canvas, start_x, start_y):
        self.canvas = canvas
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = start_x
        self.end_y = start_y
        self.shape = self.canvas.create_line(start_x, start_y, start_x, start_y, fill='black')
    
    def update(self, end_x, end_y):
        self.end_x = end_x
        self.end_y = end_y
        self.canvas.coords(self.shape, self.start_x, self.start_y, self.end_x, self.end_y)

    def get_coords(self):
        return self.start_x, self.start_y, self.end_x, self.end_y

    def intersect(self, x1, y1, x2, y2):
        return False  # Lines are not considered for selection in this implementation

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=400, bg='white')
        self.canvas.pack()
        self.selected_item = None
        self.shapes = []  # List to store drawn objects
        self.selection_rect = None
        self.toolbar = tk.Frame(master)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        self.select_button = tk.Button(self.toolbar, text="Select", command=self.activate_selection)
        self.select_button.pack(side=tk.LEFT)

        self.rect_button = tk.Button(self.toolbar, text="Rectangle", command=self.draw_rectangle)
        self.rect_button.pack(side=tk.LEFT)
        
        self.line_button = tk.Button(self.toolbar, text="Line", command=self.draw_line)
        self.line_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self.toolbar, text="Delete", command=self.delete_selected)
        self.delete_button.pack(side=tk.LEFT)

        self.select_mode = False
        self.canvas.bind('<Button-1>', self.start_draw)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.end_draw)
        
    def draw_rectangle(self):
        self.selected_item = Rectangle
        self.activate_draw_mode()
    
    def draw_line(self):
        self.selected_item = Line
        self.activate_draw_mode()

    def activate_selection(self):
        self.selected_item = None
        self.select_mode = True
        self.selection_rect = None

    def activate_draw_mode(self):
        self.select_mode = False
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None

    def start_draw(self, event):
        if self.select_mode:
            self.start_x = event.x
            self.start_y = event.y
        else:
            if self.selected_item == Rectangle:
                self.start_x = event.x
                self.start_y = event.y
                shape = Rectangle(self.canvas, event.x, event.y)
                self.shapes.append(shape)
            elif self.selected_item == Line:
                self.start_x = event.x
                self.start_y = event.y
                shape = Line(self.canvas, event.x, event.y)
                self.shapes.append(shape)

    def draw(self, event):
        if self.select_mode:
            if self.selection_rect:
                self.canvas.delete(self.selection_rect)
            self.selection_rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, dash=(2, 2))
        else:
            if self.selected_item == Rectangle or self.selected_item == Line:
                if self.selection_rect:
                    self.canvas.delete(self.selection_rect)
                self.selection_rect = None
                self.shapes[-1].update(event.x, event.y)

    def end_draw(self, event):
        pass  # No action needed on mouse release for drawing shapes

    def delete_selected(self):
        if self.selection_rect:
            x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
            selected_shapes = []
            for shape in self.shapes:
                if shape.intersect(x1, y1, x2, y2):
                    self.canvas.delete(shape.shape)
                else:
                    selected_shapes.append(shape)
            self.shapes = selected_shapes
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
