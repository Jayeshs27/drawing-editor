import tkinter as tk
from group_draw_ui import ControlCenter

class Rectangle:
    def __init__(self, canvas, x1, y1, x2, y2 ,color, r):
        self.canvas = canvas
        self.start_x = x1
        self.start_y = y1
        self.end_x = x2
        self.end_y = y2
        self.radius=r
        self.color=color
        self.is_move=False
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        self.shape = self.canvas.create_polygon(points, outline=self.color, fill="", smooth=True)

    def update(self, x2, y2):
        self.end_x = x2
        self.end_y = y2
        x1=self.start_x
        y1=self.start_y
        r=self.radius
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        self.canvas.coords(self.shape, *points)

    def update_radius(self,x2,y2,r):
        self.end_x = x2
        self.end_y = y2
        x1=self.start_x
        y1=self.start_y
        self.radius=r
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        self.canvas.coords(self.shape, *points)

    def update_color(self,color,flag):
        if flag:
            self.color=color
        self.canvas.itemconfigure(self.shape, fill="", outline=color)
    
    def get_coords(self):
        return self.start_x, self.start_y, self.end_x, self.end_y

    def intersect(self, x1, y1, x2, y2):
        rect_x1, rect_y1, rect_x2, rect_y2 = self.get_coords()

        return not (
            x2 < rect_x1 or x1 > rect_x2 or y2 < rect_y1 or y1 > rect_y2
        ) and not (
            (min(self.start_x, self.end_x) < x1 < max(self.start_x, self.end_x))
            and (min(self.start_x, self.end_x) < x2 < max(self.start_x, self.end_x))
            and (min(self.start_y, self.end_y) < y1 < max(self.start_y, self.end_y))
            and (min(self.start_y, self.end_y) < y2 < max(self.start_y, self.end_y))
        )
    
    def deepcope(self):
        copied_rect = Rectangle(self.canvas, self.start_x, self.start_y,self.end_x,self.end_y,self.color,self.radius)
        copied_rect.is_move=self.is_move
        # copied_rect.end_x = self.end_x
        # copied_rect.end_y = self.end_y
        # copied_rect.is_move = self.is_move
        # copied_rect.shape = self.canvas.create_rectangle(
        #     self.start_x, self.start_y, self.end_x, self.end_y
        # )
        return copied_rect


def line_equation(x, y, slope, x1, y1):
    return (y - y1) - slope * (x - x1)


def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list


def flatten2(nested_list):
    for element in nested_list:
        if isinstance(element, list):
            yield from flatten2(element)
        else:
            yield element


class Line:
    def __init__(self, canvas, start_x, start_y,color):
        self.canvas = canvas
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = start_x
        self.end_y = start_y
        self.color=color
        self.is_move=False
        self.shape = self.canvas.create_line(
            start_x, start_y, start_x, start_y, fill=color
        )

    def update(self, end_x, end_y):
        self.end_x = end_x
        self.end_y = end_y
        self.canvas.coords(
            self.shape, self.start_x, self.start_y, self.end_x, self.end_y
        )

    def intersect(self, x1, y1, x2, y2):
        if (self.end_x - self.start_x) != 0:
            slope = (self.end_y - self.start_y) / (self.end_x - self.start_x)

            a1 = line_equation(x1, y1, slope, self.start_x, self.start_y)
            a2 = line_equation(x1, y2, slope, self.start_x, self.start_y)
            a3 = line_equation(x2, y2, slope, self.start_x, self.start_y)
            a4 = line_equation(x2, y1, slope, self.start_x, self.start_y)
            if (
                max(y1, y2) < min(self.start_y, self.end_y)
                or min(y1, y2) > max(self.start_y, self.end_y)
                or max(x1, x2) < min(self.start_x, self.end_x)
                or min(x1, x2) > max(self.start_x, self.end_x)
            ):
                return False
            return not (
                (a1 >= 0 and a2 >= 0 and a3 >= 0 and a4 >= 0)
                or (a1 < 0 and a2 < 0 and a3 < 0 and a4 < 0)
            )
        else:
            return x1 <= self.start_x <= x2 or x1 >= self.start_x >= x2
    
    def update_color(self,color,flag):
        if flag:
            self.color=color
        self.canvas.itemconfigure(self.shape, fill=color)

    def deepcope(self):
        copied_line = Line(self.canvas, self.start_x, self.start_y,self.color)
        copied_line.end_x = self.end_x
        copied_line.end_y = self.end_y
        copied_line.is_move = self.is_move
        copied_line.shape = self.canvas.create_line(
            self.start_x, self.start_y, self.end_x, self.end_y, fill="black"
        )
        return copied_line


class DrawingApp:
    def __init__(self, controlcenter):
        self.selected_value= tk.StringVar()
        self.selected_value2=tk.StringVar()
        self.color="black"
        self.edit_color="black"
        self.edit_radius=0
        self.radius=0
        self.controlcenter = controlcenter
        self.canvas = self.controlcenter.canvas
        # self.canvas = tk.Canvas(master, width=400, height=400, bg="white")
        # self.canvas.pack()
        
        self.selected_item = None
        self.shapes = []
        self.first_move = False
        self.selection_rect = None
        # self.toolbar = tk.Frame(master)
        # self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.controlcenter.select_btn.configure(command=self.activate_selection)
        # self.controlcenter.select_btn.pack(side=tk.LEFT)

        self.controlcenter.move_btn.configure(command=self.activate_move_mode)
        # self.controlcenter.move_btn.pack(side=tk.LEFT)

        self.controlcenter.copy_btn.configure(command=self.activate_copy_mode)
        # self.controlcenter.copy_btn.pack(side=tk.LEFT)

        self.controlcenter.rect_btn.configure(command=self.draw_rectangle)
        # self.controlcenter.rect_btn.pack(side=tk.LEFT)

        self.controlcenter.line_btn.configure(command=self.draw_line)

        self.controlcenter.delete_btn.configure(command=self.delete_selected)
        # self.controlcenter.delete_btn.pack(side=tk.LEFT)

        self.controlcenter.group_btn.configure(command=self.group_selected)
        # self.controlcenter.group_btn.pack(side=tk.LEFT)

        self.controlcenter.ungroup_btn.configure(command=self.ungroup_selected)
        # self.controlcenter.ungroup_btn.pack(side=tk.LEFT)

        self.controlcenter.ungroup_all_btn.configure(command=self.ungroup_all)
        # self.controlcenter.ungroup_all_btn.pack(side=tk.LEFT)

        self.controlcenter.edit_btn.configure(command=self.open_dialog)
        # self.controlcenter.edit_btn.pack(side=tk.LEFT)

        self.controlcenter.red_color_btn.configure(command=self.set_color_red)

        self.controlcenter.green_color_btn.configure(command=self.set_color_green)
        # self.controlcenter.green_color_btn.pack(side=tk.TOP)

        self.controlcenter.blue_color_btn.configure(command=self.set_color_blue)
        # self.controlcenter.blue_color_btn.pack(side=tk.TOP)

        self.controlcenter.black_color_btn.configure(command=self.set_color_black)
        # self.controlcenter.black_color_btn.pack(side=tk.TOP)

        # self.controlcenter.radio = tk.IntVar()     
        self.controlcenter.R1.configure(command=self.set_rounded)
        # self.controlcenter.R1.pack(side=tk.TOP)  
        self.controlcenter.R2.configure(command=self.set_unrounded)
        # self.controlcenter.R2.pack(side=tk.TOP)
        self.controlcenter.radio.set(2)

        self.select_mode = False

        self.move_mode = False
        self.copy_mode = False
        self.move_start_x = None
        self.move_start_y = None

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    def draw_rectangle(self):
        self.selected_item = Rectangle
        self.controlcenter.rect_btn.config(bg='yellow')
        self.controlcenter.select_btn.config(bg='lightgrey')
        self.controlcenter.line_btn.config(bg='lightgrey')
        self.controlcenter.move_btn.config(bg='lightgrey')
        self.controlcenter.copy_btn.config(bg='lightgrey')
        self.controlcenter.delete_btn.config(bg='lightgrey')
        self.controlcenter.group_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_all_btn.config(bg='lightgrey')
        self.controlcenter.edit_btn.config(bg='lightgrey')
        self.activate_draw_mode()

    def draw_line(self):
        self.selected_item = Line
        self.controlcenter.line_btn.config(bg='yellow')
        self.controlcenter.rect_btn.config(bg='lightgrey')
        self.controlcenter.select_btn.config(bg='lightgrey')
        self.controlcenter.move_btn.config(bg='lightgrey')
        self.controlcenter.copy_btn.config(bg='lightgrey')
        self.controlcenter.delete_btn.config(bg='lightgrey')
        self.controlcenter.group_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_all_btn.config(bg='lightgrey')
        self.controlcenter.edit_btn.config(bg='lightgrey')
        self.activate_draw_mode()

    def activate_selection(self):
        self.controlcenter.select_btn.config(bg='yellow')
        self.controlcenter.rect_btn.config(bg='lightgrey')
        self.controlcenter.line_btn.config(bg='lightgrey')
        self.controlcenter.move_btn.config(bg='lightgrey')
        self.controlcenter.copy_btn.config(bg='lightgrey')
        self.controlcenter.delete_btn.config(bg='lightgrey')
        self.controlcenter.group_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_all_btn.config(bg='lightgrey')
        self.controlcenter.edit_btn.config(bg='lightgrey')
        self.selected_item = None
        if self.selection_rect:
            print("hello,yaha kaise aaya")
            self.reset_selected_color()
            self.canvas.delete(self.selection_rect)
            self.selection_rect=None
        print("i am here")
        self.select_mode = True
        self.selection_rect = None

    def activate_draw_mode(self):
        self.select_mode = False
        if self.selection_rect:
            self.reset_selected_color()
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None

    def on_option_select(self):
        selected = self.selected_value.get()
        self.color=selected

    def on_option_select2(self):
        selected = self.selected_value2.get()
        self.radius=int(selected)

    def start_draw(self, event):
        if self.select_mode:
            self.start_x = event.x
            self.start_y = event.y
        elif self.move_mode or self.copy_mode:
            self.move_start_x = event.x
            self.move_start_y = event.y
        else:
            if self.selected_item == Rectangle:
                self.start_x = event.x
                self.start_y = event.y
                shape = Rectangle(self.canvas, event.x, event.y,event.x,event.y,self.color,self.radius)
                self.shapes.append(shape)
            elif self.selected_item == Line:
                self.start_x = event.x
                self.start_y = event.y
                shape = Line(self.canvas, event.x, event.y,self.color)
                self.shapes.append(shape)

    def draw(self, event):
        if self.select_mode:
            if self.selection_rect:
                self.reset_selected_color()
                self.canvas.delete(self.selection_rect)
                self.selection_rect=None
            self.selection_rect = self.canvas.create_rectangle(
                self.start_x,
                self.start_y,
                event.x,
                event.y,
                dash=(2, 2),
                outline="black",
            )
        elif self.move_mode:
            self.move_selected(event)
        elif self.copy_mode:
            self.copy_selected(event)
        else:
            if self.selected_item == Rectangle or self.selected_item == Line:
                if self.selection_rect:
                    self.reset_selected_color()
                    self.canvas.delete(self.selection_rect)
                self.selection_rect = None
                self.shapes[-1].update(event.x, event.y)

    def reset_selected_color(self):
        if self.selection_rect:
            x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
            for i in range(len(self.shapes)):
                if type(self.shapes[i]) == list:
                    flattened_list = flatten_list(self.shapes[i])
                    for j in range(len(flattened_list)):
                        if flattened_list[j].intersect(x1, y1, x2, y2):
                            for elem in flattened_list:
                                # self.canvas.addtag_withtag('selected-object',elem.shape)
                                elem.update_color(elem.color,0)
                            break

                elif self.shapes[i].intersect(x1, y1, x2, y2):
                    # self.canvas.addtag_withtag('selected-object', self.shapes[i].shape)
                    self.shapes[i].update_color(self.shapes[i].color,0)

    def end_draw(self, event):
        if self.select_mode:
            x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
            for i in range(len(self.shapes)):
                if type(self.shapes[i]) == list:
                    flattened_list = flatten_list(self.shapes[i])
                    for j in range(len(flattened_list)):
                        if flattened_list[j].intersect(x1, y1, x2, y2):
                            for elem in flattened_list:
                                # self.canvas.addtag_withtag('selected-object',elem.shape)
                                elem.update_color("cyan",0)
                                # print("updated_color:",elem.color)
                            # return

                elif self.shapes[i].intersect(x1, y1, x2, y2):
                    self.shapes[i].update_color("cyan",0)
                    # print("updated color:",self.shapes[i].color)
                    # return
            # self.reset_selected_color()
            # self.canvas.delete(self.selection_rect)

        elif self.move_mode:
            self.end_move(event)

        elif self.copy_mode:
            self.end_copy(event)

    def open_dialog(self):
        self.controlcenter.edit_btn.config(bg='yellow')
        self.controlcenter.rect_btn.config(bg='lightgrey')
        self.controlcenter.select_btn.config(bg='lightgrey')
        self.controlcenter.line_btn.config(bg='lightgrey')
        self.controlcenter.move_btn.config(bg='lightgrey')
        self.controlcenter.copy_btn.config(bg='lightgrey')
        self.controlcenter.delete_btn.config(bg='lightgrey')
        self.controlcenter.group_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_all_btn.config(bg='lightgrey')
        if self.selection_rect:
            x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
            count=0
            for shape in self.shapes:
                if type(shape)!=list:
                    if shape.intersect(x1, y1, x2, y2):
                        count+=1
                        temp_shape=shape
                        if count==2:
                            break
                else:
                    flattened_list = flatten_list(shape)
                    for j in range(len(flattened_list)):
                        if flattened_list[j].intersect(x1, y1, x2, y2):
                            count=2
                    if count==2:
                        break
                
 

            
            if count!=1:
                self.reset_selected_color()
                self.canvas.delete(self.selection_rect)
                self.selection_rect = None
                return
            
            dialog = tk.Toplevel(self.canvas)
            dialog.title("Input Dialog")
            # Entry for inputting text
            # tk.Label(dialog, text="Color:").grid(row=0, column=0)
            # color_entry = tk.Entry(dialog)
            # color_entry.grid(row=0, column=1)
            # red_button_border = tk.Frame(dialog, highlightbackground = "black",  highlightthickness = 2, bd=0)
            if temp_shape.color=='red':
                self.edit_color='red'
                self.red_edit_button=tk.Button(dialog,fg='red',bg='red',bd=5, text="", command=self.set_edit_color_red)
            else:
                self.red_edit_button=tk.Button(dialog,fg='red',bg='red',bd=0, text="", command=self.set_edit_color_red)
            self.red_edit_button.pack(side=tk.TOP)
            
            if temp_shape.color=='green':
                self.edit_color='green'
                self.green_edit_button=tk.Button(dialog,fg='green',bg='green',bd=5, text="", command=self.set_edit_color_green)
            else:
                self.green_edit_button=tk.Button(dialog,fg='green',bg='green',bd=0, text="", command=self.set_edit_color_green)
            self.green_edit_button.pack(side=tk.TOP)

            if temp_shape.color=='blue':
                self.edit_color='blue'
                self.blue_edit_button=tk.Button(dialog,fg='blue',bg='blue',bd=5, text="", command=self.set_edit_color_blue)
            else:
                self.blue_edit_button=tk.Button(dialog,fg='blue',bg='blue',bd=0, text="", command=self.set_edit_color_blue)
            self.blue_edit_button.pack(side=tk.TOP)

            if temp_shape.color=='black':
                self.edit_color='black'
                self.black_edit_button=tk.Button(dialog,fg='black',bg='black',bd=5, text="", command=self.set_edit_color_black)
            else:
                self.black_edit_button=tk.Button(dialog,fg='black',bg='black',bd=0, text="", command=self.set_edit_color_black)
            self.black_edit_button.pack(side=tk.TOP)
            
            
            if isinstance(temp_shape,Rectangle):
                # # Scale widget for selecting a numerical value
                # tk.Label(dialog, text="Radius:").grid(row=2, column=0)
                # radius_scale = tk.Scale(dialog, from_=0, to=50, orient=tk.HORIZONTAL)
                # radius_scale.grid(row=2, column=1)
                # rounded_button=tk.Button(dialog, text="ROUNDED", command=self.set_edit_rounded)
                # rounded_button.pack(side=tk.TOP)
                self.edit_radio = tk.IntVar()     
                self.edit_R1 = tk.Radiobutton(dialog, text="ROUNDED", variable=self.edit_radio, value=1,  command=self.set_edit_rounded)  
                self.edit_R1.pack(side=tk.TOP)  
                self.edit_R2 = tk.Radiobutton(dialog, text="UNROUNDED", variable=self.edit_radio, value=2,  command=self.set_edit_unrounded)  
                self.edit_R2.pack(side=tk.TOP)
                if temp_shape.radius==0:
                    self.edit_radius=0
                    self.edit_radio.set(2)
                else:
                    self.edit_radius=25
                    self.edit_radio.set(1)
            # Button to submit the inputs
            if isinstance(temp_shape,Rectangle):
                submit_button = tk.Button(dialog, text="Submit", command=lambda: self.edit_selected(self.edit_color,  self.edit_radius,dialog))
            else:
                submit_button = tk.Button(dialog, text="Submit", command=lambda: self.edit_selected(self.edit_color,  0,dialog))
            # submit_button.grid(row=4, columnspan=2)
            submit_button.pack(side=tk.TOP)

    def set_edit_color_red(self):
        self.edit_color="red"
        self.red_edit_button.config(bd=5)
        self.green_edit_button.config(bd=0)
        self.black_edit_button.config(bd=0)
        self.blue_edit_button.config(bd=0)
        return
    def set_edit_color_green(self):
        self.edit_color="green"
        self.green_edit_button.config(bd=5)
        self.red_edit_button.config(bd=0)
        self.black_edit_button.config(bd=0)
        self.blue_edit_button.config(bd=0)
        return
    def set_edit_color_blue(self):
        self.edit_color="blue"
        self.blue_edit_button.config(bd=5)
        self.red_edit_button.config(bd=0)
        self.green_edit_button.config(bd=0)
        self.black_edit_button.config(bd=0)
        return
    def set_edit_color_black(self):
        self.edit_color="black"
        self.black_edit_button.config(bd=5)
        self.red_edit_button.config(bd=0)
        self.green_edit_button.config(bd=0)
        self.blue_edit_button.config(bd=0)


    def set_color_red(self):
        self.color="red"
        self.controlcenter.red_color_btn.config(bd=5)
        self.controlcenter.green_color_btn.config(bd=0)
        self.controlcenter.black_color_btn.config(bd=0)
        self.controlcenter.blue_color_btn.config(bd=0)
        return
    def set_color_green(self):
        self.color="green"
        self.controlcenter.green_color_btn.config(bd=5)
        self.controlcenter.red_color_btn.config(bd=0)
        self.controlcenter.black_color_btn.config(bd=0)
        self.controlcenter.blue_color_btn.config(bd=0)
        return
    def set_color_blue(self):
        self.color="blue"
        self.controlcenter.blue_color_btn.config(bd=5)
        self.controlcenter.red_color_btn.config(bd=0)
        self.controlcenter.green_color_btn.config(bd=0)
        self.controlcenter.black_color_btn.config(bd=0)
        return
    def set_color_black(self):
        self.color="black"
        self.controlcenter.black_color_btn.config(bd=5)
        self.controlcenter.red_color_btn.config(bd=0)
        self.controlcenter.green_color_btn.config(bd=0)
        self.controlcenter.blue_color_btn.config(bd=0)

    def set_edit_rounded(self):
        self.edit_radius=25
        return
    def set_edit_unrounded(self):
        self.edit_radius=0
        return
    
    def set_rounded(self):
        self.radius=25
        return
    def set_unrounded(self):
        self.radius=0
        return
    
    def edit_selected(self,color, radius,dialog):
        dialog.destroy()
        self.controlcenter.edit_btn.config(bg='lightgrey')
        self.controlcenter.rect_btn.config(bg='lightgrey')
        self.controlcenter.select_btn.config(bg='lightgrey')
        self.controlcenter.line_btn.config(bg='lightgrey')
        self.controlcenter.move_btn.config(bg='lightgrey')
        self.controlcenter.copy_btn.config(bg='lightgrey')
        self.controlcenter.delete_btn.config(bg='lightgrey')
        self.controlcenter.group_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_all_btn.config(bg='lightgrey')
        if self.selection_rect:
            x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
            # selected_shapes = []
            for i in range(len(self.shapes)):
                if type(self.shapes[i]) != list:
                    if self.shapes[i].intersect(x1, y1, x2, y2):
                        if isinstance(self.shapes[i],Rectangle):
                            self.shapes[i].update_radius(self.shapes[i].end_x,self.shapes[i].end_y,int(radius))
                        self.shapes[i].update_color(color,1)  
            self.reset_selected_color()
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None

    def group_selected(self):
        self.controlcenter.group_btn.config(bg='yellow')
        self.controlcenter.rect_btn.config(bg='lightgrey')
        self.controlcenter.select_btn.config(bg='lightgrey')
        self.controlcenter.line_btn.config(bg='lightgrey')
        self.controlcenter.move_btn.config(bg='lightgrey')
        self.controlcenter.copy_btn.config(bg='lightgrey')
        self.controlcenter.delete_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_all_btn.config(bg='lightgrey')
        self.controlcenter.edit_btn.config(bg='lightgrey')
        group_list = []
        temp_list = []
        if self.selection_rect:
            x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
            for i in range(len(self.shapes)):

                if type(self.shapes[i]) == list:
                    flattened_list = flatten_list(self.shapes[i])
                    for j in range(len(flattened_list)):
                        if flattened_list[j].intersect(x1, y1, x2, y2):
                            group_list.append(self.shapes[i])
                            temp_list.append(i)

                elif self.shapes[i].intersect(x1, y1, x2, y2):
                    group_list.append(self.shapes[i])
                    temp_list.append(i)

            for i in list(range(len(temp_list))):
                self.shapes.pop(temp_list[i])
                for j in range(i + 1, len(temp_list)):
                    temp_list[j] -= 1
            self.shapes.append(group_list)
            self.activate_draw_mode()
        print(self.shapes)

    def activate_move_mode(self):
        self.controlcenter.move_btn.config(bg='yellow')
        self.controlcenter.rect_btn.config(bg='lightgrey')
        self.controlcenter.select_btn.config(bg='lightgrey')
        self.controlcenter.line_btn.config(bg='lightgrey')
        self.controlcenter.copy_btn.config(bg='lightgrey')
        self.controlcenter.delete_btn.config(bg='lightgrey')
        self.controlcenter.group_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_all_btn.config(bg='lightgrey')
        self.controlcenter.edit_btn.config(bg='lightgrey')
        if self.selection_rect:
            self.select_mode = False
            self.move_mode = True
            self.first_move = True

    def activate_copy_mode(self):
        self.controlcenter.copy_btn.config(bg='yellow')
        self.controlcenter.ungroup_all_btn.config(bg='lightgrey')
        self.controlcenter.rect_btn.config(bg='lightgrey')
        self.controlcenter.select_btn.config(bg='lightgrey')
        self.controlcenter.line_btn.config(bg='lightgrey')
        self.controlcenter.move_btn.config(bg='lightgrey')
        self.controlcenter.delete_btn.config(bg='lightgrey')
        self.controlcenter.group_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_btn.config(bg='lightgrey')
        self.controlcenter.edit_btn.config(bg='lightgrey')
        if self.selection_rect:
            self.select_mode = False
            self.copy_mode = True
            self.first_move = True

    def delete_selected(self):
        self.controlcenter.delete_btn.config(bg='yellow')
        self.controlcenter.rect_btn.config(bg='lightgrey')
        self.controlcenter.select_btn.config(bg='lightgrey')
        self.controlcenter.line_btn.config(bg='lightgrey')
        self.controlcenter.move_btn.config(bg='lightgrey')
        self.controlcenter.copy_btn.config(bg='lightgrey')
        self.controlcenter.group_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_all_btn.config(bg='lightgrey')
        self.controlcenter.edit_btn.config(bg='lightgrey')
        temp_list = []
        if self.selection_rect:
            x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
            for i in range(len(self.shapes)):
                if type(self.shapes[i]) == list:
                    flattened_list = flatten_list(self.shapes[i])
                    for j in range(len(flattened_list)):
                        if flattened_list[j].intersect(x1, y1, x2, y2):
                            for del_elem in flattened_list:
                                self.canvas.delete(del_elem.shape)
                            temp_list.append(i)
                            break

                elif self.shapes[i].intersect(x1, y1, x2, y2):
                    self.canvas.delete(self.shapes[i].shape)
                    temp_list.append(i)

            for i in list(range(len(temp_list))):
                self.shapes.pop(temp_list[i])
                for j in range(i + 1, len(temp_list)):
                    temp_list[j] -= 1
        self.activate_draw_mode()

    def move_selected(self, event):
        if self.move_mode:
            if self.selection_rect:
                x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
                dx = event.x - self.move_start_x
                dy = event.y - self.move_start_y
                for i in range(len(self.shapes)):
                    if type(self.shapes[i]) == list:
                        flattened_list = list(flatten2(self.shapes[i]))
                        for j in range(len(flattened_list)):
                            if flattened_list[j].intersect(x1, y1, x2, y2) and (
                                self.first_move or flattened_list[j].is_move
                            ):
                                for elem in flattened_list:
                                    self.canvas.move(elem.shape, dx, dy)
                                    elem.start_x += dx
                                    elem.end_x += dx
                                    elem.start_y += dy
                                    elem.end_y += dy
                                    if self.first_move:
                                        elem.is_move = True
                                break

                    elif self.shapes[i].intersect(x1, y1, x2, y2) and (
                        self.first_move or self.shapes[i].is_move
                    ):
                        self.canvas.move(self.shapes[i].shape, dx, dy)
                        self.shapes[i].start_x += dx
                        self.shapes[i].end_x += dx
                        self.shapes[i].start_y += dy
                        self.shapes[i].end_y += dy
                        if self.first_move:
                            self.shapes[i].is_move = True

                self.first_move = False
                self.canvas.move(self.selection_rect, dx, dy)

                self.move_start_x = event.x
                self.move_start_y = event.y

    def copy_selected(self, event):
        if self.copy_mode:
            if self.selection_rect:
                x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
                dx = event.x - self.move_start_x
                dy = event.y - self.move_start_y
                for i in range(len(self.shapes)):
                    if type(self.shapes[i]) == list:
                        flattened_list = list(flatten2(self.shapes[i]))
                        for j in range(len(flattened_list)):
                            if flattened_list[j].intersect(x1, y1, x2, y2) and (
                                self.first_move or flattened_list[j].is_move
                            ):
                                for ele_cop in flattened_list:
                                    if self.first_move:
                                        copied = ele_cop.deepcope()
                                        self.shapes.append(copied)
                                        self.shapes[-1].is_move = False
                                for elem in flattened_list:
                                    self.canvas.move(elem.shape, dx, dy)
                                    elem.start_x += dx
                                    elem.end_x += dx
                                    elem.start_y += dy
                                    elem.end_y += dy
                                    if self.first_move:
                                        elem.is_move = True
                                break

                    elif self.shapes[i].intersect(x1, y1, x2, y2) and (
                        self.first_move or self.shapes[i].is_move
                    ):
                        if self.first_move:
                            copied = self.shapes[i].deepcope()
                            self.shapes.append(copied)
                            self.shapes[-1].is_move = False
                        self.canvas.move(self.shapes[i].shape, dx, dy)
                        self.shapes[i].start_x += dx
                        self.shapes[i].end_x += dx
                        self.shapes[i].start_y += dy
                        self.shapes[i].end_y += dy
                        if self.first_move:
                            self.shapes[i].is_move = True

                self.first_move = False
                self.canvas.move(self.selection_rect, dx, dy)
                self.move_start_x = event.x
                self.move_start_y = event.y

    def end_move(self, event):
        self.reset_selected_color()
        self.canvas.delete(self.selection_rect)
        self.selection_rect=None
        self.move_start_x = None
        self.move_start_y = None
        self.move_mode = False
        for i in range(len(self.shapes)):
            if type(self.shapes[i]) == list:
                flattened_list = list(flatten2(self.shapes[i]))
                for j in range(len(flattened_list)):
                    flattened_list[j].is_move = False
            else:
                self.shapes[i].is_move = False

    def end_copy(self, event):
        self.reset_selected_color()
        self.canvas.delete(self.selection_rect)
        self.selection_rect=None
        self.move_start_x = None
        self.move_start_y = None
        self.copy_mode = False
        self.move_mode=False
        for i in range(len(self.shapes)):
            if type(self.shapes[i]) == list:
                flattened_list = list(flatten2(self.shapes[i]))
                for j in range(len(flattened_list)):
                    flattened_list[j].is_move = False
            else:
                self.shapes[i].is_move = False

    def ungroup_selected(self):
        self.reset_selected_color()
        self.controlcenter.ungroup_btn.config(bg='yellow')
        self.controlcenter.rect_btn.config(bg='lightgrey')
        self.controlcenter.select_btn.config(bg='lightgrey')
        self.controlcenter.line_btn.config(bg='lightgrey')
        self.controlcenter.move_btn.config(bg='lightgrey')
        self.controlcenter.copy_btn.config(bg='lightgrey')
        self.controlcenter.delete_btn.config(bg='lightgrey')
        self.controlcenter.group_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_all_btn.config(bg='lightgrey')
        self.controlcenter.edit_btn.config(bg='lightgrey')
        if self.selection_rect:
            x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
            for i in range(len(self.shapes)):
                if type(self.shapes[i]) == list:
                    flattened_list = flatten_list(self.shapes[i])
                    flag = False
                    for ele in flattened_list:
                        if ele.intersect(x1, y1, x2, y2):
                            flag = True
                            break
                    if flag:
                        self.shapes.extend(self.shapes[i])
                        self.shapes.pop(i)
            print(self.shapes)
        self.activate_draw_mode()

    def ungroup_all(self):
        self.controlcenter.ungroup_all_btn.config(bg='yellow')
        self.controlcenter.rect_btn.config(bg='lightgrey')
        self.controlcenter.select_btn.config(bg='lightgrey')
        self.controlcenter.line_btn.config(bg='lightgrey')
        self.controlcenter.move_btn.config(bg='lightgrey')
        self.controlcenter.copy_btn.config(bg='lightgrey')
        self.controlcenter.delete_btn.config(bg='lightgrey')
        self.controlcenter.group_btn.config(bg='lightgrey')
        self.controlcenter.ungroup_btn.config(bg='lightgrey')
        self.controlcenter.edit_btn.config(bg='lightgrey')
        self.shapes = flatten_list(self.shapes)
        self.activate_draw_mode()
        print(self.shapes)


def main():
    control_center = ControlCenter()
    app = DrawingApp(control_center)
    control_center.root.mainloop()


if __name__ == "__main__":
    main()