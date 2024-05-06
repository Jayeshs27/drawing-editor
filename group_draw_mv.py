import tkinter as tk


class Rectangle:
    def __init__(self, canvas, start_x, start_y):
        self.canvas = canvas
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = start_x
        self.end_y = start_y
        self.shape = self.canvas.create_rectangle(
            start_x, start_y, start_x, start_y, outline="black"
        )

    def update(self, end_x, end_y):
        self.end_x = end_x
        self.end_y = end_y
        self.canvas.coords(
            self.shape, self.start_x, self.start_y, self.end_x, self.end_y
        )

    def get_coords(self):
        return self.start_x, self.start_y, self.end_x, self.end_y

    # def intersect(self, x1, y1, x2, y2):
    #     return (
    #         y1 <= self.start_y <= y2
    #         or y2 <= self.start_y <= y1
    #         or y1 <= self.end_x <= y2
    #         or y2 <= self.end_x <= y2
    #         or x1 <= self.start_x <= x2
    #         or x2 <= self.start_x <= x1
    #         or x1 <= self.end_x <= x2
    #         or x2 <= self.end_x <= x1
    #     )

    def intersect(self, x1, y1, x2, y2):
        rect_x1, rect_y1, rect_x2, rect_y2 = self.get_coords()

        return not (
            x2 < rect_x1 or x1 > rect_x2 or y2 < rect_y1 or y1 > rect_y2
        ) and not ((min(self.start_x,self.end_x) < x1 < max(self.start_x,self.end_x)) and
                   (min(self.start_x,self.end_x) < x2 < max(self.start_x,self.end_x)) and 
                   (min(self.start_y,self.end_y) < y1 < max(self.start_y,self.end_y)) and
                   (min(self.start_y,self.end_y) < y2 < max(self.start_y,self.end_y))
                   ) 


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
    def __init__(self, canvas, start_x, start_y):
        self.canvas = canvas
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = start_x
        self.end_y = start_y
        self.shape = self.canvas.create_line(
            start_x, start_y, start_x, start_y, fill="black"
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
            # y_int1 = slope * (x1 - self.start_x) + self.start_y
            # y_int2 = slope * (x2 - self.start_x) + self.start_y
            # x_int1 = (y1 - self.start_y) / slope + self.start_x
            # x_int2 = (y2 - self.start_y) / slope + self.start_x
            a1 = line_equation(x1, y1, slope, self.start_x, self.start_y)
            a2 = line_equation(x1, y2, slope, self.start_x, self.start_y)
            a3 = line_equation(x2, y2, slope, self.start_x, self.start_y)
            a4 = line_equation(x2, y1, slope, self.start_x, self.start_y)
            # return x1 <= x_int1 <= x2 or x1 <= x_int2 <= x2 or y1 <= y_int1 <= y2 or y1 <= y_int2 <= y2
            return not (
                (a1 >= 0 and a2 >= 0 and a3 >= 0 and a4 >= 0)
                or (a1 < 0 and a2 < 0 and a3 < 0 and a4 < 0)
            )
        else:
            return x1 <= self.start_x <= x2 or x1 >= self.start_x >= x2


class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=400, bg="white")
        self.canvas.pack()
        self.selected_item = None
        self.shapes = []
        self.selection_rect = None
        self.toolbar = tk.Frame(master)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.select_button = tk.Button(
            self.toolbar, text="Select", command=self.activate_selection
        )
        self.select_button.pack(side=tk.LEFT)

        self.select_button = tk.Button(
            self.toolbar, text="Move", command=self.activate_move_mode
        )
        self.select_button.pack(side=tk.LEFT)

        self.select_button = tk.Button(
            self.toolbar, text="Copy", command=self.activate_move_mode
        )
        self.select_button.pack(side=tk.LEFT)

        self.rect_button = tk.Button(
            self.toolbar, text="Rectangle", command=self.draw_rectangle
        )
        self.rect_button.pack(side=tk.LEFT)

        self.line_button = tk.Button(self.toolbar, text="Line", command=self.draw_line)
        self.line_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(
            self.toolbar, text="Delete", command=self.delete_selected
        )
        self.delete_button.pack(side=tk.LEFT)

        self.group_button = tk.Button(
            self.toolbar, text="Group", command=self.group_selected
        )
        self.group_button.pack(side=tk.LEFT)

        self.group_button = tk.Button(
            self.toolbar, text="Ungroup Selected", command=self.ungroup_selected
        )
        self.group_button.pack(side=tk.LEFT)

        # self.group_button = tk.Button(
        #     self.toolbar, text="Ungroup Selected", command=self.ungroup_selected
        # )
        # self.group_button.pack(side=tk.LEFT)

        self.ungroup_all_button = tk.Button(
            self.toolbar, text="Ungroup All", command=self.ungroup_all
        )
        self.ungroup_all_button.pack(side=tk.LEFT)

        self.select_mode = False

        # move mode attributes
        self.move_mode = False  
        self.move_start_x = None
        self.move_start_y = None

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    def draw_rectangle(self):
        self.selected_item = Rectangle
        self.activate_draw_mode()

    def draw_line(self):
        self.selected_item = Line
        self.activate_draw_mode()

    def activate_selection(self):
        self.selected_item = None
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
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
        elif self.move_mode:
            self.move_start_x = event.x
            self.move_start_y = event.y
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
        else:
            if self.selected_item == Rectangle or self.selected_item == Line:
                if self.selection_rect:
                    self.canvas.delete(self.selection_rect)
                self.selection_rect = None
                self.shapes[-1].update(event.x, event.y)

    def end_draw(self, event):
        if self.select_mode:
            x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
            for i in range(len(self.shapes)):
                if type(self.shapes[i]) == list:
                    flattened_list = flatten_list(self.shapes[i])
                    for j in range(len(flattened_list)):
                        if flattened_list[j].intersect(x1, y1, x2, y2):
                            return

                elif self.shapes[i].intersect(x1, y1, x2, y2):
                    return
            
            self.canvas.delete(self.selection_rect)

        if self.move_mode:
            self.end_move(event)
        


    def group_selected(self):
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
        if self.selection_rect:
            self.select_mode = False
            self.move_mode = True

    def delete_selected(self):
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
        # self.canvas.delete('selected-object')
        self.activate_draw_mode()

    def move_selected(self, event):
        if self.move_mode:
            if self.selection_rect:
                x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
                dx = event.x - self.move_start_x
                dy = event.y - self.move_start_y
                # self.canvas.move('selected-object', dx, dy)
                for i in range(len(self.shapes)):
                    if type(self.shapes[i]) == list:
                        flattened_list = list(flatten2(self.shapes[i]))
                        for j in range(len(flattened_list)):
                            if flattened_list[j].intersect(x1, y1, x2, y2):
                                for elem in flattened_list:
                                    self.canvas.move(elem.shape, dx, dy)
                                    # elem.start_x = 20
                                    # elem.end_x = 150
                                    # elem.start_y = 20
                                    # elem.end_y = 150
                                    elem.start_x += dx
                                    elem.end_x += dx
                                    elem.start_y += dy
                                    elem.end_y += dy
                                    

                                    print("elem start = ", elem.start_x)
                                    print("shapes start = ", self.shapes[0][0].start_x)
                                break

                    elif self.shapes[i].intersect(x1, y1, x2, y2):
                        self.canvas.move(self.shapes[i].shape, dx, dy)
                        self.shapes[i].start_x += dx
                        self.shapes[i].end_x += dx
                        self.shapes[i].start_y += dy
                        self.shapes[i].end_y += dy

                        print("start_x = ", self.shapes[i].start_x)
                
                self.canvas.move(self.selection_rect, dx, dy)

                self.move_start_x = event.x
                self.move_start_y = event.y

    def end_move(self, event):
        # x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
        # for i in range(len(self.shapes)):
        #     if type(self.shapes[i]) == list:
        #         flattened_list = flatten_list(self.shapes[i])
        #         for j in range(len(flattened_list)):
        #             if flattened_list[j].intersect(x1, y1, x2, y2):
        #                 for elem in flattened_list:
        #                         self.canvas.dtag('selected-object',elem.shape)
        #                 break

        #     elif self.shapes[i].intersect(x1, y1, x2, y2):
        #         self.canvas.dtag('selected-object', self.shapes[i].shape)
        # self.canvas.dtag('selected-object',self.selection_rect)
        self.canvas.delete(self.selection_rect)
        self.move_start_x = None
        self.move_start_y = None
        self.move_mode = False

    def ungroup_selected(self):
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
        # temp_list = []
        # # if self.selection_rect:
        #     # x1, y1, x2, y2 = self.canvas.coords(self.selection_rect)
        # for i in range(len(self.shapes)):
        #     if type(self.shapes[i]) == list:
        #         flattened_list = flatten_list(self.shapes[i]) 
        #         for ungroup in range(len(flattened_list)):
        #             # if self.shapes[i][j].intersect(x1, y1, x2, y2):
        #             self.shapes.append(flattened_list[ungroup])
        #         temp_list.append(i)      
        
        #     # elif self.shapes[i].intersect(x1, y1, x2, y2):
        #     #     self.shapes.append(self.shapes[i])
        #     #     temp_list.append(i)

        # for i in list(range(len(temp_list))):
        #     self.shapes.pop(temp_list[i])
        #     for j in range(i + 1, len(temp_list)):
        #         temp_list[j] -= 1
        self.shapes = flatten_list(self.shapes)
        self.activate_draw_mode()
        print(self.shapes)


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
