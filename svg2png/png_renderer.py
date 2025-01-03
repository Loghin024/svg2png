from PIL import Image, ImageDraw, ImagePath
import re


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
            self.render_rectangle(draw, element)
        elif element['tag'] == 'circle':
            self.render_circle(draw, element)
        elif element['tag'] == 'line':
            self.render_line(draw, element)
        elif element['tag'] == 'polyline':
            self.render_polyline(draw, element)
        elif element['tag'] == 'ellipse':
            self.render_ellipse(draw, element)
        elif element['tag'] == 'path':
            self.render_path(draw, element)

    def render_rectangle(self, draw, element):
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
        opacity = float(element.get('opacity', 1))

        if rx == 0 and ry == 0:
            # draw normal rectangle
            draw.rectangle([x, y, x + width, y + height], fill=fill, outline=stroke, width=stroke_width)
        else:

            # draw corners using ellipses
            draw.ellipse([x, y, x + 2 * rx, y + 2 * ry], fill=fill)
            draw.ellipse([x + width - 2 * rx, y, x + width, y + 2 * ry], fill=fill)
            draw.ellipse([x, y + height - 2 * ry, x + 2 * rx, y + height], fill=fill)
            draw.ellipse([x + width - 2 * rx, y + height - 2 * ry, x + width, y + height], fill=fill)

            # draw rectangles
            draw.rectangle([x + rx, y, x + width - rx, y + height], fill=fill)
            draw.rectangle([x, y + ry, x + width, y + height - ry], fill=fill)

    def render_circle(self, draw, element):
        """
        Render the circle
        """
        cx = float(element.get('cx', 0))
        cy = float(element.get('cy', 0))
        r = float(element.get('r', 0))
        fill = element.get('fill', 'black')
        stroke = element.get('stroke', None)
        stroke_width = int(element.get('stroke-width', 1))

        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=stroke, width=stroke_width)

    def render_line(self, draw, element):
        """
        Render the line
        """
        x1 = float(element.get('x1', 0))
        y1 = float(element.get('y1', 0))
        x2 = float(element.get('x2', 0))
        y2 = float(element.get('y2', 0))
        stroke = element.get('stroke', 'black')
        stroke_width = int(element.get('stroke-width', 1))

        draw.line([x1, y1, x2, y2], fill=stroke, width=stroke_width)

    def render_polyline(self, draw, element):
        """
        Render the polyline
        """
        points = element.get('points', '')
        points = points.split(' ')

        # convert from a,b to [(a,b), (c,d)]
        points = [point.split(',') for point in points]

        # convert from string to int
        points = [(int(point[0]), int(point[1])) for point in points if point]

        stroke = element.get('stroke', 'black')
        stroke_width = int(element.get('stroke-width', 1))

        draw.line(points, fill=stroke, width=stroke_width)

    def render_ellipse(self, draw, element):
        """
        Render the ellipse
        """
        cx = float(element.get('cx', 0))
        cy = float(element.get('cy', 0))
        rx = float(element.get('rx', 0))
        ry = float(element.get('ry', 0))
        fill = element.get('fill', 'black')
        stroke = element.get('stroke', None)
        stroke_width = int(element.get('stroke-width', 1))

        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=stroke, width=stroke_width)

    def render_path(self, draw, element):
        """
        Render the path, supporting all SVG path commands
        """
        path_data = element.get('d', '')
        fill = element.get('fill', None)
        stroke = element.get('stroke', None)
        stroke_width = int(element.get('stroke-width', 1))

        if fill == 'none':
            fill = None
        if stroke == 'none':
            stroke = None

        if not path_data:
            return

        try:
            path_segments = re.findall(r'[a-zA-Z]|[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', path_data)
            current_pos = [0, 0]
            start_pos = [0, 0]

            # for smooth Bézier curves
            control_point = None
            path_points = []
            i = 0

            while i < len(path_segments):
                segment = path_segments[i]

                if segment.isalpha():  # command
                    # ensure command is uppercase
                    command = segment.upper()

                    # check if command is relative
                    relative = segment.islower()
                    i += 1
                else:
                    command = None
                    relative = False

                if command == 'M':  # moveto
                    x, y = float(path_segments[i]), float(path_segments[i + 1])
                    if relative:
                        x += current_pos[0]
                        y += current_pos[1]
                    current_pos = [x, y]
                    start_pos = [x, y]
                    path_points.append(tuple(current_pos))
                    i += 2

                elif command == 'L':  # lineto
                    x, y = float(path_segments[i]), float(path_segments[i + 1])
                    if relative:
                        x += current_pos[0]
                        y += current_pos[1]
                    current_pos = [x, y]
                    path_points.append(tuple(current_pos))
                    i += 2

                elif command == 'H':  # horizontal lineto
                    x = float(path_segments[i])
                    if relative:
                        x += current_pos[0]
                    current_pos[0] = x
                    path_points.append(tuple(current_pos))
                    i += 1

                elif command == 'V':  # vertical lineto
                    y = float(path_segments[i])
                    if relative:
                        y += current_pos[1]
                    current_pos[1] = y
                    path_points.append(tuple(current_pos))
                    i += 1

                elif command == 'C':  # curveto
                    x1, y1 = float(path_segments[i]), float(path_segments[i + 1])
                    x2, y2 = float(path_segments[i + 2]), float(path_segments[i + 3])
                    x3, y3 = float(path_segments[i + 4]), float(path_segments[i + 5])
                    if relative:
                        x1 += current_pos[0]
                        y1 += current_pos[1]
                        x2 += current_pos[0]
                        y2 += current_pos[1]
                        x3 += current_pos[0]
                        y3 += current_pos[1]
                    path_points.extend(self._cubic_bezier_curve(current_pos, [x1, y1], [x2, y2], [x3, y3]))
                    control_point = [x2, y2]
                    current_pos = [x3, y3]
                    i += 6

                elif command == 'S':  # smooth curveto
                    if control_point is None:
                        control_point = current_pos
                    x1, y1 = 2 * current_pos[0] - control_point[0], 2 * current_pos[1] - control_point[1]
                    x2, y2 = float(path_segments[i]), float(path_segments[i + 1])
                    x3, y3 = float(path_segments[i + 2]), float(path_segments[i + 3])
                    if relative:
                        x2 += current_pos[0]
                        y2 += current_pos[1]
                        x3 += current_pos[0]
                        y3 += current_pos[1]
                    path_points.extend(self._cubic_bezier_curve(current_pos, [x1, y1], [x2, y2], [x3, y3]))
                    control_point = [x2, y2]
                    current_pos = [x3, y3]
                    i += 4

                elif command == 'Q':  # quadratic Bézier curve
                    x1, y1 = float(path_segments[i]), float(path_segments[i + 1])
                    x2, y2 = float(path_segments[i + 2]), float(path_segments[i + 3])
                    if relative:
                        x1 += current_pos[0]
                        y1 += current_pos[1]
                        x2 += current_pos[0]
                        y2 += current_pos[1]
                    path_points.extend(self._quadratic_bezier_curve(current_pos, [x1, y1], [x2, y2]))
                    control_point = [x1, y1]
                    current_pos = [x2, y2]
                    i += 4

                elif command == 'T':  # smooth quadratic Bézier curveto

                    if control_point is None:
                        control_point = current_pos
                    x1, y1 = 2 * current_pos[0] - control_point[0], 2 * current_pos[1] - control_point[1]
                    x2, y2 = float(path_segments[i]), float(path_segments[i + 1])
                    if relative:
                        x2 += current_pos[0]
                        y2 += current_pos[1]
                    path_points.extend(self._quadratic_bezier_curve(current_pos, [x1, y1], [x2, y2]))
                    control_point = [x1, y1]
                    current_pos = [x2, y2]
                    i += 2

                elif command == 'A':  # elliptical arc
                    rx, ry = float(path_segments[i]), float(path_segments[i + 1])
                    x_axis_rotation = float(path_segments[i + 2])
                    large_arc_flag = bool(int(path_segments[i + 3]))
                    sweep_flag = bool(int(path_segments[i + 4]))
                    x2, y2 = float(path_segments[i + 5]), float(path_segments[i + 6])
                    if relative:
                        x2 += current_pos[0]
                        y2 += current_pos[1]
                    path_points.extend(
                        self._elliptical_arc(current_pos, rx)
                    )
                    current_pos = [x2, y2]
                    i += 7

                elif command in {'Z', 'z'}:  # closepath
                    path_points.append(tuple(start_pos))
                    current_pos = start_pos

            # draw the path
            if fill:
                draw.polygon(path_points, fill=fill)
            if stroke:
                draw.line(path_points, fill=stroke, width=stroke_width)

        except Exception as e:
            print(f"Error rendering path: {e}")

    def _cubic_bezier_curve(self, start, control1, control2, end, steps=50):
        """
        Generate points for a cubic Bézier curve
        """
        points = []
        for t in range(steps + 1):
            t /= steps
            x = (1 - t) ** 3 * start[0] + 3 * (1 - t) ** 2 * t * control1[0] + 3 * (1 - t) * t ** 2 * control2[
                0] + t ** 3 * end[0]
            y = (1 - t) ** 3 * start[1] + 3 * (1 - t) ** 2 * t * control1[1] + 3 * (1 - t) * t ** 2 * control2[
                1] + t ** 3 * end[1]
            points.append((x, y))
        return points

    def _elliptical_arc(self, start, end):
        """
        Generate points for an elliptical arc
        """
        # placeholder for actual arc calculation
        points = [start, end]
        return points

    def _quadratic_bezier_curve(self, start, control, end, steps=50):
        """
        Generate points for a quadratic Bézier curve
        """
        points = []
        for t in range(steps + 1):
            t /= steps
            x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0]
            y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1]
            points.append((x, y))
        return points

    def get_image(self):
        """
        Get the image
        """
        return self.image
