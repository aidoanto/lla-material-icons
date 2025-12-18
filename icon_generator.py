#!/usr/bin/env python3
"""
Material Icons Generator

This script generates 500x500 PNG icons with different color variations
using Google Material Symbols SVG files.
"""

import os
import io
import cairosvg
from PIL import Image, ImageDraw, ImageColor
from pathlib import Path


class MaterialIconGenerator:
    def __init__(self):
        self.size = (500, 500)
        self.icon_size = 250
        self.circle_radius = 250  # For a circle that fills the 500x500 square
        self.svg_base_path = "material-icons-repo/symbols/web"

        # Color configurations as specified in README
        self.color_configs = {
            "blue-alpha": {
                "icon_color": "#221FBB",
                "bg_color": None,  # transparent
                "output_dir": "icons/blue-alpha",
            },
            "blue-beige": {
                "icon_color": "#221FBB",
                "bg_color": "#F3EBD9",
                "output_dir": "icons/blue-beige",
            },
            "orange-blue": {
                "icon_color": "#221FBB",
                "bg_color": "#FF9E85",
                "output_dir": "icons/orange-blue",
            },
            "blue-yellow": {
                "icon_color": "#221FBB",
                "bg_color": "#FFD075",
                "output_dir": "icons/blue-yellow",
            },
        }

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        if hex_color is None:
            return None
        return ImageColor.getrgb(hex_color)

    def hex_to_rgba(self, hex_color, alpha=255):
        """Convert hex color to RGBA tuple."""
        if hex_color is None:
            return None
        rgb = ImageColor.getrgb(hex_color)
        return rgb + (alpha,)

    def create_circle_background(self, bg_color):
        """Create a 500x500 image with a circle background."""
        # Create image with transparent background
        img = Image.new("RGBA", self.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw circle
        center_x, center_y = self.size[0] // 2, self.size[1] // 2
        draw.ellipse(
            [
                (center_x - self.circle_radius, center_y - self.circle_radius),
                (center_x + self.circle_radius, center_y + self.circle_radius),
            ],
            fill=bg_color,
        )

        return img

    def find_svg_file(self, icon_name):
        """Find the SVG file for a given icon name."""
        # Look for the SVG file in the material-icons-repo
        icon_dir = Path(self.svg_base_path) / icon_name

        if not icon_dir.exists():
            return None

        # Look for the outlined SVG (materialsymbolsoutlined)
        # We'll use the default 48px version without any weight/fill variations
        outlined_dir = icon_dir / "materialsymbolsoutlined"

        if not outlined_dir.exists():
            return None

        # Try different possible SVG filenames (prefer larger sizes for better quality)
        possible_files = [
            outlined_dir / f"{icon_name}_48px.svg",
            outlined_dir / f"{icon_name}_40px.svg",
            outlined_dir / f"{icon_name}_24px.svg",
            outlined_dir / f"{icon_name}_20px.svg",
        ]

        for svg_file in possible_files:
            if svg_file.exists():
                return svg_file

        return None

    def recolor_svg(self, svg_content, new_color):
        """Replace or add the fill color in the SVG with the new color."""
        import re

        # Replace existing fill attributes
        svg_content = svg_content.replace('fill="#000000"', f'fill="{new_color}"')
        svg_content = svg_content.replace('fill="#000"', f'fill="{new_color}"')
        svg_content = svg_content.replace('fill="black"', f'fill="{new_color}"')
        svg_content = svg_content.replace('fill="currentColor"', f'fill="{new_color}"')

        # Also handle style attributes
        svg_content = svg_content.replace(
            'style="fill:#000000"', f'style="fill:{new_color}"'
        )
        svg_content = svg_content.replace(
            'style="fill:#000"', f'style="fill:{new_color}"'
        )

        # Add fill attribute to path elements that don't have one
        # This handles Material Symbols which often don't specify fill
        svg_content = re.sub(
            r'<path\s+([^>]*?)d="', f'<path fill="{new_color}" \\1d="', svg_content
        )

        # Also add to other shape elements
        for element in ["circle", "rect", "polygon", "polyline", "ellipse"]:
            svg_content = re.sub(
                f"<{element}\\s+(?!.*fill=)([^>]*?)>",
                f'<{element} fill="{new_color}" \\1>',
                svg_content,
            )

        return svg_content

    def svg_to_png(self, svg_path, icon_color, output_size):
        """Convert SVG to PNG with specified color and size."""
        try:
            # Read the SVG file
            with open(svg_path, "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Recolor the SVG
            svg_content = self.recolor_svg(svg_content, icon_color)

            # Convert SVG to PNG using cairosvg
            png_data = cairosvg.svg2png(
                bytestring=svg_content.encode("utf-8"),
                output_width=output_size,
                output_height=output_size,
            )

            # Open as PIL Image
            icon_img = Image.open(io.BytesIO(png_data))

            return icon_img

        except Exception as e:
            print(f"Error converting SVG: {e}")
            return None

    def add_icon_to_image(self, base_image, icon_name, icon_color):
        """Add the Material Symbol icon to the image."""
        # Find the SVG file
        svg_path = self.find_svg_file(icon_name)

        if svg_path is None:
            print(f"Warning: Could not find SVG for {icon_name}")
            return base_image

        # Convert SVG to PNG with the desired color
        icon_img = self.svg_to_png(svg_path, icon_color, self.icon_size)

        if icon_img is None:
            return base_image

        # Ensure icon is RGBA
        if icon_img.mode != "RGBA":
            icon_img = icon_img.convert("RGBA")

        # Calculate position to center the icon
        x = (self.size[0] - self.icon_size) // 2
        y = (self.size[1] - self.icon_size) // 2

        # Paste the icon onto the base image
        base_image.paste(icon_img, (x, y), icon_img)

        return base_image

    def generate_icon(self, icon_name, color_config_name):
        """Generate a single icon with the specified color configuration."""
        config = self.color_configs[color_config_name]

        # Create base image with solid rectangular background (no circle)
        bg_color = (
            self.hex_to_rgba(config["bg_color"]) if config["bg_color"] else (0, 0, 0, 0)
        )
        # Create image with solid color background instead of circle
        img = Image.new("RGBA", self.size, bg_color)

        # Add the icon
        icon_color = config["icon_color"]
        img = self.add_icon_to_image(img, icon_name, icon_color)

        # Ensure output directory exists
        os.makedirs(config["output_dir"], exist_ok=True)

        # Save the image
        output_path = os.path.join(
            config["output_dir"], f"{icon_name}-{color_config_name}.png"
        )
        img.save(output_path, "PNG")

        return output_path

    def get_all_icon_names(self):
        """Get all available icon names from the material-icons-repo."""
        svg_base = Path(self.svg_base_path)
        if not svg_base.exists():
            print(f"Error: {self.svg_base_path} does not exist!")
            return []

        # Get all subdirectories (each represents an icon)
        icon_names = [d.name for d in svg_base.iterdir() if d.is_dir()]
        icon_names.sort()

        return icon_names

    def generate_all_icons(self):
        """Generate all icons for all color configurations."""
        # Get icon names from the repo
        icon_names = self.get_all_icon_names()

        if not icon_names:
            print("No icons found!")
            return

        total_icons = len(icon_names)
        print(
            f"Generating {total_icons} icons for {len(self.color_configs)} color schemes..."
        )

        generated_count = 0
        failed_icons = []

        for color_config_name in self.color_configs.keys():
            print(f"\nGenerating {color_config_name} icons...")

            for i, icon_name in enumerate(icon_names, 1):
                try:
                    self.generate_icon(icon_name, color_config_name)
                    generated_count += 1

                    # Progress update every 100 icons
                    if i % 100 == 0:
                        print(
                            f"Progress: {i}/{total_icons} icons for {color_config_name}"
                        )

                except Exception as e:
                    failed_icons.append((icon_name, color_config_name, str(e)))
                    if i % 100 == 0:  # Only print errors periodically to avoid spam
                        print(
                            f"Error generating {icon_name} for {color_config_name}: {e}"
                        )

        print(f"\nCompleted! Generated {generated_count} icons total.")

        if failed_icons:
            print(f"\nFailed to generate {len(failed_icons)} icons.")
            print("First few failures:")
            for icon_name, config, error in failed_icons[:5]:
                print(f"  - {icon_name} ({config}): {error}")


def main():
    generator = MaterialIconGenerator()
    generator.generate_all_icons()


if __name__ == "__main__":
    main()
