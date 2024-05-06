import tkinter as tk

class ControlCenter:
    def __init__(self):
        self.current_color = 'black'
        self.radius_of_roundness = 8
        self.root = tk.Tk()

        self.root.geometry("800x600")
        self.toolbar_frame = tk.Frame(self.root, width=100, bg="light grey")
        self.canvas_frame = tk.Frame(self.root, bg="white")

        self.toolbar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.shapes_frame = tk.Frame(self.toolbar_frame, width=100, bg='light gray')
        self.shapes_frame.grid(row=0, column=0, padx=5,pady=5)

        self.colors_frame = tk.Frame(self.toolbar_frame, width=100, bg='light gray')
        self.colors_frame.grid(row=1, column=0, padx=5,pady=5)

        self.roundedness_frame = tk.Frame(self.toolbar_frame, width=100, bg='light gray')
        self.roundedness_frame.grid(row=2, column=0, padx=5,pady=5)

        self.operations_frame = tk.Frame(self.toolbar_frame, width=100, bg='light gray')
        self.operations_frame.grid(row=3, column=0, padx=5,pady=5)
        
        self.fileIO_frame = tk.Frame(self.toolbar_frame, width=100, bg='light gray')
        self.fileIO_frame.grid(row=4, column=0, padx=5,pady=5)

        self.shapes_label = tk.Label(self.shapes_frame,text='Shapes')
        self.shapes_label.grid(row=0,column=0,columnspan=2)

        self.rect_btn = tk.Button(self.shapes_frame,text='rectangle',width=6, height=1)
        self.rect_btn.grid(row=1,column=0,padx=5,pady=5)

        self.line_btn = tk.Button(self.shapes_frame,text='line',width=6, height=1)
        self.line_btn.grid(row=1,column=1,padx=5,pady=5)

        self.colors_label = tk.Label(self.colors_frame,text='Colors')
        self.colors_label.grid(row=0,column=0,columnspan=2)

        self.green_color_btn = tk.Button(self.colors_frame,width=2, height=1, bg='green')
        self.green_color_btn.grid(row=1,column=0,padx=10,pady=5)

        self.red_color_btn = tk.Button(self.colors_frame,width=2, height=1, bg='red')
        self.red_color_btn.grid(row=1,column=1,padx=10,pady=5)

        self.blue_color_btn = tk.Button(self.colors_frame,width=2, height=1, bg='blue')
        self.blue_color_btn.grid(row=2,column=0,padx=10,pady=5)

        self.black_color_btn = tk.Button(self.colors_frame,width=2, height=1, bg='black')
        self.black_color_btn.grid(row=2,column=1,padx=10,pady=5)

        self.rounded_label = tk.Label(self.roundedness_frame,text='Roundedness')
        self.rounded_label.grid(row=0,column=0,columnspan=2)

        self.radio = tk.IntVar()     
        self.R1 = tk.Radiobutton(self.roundedness_frame, text="ROUNDED", variable=self.radio, value=1)  
        self.R1.grid(row=0,column=0)  
        self.R2 = tk.Radiobutton(self.roundedness_frame, text="UNROUNDED", variable=self.radio, value=2)  
        self.R2.grid(row=0,column=1)
        # self.radio.set(2)

        self.operations_label = tk.Label(self.operations_frame,text='operations')
        self.operations_label.grid(row=0,column=0,columnspan=2)

        self.select_btn = tk.Button(self.operations_frame, text='select',width=6, height=1)
        self.select_btn.grid(row=1,column=0,padx=5,pady=5)

        self.move_btn = tk.Button(self.operations_frame,text='move',width=6, height=1)
        self.move_btn.grid(row=1,column=1,padx=5,pady=5)

        self.copy_btn = tk.Button(self.operations_frame,text='copy',width=6, height=1)
        self.copy_btn.grid(row=2,column=0,padx=5,pady=5)

        self.delete_btn = tk.Button(self.operations_frame,text='delete',width=6, height=1)
        self.delete_btn.grid(row=2,column=1,padx=5,pady=5)

        self.group_btn = tk.Button(self.operations_frame,text='group',width=6, height=1)
        self.group_btn.grid(row=3,column=0,padx=5,pady=5)

        self.ungroup_btn = tk.Button(self.operations_frame,text='Ungroup',width=6, height=1)
        self.ungroup_btn.grid(row=3,column=1,padx=5,pady=5)

        self.ungroup_all_btn = tk.Button(self.operations_frame,text='Ungroup all',width=6, height=1)
        self.ungroup_all_btn.grid(row=4,column=0,padx=5,pady=5)

        self.edit_btn = tk.Button(self.operations_frame,text='edit',width=6, height=1)
        self.edit_btn.grid(row=4,column=1,padx=5,pady=5)

        self.fileIO_label = tk.Label(self.fileIO_frame,text='file I/O')
        self.fileIO_label.grid(row=0,column=0)

        self.export_btn = tk.Button(self.fileIO_frame, text='export to xml',width=12, height=1)
        self.export_btn.grid(row=1,column=0,padx=5,pady=5)

        self.import_btn = tk.Button(self.fileIO_frame, text='import from xml',width=12, height=1)
        self.import_btn.grid(row=2,column=0,padx=5,pady=5)

        self.canvas = tk.Canvas(self.canvas_frame, width=400, height=400, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)



def on_button_click():
    print("Button clicked")

def on_color_selected(color):
    print("Color selected:", color)


# control_center = ControlCenter()
# control_center.root.mainloop()
# Create frames for toolbar and canvas

