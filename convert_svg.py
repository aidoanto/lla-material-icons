# this script is unrelated to icon_generator.py

# !/usr/bin/env python3
import cairosvg
from PIL import Image
import sys


def convert_svg_to_centered_png(svg_file, png_file, icon_width=350, container_size=500):
    """Convert SVG to PNG centered in a square container"""
    try:
        # Calculate proportional height for the icon
        # Original aspect ratio from SVG viewBox (53:47)
        aspect_ratio = 47 / 53
        icon_height = int(icon_width * aspect_ratio)

        # Step 1: Convert SVG to temporary icon
        temp_icon = "/tmp/temp_icon.png"
        cairosvg.svg2png(
            url=svg_file,
            write_to=temp_icon,
            output_width=icon_width,
            output_height=icon_height,
            background_color="transparent",
        )

        # Step 2: Create a square canvas with transparent background
        canvas = Image.new("RGBA", (container_size, container_size), (0, 0, 0, 0))

        # Step 3: Load the icon and center it on the canvas
        icon = Image.open(temp_icon)

        # Calculate position to center the icon
        x_offset = (container_size - icon_width) // 2
        y_offset = (container_size - icon_height) // 2

        # Paste the icon onto the canvas (centered)
        canvas.paste(icon, (x_offset, y_offset), icon)

        # Step 4: Save the final result
        canvas.save(png_file, "PNG")
        print(
            f"Successfully created {png_file} ({container_size}x{container_size} with {icon_width}px centered icon)"
        )
        return True
    except Exception as e:
        print(f"Error converting SVG to PNG: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 convert_svg.py <input.svg> <output.png>")
        sys.exit(1)

    input_svg = sys.argv[1]
    output_png = sys.argv[2]

    success = convert_svg_to_centered_png(input_svg, output_png)
    sys.exit(0 if success else 1)
