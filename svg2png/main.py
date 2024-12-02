import sys
from svg_parser import SVGParser

def main():

    # get the arguments
    args = sys.argv[1:]

    # check if the number of arguments is correct
    if len(args) != 2:
        print("Usage: python main.py svg_file png_file")
        sys.exit(1)

    # check if the file extension is correct
    if not args[0].endswith('.svg'):
        print("The first file should be an SVG file")
        sys.exit(1)

    if not args[1].endswith('.png'):
        print("The second file should be a PNG file")
        sys.exit(1)

    # check if the file exists
    try:
        with open(args[0], 'r') as f:
            pass
    except FileNotFoundError:
        print(f"File {args[0]} not found")
        sys.exit(1)

    svg_parser = SVGParser(args[0])
    svg_parser.parse()
    svg_attributes = svg_parser.get_svg_attributes()


if __name__ == "__main__":
    main()