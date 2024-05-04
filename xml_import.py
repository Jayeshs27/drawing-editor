import xml.etree.ElementTree as ET
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

def write_shapes_to_xml(shapes_list, parent_element, level=0):
    indent = "  " * level
    for shape in shapes_list:
        if isinstance(shape, list):
            group_element = ET.SubElement(parent_element, "group")
            write_shapes_to_xml(shape, group_element, level + 1)
        else:
            if isinstance(shape, Line):
                line_element = ET.SubElement(parent_element, "line")
                begin_element = ET.SubElement(line_element, "begin")
                ET.SubElement(begin_element, "x").text = str(shape.begin_x)
                ET.SubElement(begin_element, "y").text = str(shape.begin_y)
                end_element = ET.SubElement(line_element, "end")
                ET.SubElement(end_element, "x").text = str(shape.end_x)
                ET.SubElement(end_element, "y").text = str(shape.end_y)
                ET.SubElement(line_element, "color").text = shape.color
            elif isinstance(shape, Rectangle):
                rect_element = ET.SubElement(parent_element, "rectangle")
                upper_left_element = ET.SubElement(rect_element, "upper-left")
                ET.SubElement(upper_left_element, "x").text = str(shape.upper_left_x)
                ET.SubElement(upper_left_element, "y").text = str(shape.upper_left_y)
                lower_right_element = ET.SubElement(rect_element, "lower-right")
                ET.SubElement(lower_right_element, "x").text = str(shape.lower_right_x)
                ET.SubElement(lower_right_element, "y").text = str(shape.lower_right_y)
                ET.SubElement(rect_element, "color").text = shape.color
                ET.SubElement(rect_element, "corner").text = shape.corner

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
                child.find("color").text
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
                child.find("corner").text
            )
            shapes_list.append(rectangle)
    return shapes_list

# Writing shapes to XML
shapes_list = [
    Line(10, 50, 20, 25, "black"),
    Rectangle(10, 20, 20, 35, "black", "rounded"),
    [Line(30, 40, 50, 60, "red"), Rectangle(15, 25, 30, 40, "blue", "sharp")]
]

root_element = ET.Element("shapes")
write_shapes_to_xml(shapes_list, root_element)
tree = ET.ElementTree(root_element)
tree.write("shapes_info.xml", encoding="utf-8", xml_declaration=True)

# Reading shapes from XML
tree = ET.parse("shapes_info.xml")
root_element = tree.getroot()
shapes_list = read_shapes_from_xml(root_element)
print(shapes_list)
