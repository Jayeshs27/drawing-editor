import xml.etree.ElementTree as ET


class Rectangle:
    def __init__(
        self, upper_left_x, upper_left_y, lower_right_x, lower_right_y, color, corner
    ):
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


def read_shapes_from_xml(parent_element):
    shapes_list = []
    for child in parent_element:
        if child.tag == "group":
            shapes_list.append(read_shapes_from_xml(child))
        elif child.tag == "line":
            begin = child.find("begin")
            end = child.find("end")
            line = Line(
                int(begin.find("x").text),
                int(begin.find("y").text),
                int(end.find("x").text),
                int(end.find("y").text),
                child.find("color").text,
            )
            shapes_list.append(line)
        elif child.tag == "rectangle":
            upper_left = child.find("upper-left")
            lower_right = child.find("lower-right")
            rectangle = Rectangle(
                int(upper_left.find("x").text),
                int(upper_left.find("y").text),
                int(lower_right.find("x").text),
                int(lower_right.find("y").text),
                child.find("color").text,
                child.find("corner").text,
            )
            shapes_list.append(rectangle)
    return shapes_list


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


# Read the content of the file
with open("shapes_info2.xml", "r") as file:
    content = file.read()

# Wrap the content with a single root element
xml_string = f"<root>{content}</root>"

root_element = ET.fromstring(xml_string)
shapes_list = read_shapes_from_xml(root_element)
print(shapes_list)


# # Writing shapes to XML
# shapes_list = [
#     Line(10, 50, 20, 25, "black"),
#     Rectangle(10, 20, 20, 35, "black", "rounded"),
#     [Line(30, 40, 50, 60, "red"), Rectangle(15, 25, 30, 40, "blue", "sharp")]
# ]

with open("shapes_info.xml", "w") as file:
    write_shapes_to_xml(shapes_list, file)
