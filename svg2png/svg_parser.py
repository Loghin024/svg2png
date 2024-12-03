import xml.etree.ElementTree as ET


class SVGParser:
    """"
    SVGParser class
    """
    def __init__(self, svg_file_path):
        self.svg_file_path = svg_file_path
        self.svg_attributes = dict()

    def parse(self):
        """
        Parse the SVG file
        """
        tree = ET.parse(self.svg_file_path)
        root = tree.getroot()

        # get root tag
        if root.tag == '{http://www.w3.org/2000/svg}svg':
            print('SVG file detected')
        else:
            print('This is not an SVG file')
            return

        # get the width and height of the SVG file
        width = root.attrib.get('width')
        height = root.attrib.get('height')

        elements = []
        for element in root:

            # get the tag name
            tag = element.tag.split('}')[1]
            element_dict = dict()
            element_dict['tag'] = tag

            # get the attributes
            for key, value in element.attrib.items():
                if key == 'style':
                    element_dict = self.parse_style_attribute(element_dict, value)
                else:
                    element_dict[key] = value
            elements.append(element_dict)

        self.svg_attributes['width'] = width
        self.svg_attributes['height'] = height
        self.svg_attributes['elements'] = elements

    def parse_style_attribute(self, element_dict, style):
        """
        Parse the style attribute
        :param element_dict:
        :param style:
        :return: element_dict with style attributes
        """

        style_attributes = style.split(';')
        for attribute in style_attributes:
            key, value = attribute.split(':')
            element_dict[key.strip()] = value.strip()

        return element_dict


    def get_svg_attributes(self):
        """
        Get the SVG attributes
        """
        return self.svg_attributes
