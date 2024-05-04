import tkinter as tk
import random

class Rectangle:
    def __init__(self, start_x, start_y, end_x, end_y, color, is_rounded):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color
        self.is_rounded = is_rounded

class Line:
    def __init__(self, start_x, start_y, end_x, end_y, color):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color

def parse_line(line):
    parts = line.strip().split()
    if parts[0] == "line":
        return Line(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), parts[5])
    elif parts[0] == "rect":
        return Rectangle(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), parts[5], parts[6])

def read_shapes_from_file(file_name):
    shapes_list = []
    with open(file_name, "r") as file:
        for line in file:
            line = line.strip()
            if line == "start":
                nested_list = []
                shapes_list.append(nested_list)
            elif line == "end":
                pass
            else:
                shape_info = parse_line(line)
                if shapes_list and isinstance(shapes_list[-1], list):
                    shapes_list[-1].append(shape_info)
                else:
                    shapes_list.append(shape_info)
    return shapes_list

def write_shapes_to_file(shapes_list, file):
    for shape in shapes_list:
        if isinstance(shape, list):
            file.write("start\n")
            write_shapes_to_file(shape, file)
            file.write("end\n")
        else:
            if isinstance(shape, Line):
                file.write(f"line {shape.start_x} {shape.start_y} {shape.end_x} {shape.end_y} {shape.color}\n")
            elif isinstance(shape, Rectangle):
                file.write(f"rect {shape.start_x} {shape.start_y} {shape.end_x} {shape.end_y} {shape.color} {shape.is_rounded}\n")

# Reading shapes from file
shapes_list = read_shapes_from_file("shapes_info.txt")
print(shapes_list)

# Writing shapes to file
# shapes_list = [
#     Line(10, 10, 50, 50, "b"),
#     Rectangle(20, 20, 80, 80, "r", "s"),
#     [Line(30, 30, 70, 70, "g"), Rectangle(40, 40, 90, 90, "b", "r")]
# ]

with open("shapes_info2.txt", "w") as file:
    write_shapes_to_file(shapes_list, file)

