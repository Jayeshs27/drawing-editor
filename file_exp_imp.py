import xml.etree.ElementTree as ET


class Rectangle:
    def __init__(
        self, start_x, start_y, end_x, end_y, color, r
    ):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color
        self.radius = r
class Line:
    def __init__(self, start_x, start_y, end_x, end_y, color):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color

class FileIOManager:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_shapes_from_file(self):
        raise NotImplementedError("Subclasses must implement read_shapes_from_file method")

    def write_shapes_to_file(self, shapes_list):
        raise NotImplementedError("Subclasses must implement write_shapes_to_file method")


class ASCIIFileIOManager(FileIOManager):
    def __init__(self, file_name):
        super().__init__(file_name)

    @staticmethod
    def parse_line(line):
        name_color = lambda color_code: {'k': 'black', 'r': 'red', 'g': 'green', 'b': 'blue'}.get(color_code, 'unknown')
        parts = line.strip().split()
        if parts[0] == "line":
            return Line(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), name_color(parts[5]))
        elif parts[0] == "rect":
            return Rectangle(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), name_color(parts[5]), 0 if parts[6]=='r' else 25)

    def read_shapes_from_file(self):
        shapes_list = []
        with open(self.file_name, "r") as file:
            for line in file:
                line = line.strip()
                if line == "start":
                    nested_list = []
                    shapes_list.append(nested_list)
                elif line == "end":
                    pass
                else:
                    shape_info = self.parse_line(line)
                    if shapes_list and isinstance(shapes_list[-1], list):
                        shapes_list[-1].append(shape_info)
                    else:
                        shapes_list.append(shape_info)
        return shapes_list

    def write_shapes_to_file(self, shapes_list):
        with open(self.file_name, "w") as file:
            self._write_shapes_to_file(shapes_list, file)

    @staticmethod
    def _write_shapes_to_file(shapes_list, file):
        name_color = lambda color_name: {v: k for k, v in {'k': 'black', 'r': 'red', 'g': 'green', 'b': 'blue'}.items()}.get(color_name, 'unknown')
        for shape in shapes_list:
            if isinstance(shape, list):
                file.write("start\n")
                ASCIIFileIOManager._write_shapes_to_file(shape, file)
                file.write("end\n")
            else:
                if isinstance(shape, Line):
                    file.write(f"line {shape.start_x} {shape.start_y} {shape.end_x} {shape.end_y} {name_color(shape.color)}\n")
                elif isinstance(shape, Rectangle):
                    file.write(f"rect {shape.start_x} {shape.start_y} {shape.end_x} {shape.end_y} {name_color(shape.color)} {'s' if shape.radius==0 else 'r'}\n")

class XMLFileIOManager(FileIOManager):
    def __init__(self, file_name):
        super().__init__(file_name)

    def read_shapes_from_file(self):
        with open(self.file_name, "r") as file:
            content = file.read()
        xml_string = f"<root>{content}</root>"
        root_element = ET.fromstring(xml_string)
        return self._read_shapes_from_xml(root_element)

    @staticmethod
    def _read_shapes_from_xml(parent_element):
        shapes_list = []
        for child in parent_element:
            if child.tag == "group":
                shapes_list.append(XMLFileIOManager._read_shapes_from_xml(child))
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
                    0 if child.find("corner").text=='rounded' else 25,
                )
                shapes_list.append(rectangle)
        return shapes_list

    def write_shapes_to_file(self, shapes_list):
        print(self.file_name)
        print(shapes_list[0].start_x)
        with open(self.file_name, "w") as file:
            self._write_shapes_to_xml(shapes_list, file)

    @staticmethod
    def _write_shapes_to_xml(shapes_list, file, indent=0):
        def write_indent():
            file.write("\t" * indent)

        for shape in shapes_list:
            write_indent()
            if isinstance(shape, Line):
                file.write("<line>\n")
                write_indent()
                file.write("\t<begin>\n")
                write_indent()
                file.write(f"\t\t<x>{shape.start_x}</x>\n")
                write_indent()
                file.write(f"\t\t<y>{shape.start_y}</y>\n")
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
                file.write(f"\t\t<x>{shape.start_x}</x>\n")
                write_indent()
                file.write(f"\t\t<y>{shape.start_y}</y>\n")
                write_indent()
                file.write("\t</upper-left>\n")
                write_indent()
                file.write("\t<lower-right>\n")
                write_indent()
                file.write(f"\t\t<x>{shape.end_x}</x>\n")
                write_indent()
                file.write(f"\t\t<y>{shape.end_y}</y>\n")
                write_indent()
                file.write("\t</lower-right>\n")
                write_indent()
                file.write(f"\t<color>{shape.color}</color>\n")
                write_indent()
                file.write(f"\t<corner>{'square' if shape.radius==0 else 'rounded'}</corner>\n")
                write_indent()
                file.write("</rectangle>\n")
            elif isinstance(shape, list):
                write_indent()
                file.write("<group>\n")
                XMLFileIOManager._write_shapes_to_xml(shape, file, indent + 1)
                write_indent()
                file.write("</group>\n")
shapes_list = [
    Line(10, 10, 50, 50, "blue"),
    Rectangle(20, 20, 80, 80, "red", 25),
    [Line(30, 30, 70, 70, "green"), Rectangle(40, 40, 90, 90, "blue", 0)]
]
new_xml_manager = XMLFileIOManager("shapes_info.xml")
new_xml_manager.write_shapes_to_file(shapes_list)

# xml_manager = XMLFileIOManager("shapes_info.xml")
# shapes_list = xml_manager.read_shapes_from_file()
# new_xml_manager = XMLFileIOManager("new.xml")
# new_xml_manager.write_shapes_to_file(shapes_list)

new_ascii_manager = ASCIIFileIOManager("shapes_info.txt")
new_ascii_manager.write_shapes_to_file(shapes_list)

# ascii_manager = ASCIIFileIOManager("shapes_info.txt")
# shapes_list = ascii_manager.read_shapes_from_file()
# new_ascii_manager = ASCIIFileIOManager("new.txt")
# new_ascii_manager.write_shapes_to_file(shapes_list)