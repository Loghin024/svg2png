from PIL import Image, ImageDraw


class PNGRenderer:
    """
    PNGRenderer class is responsible for rendering the PNG image
    """

    def __init__(self, svg_attributes, png_file_path):
        self.svg_attributes = svg_attributes
        self.png_file_path = png_file_path

        # create a blank image
        self.image = Image.new('RGB', (int(self.svg_attributes['width']), int(self.svg_attributes['height'])), 'white')

    def render(self):
        """
        Render the PNG image
        """
        print('Rendering the PNG image')
        draw = ImageDraw.Draw(self.image)

        # render each svg element
        for element in self.svg_attributes['elements']:
            print(element)
            self.render_element(draw, element)

    def render_element(self, draw, element):
        """
        Render the SVG element
        """
        if element['tag'] == 'rect':
            self.render_rect(draw, element)
        elif element['tag'] == 'circle':
            self.render_circle(draw, element)
        elif element['tag'] == 'line':
            self.render_line(draw, element)
        elif element['tag'] == 'polyline':
            self.render_polyline(draw, element)
        elif element['tag'] == 'polygon':
            self.render_polygon(draw, element)
        elif element['tag'] == 'path':
            self.render_path(draw, element)

    def render_rect(self, draw, element):
        """
        Render the rectangle
        """
        x = float(element.get('x', 0))
        y = float(element.get('y', 0))
        width = float(element.get('width', 0))
        height = float(element.get('height', 0))
        fill = element.get('fill', 'black')
        rx = float(element.get('rx', 0))
        ry = float(element.get('ry', 0))
        stroke = element.get('stroke', None)
        stroke_width = int(element.get('stroke-width', 1))

        if rx == 0 and ry == 0:
            # draw normal rectangle
            draw.rectangle([x, y, x + width, y + height], fill=fill, outline=stroke, width=stroke_width)
        else:

            # draw corners using elipses
            draw.ellipse([x, y, x + 2 * rx, y + 2 * ry], fill=fill)
            draw.ellipse([x + width - 2 * rx, y, x + width, y + 2 * ry], fill=fill)
            draw.ellipse([x, y + height - 2 * ry, x + 2 * rx, y + height], fill=fill)
            draw.ellipse([x + width - 2 * rx, y + height - 2 * ry, x + width, y + height], fill=fill)

            # draw rectangles
            draw.rectangle([x + rx, y, x + width - rx, y + height], fill=fill)
            draw.rectangle([x, y + ry, x + width, y + height - ry], fill=fill)

    def render_circle(self, draw, element):
        pass

    def render_line(self, draw, element):
        pass

    def render_polyline(self, draw, element):
        pass

    def render_polygon(self, draw, element):
        pass

    def render_path(self, draw, element):
        pass

    def get_image(self):
        """
        Get the image
        """
        return self.image
