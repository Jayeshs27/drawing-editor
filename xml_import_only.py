import random

class Rectangle:
    def __init__(self, upper_left_x, upper_left_y, lower_right_x, lower_right_y, color, corner):
        self.upper_left_x = upper_left_x
        self.upper_left_y = upper_left_y
        self.lower_right_x = lower_right_x
        self.lower_right_y = lower_right_y
        self.color = color
        self.corner = corner

class Line:
    def __init__(self, begin_x, begin_y, end_x, end_y, color):
        self.begin_x = begin_x
        self.begin_y = begin_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color

def write_shapes_to_xml(shapes_list, file, indent=0):
    def write_indent():
        file.write("\t" * indent)

    for shape in shapes_list:
        write_indent()
        if isinstance(shape, Line):
            file.write("<line>\n")
            write_indent()
            file.write("\t<begin>\n")
            write_indent()
            file.write(f"\t\t<x>{shape.begin_x}</x>\n")
            write_indent()
            file.write(f"\t\t<y>{shape.begin_y}</y>\n")
            write_indent()
            file.write("\t</begin>\n")
            write_indent()
            file.write("\t<end>\n")
            write_indent()
            file.write(f"\t\t<x>{shape.end_x}</x>\n")
            write_indent()
            file.write(f"\t\t<y>{shape.end_y}</y>\n")
            write_indent()
            file.write("\t</end>\n")
            write_indent()
            file.write(f"\t<color>{shape.color}</color>\n")
            write_indent()
            file.write("</line>\n")
        elif isinstance(shape, Rectangle):
            file.write("<rectangle>\n")
            write_indent()
            file.write("\t<upper-left>\n")
            write_indent()
            file.write(f"\t\t<x>{shape.upper_left_x}</x>\n")
            write_indent()
            file.write(f"\t\t<y>{shape.upper_left_y}</y>\n")
            write_indent()
            file.write("\t</upper-left>\n")
            write_indent()
            file.write("\t<lower-right>\n")
            write_indent()
            file.write(f"\t\t<x>{shape.lower_right_x}</x>\n")
            write_indent()
            file.write(f"\t\t<y>{shape.lower_right_y}</y>\n")
            write_indent()
            file.write("\t</lower-right>\n")
            write_indent()
            file.write(f"\t<color>{shape.color}</color>\n")
            write_indent()
            file.write(f"\t<corner>{shape.corner}</corner>\n")
            write_indent()
            file.write("</rectangle>\n")
        elif isinstance(shape, list):
            write_indent()
            file.write("<group>\n")
            write_shapes_to_xml(shape, file, indent + 1)
            write_indent()
            file.write("</group>\n")

# Writing shapes to XML
shapes_list = [
    Line(10, 50, 20, 25, "black"),
    Rectangle(10, 20, 20, 35, "black", "rounded"),
    [Line(30, 40, 50, 60, "red"), Rectangle(15, 25, 30, 40, "blue", "sharp")]
]

with open("shapes_info.xml", "w") as file:
    write_shapes_to_xml(shapes_list, file)


