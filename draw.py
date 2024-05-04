import tkinter as tk

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
        self.selected_item = 'rectangle'
    
    def draw_line(self):
        self.selected_item = 'line'
    
    def start_draw(self, event):
        if self.selected_item == 'rectangle':
            self.start_x = event.x
            self.start_y = event.y
            self.shapes.append(self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='black'))
        elif self.selected_item == 'line':
            self.start_x = event.x
            self.start_y = event.y
            self.shapes.append(self.canvas.create_line(event.x, event.y, event.x, event.y, fill='black'))
    
    def draw(self, event):
        if self.selected_item == 'rectangle':
            self.canvas.coords(self.shapes[-1], self.start_x, self.start_y, event.x, event.y)
        elif self.selected_item == 'line':
            self.canvas.coords(self.shapes[-1], self.start_x, self.start_y, event.x, event.y)
    
    def end_draw(self, event):
        self.selected_item = None

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
