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
        pass

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
