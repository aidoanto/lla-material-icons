#!/usr/bin/env python3
"""
Material Icons Generator - Main Entry Point

This project generates a complete library of Google Material Icons in three color variations:
- blue-alpha: Blue icons (#221FBB) on transparent background
- blue-beige: Blue icons (#221FBB) on beige background (#F3EBD9)
- orange-blue: Blue icons (#221FBB) on orange background (#FF9E85)
- blue-yellow: Blue icons (#221FBB) on yellow background (#FFD075)

Each icon is a 500x500 PNG with a circle background and centered text label.
"""

import os
from icon_generator import MaterialIconGenerator


def main():
    print("🤖 Material Icons Generator")
    print("=" * 50)

    # Check if icons already exist
    icons_dir = "icons"
    if os.path.exists(icons_dir):
        total_icons = sum(len(files) for _, _, files in os.walk(icons_dir) if files)
        print(f"✅ Found {total_icons} generated icons in {icons_dir}/")

        # Show breakdown by color scheme
        for color_dir in ["blue-alpha", "blue-beige", "orange-blue", "blue-yellow"]:
            color_path = os.path.join(icons_dir, color_dir)
            if os.path.exists(color_path):
                count = len([f for f in os.listdir(color_path) if f.endswith(".png")])
                print(f"  • {color_dir}: {count} icons")
    else:
        print("❌ No icons directory found. Run the generator first.")
        print("💡 Use: uv run python icon_generator.py")

    print("\n🎨 Color Schemes:")
    print("  • blue-alpha: Blue (#221FBB) icons on transparent background")
    print("  • blue-beige: Blue (#221FBB) icons on beige (#F3EBD9) background")
    print("  • orange-blue: Blue (#221FBB) icons on orange (#FF9E85) background")
    print("  • blue-yellow: Blue (#221FBB) icons on yellow (#FFD075) background")

    print("\n📊 Each icon is:")
    print("  • 500×500 pixels")
    print("  • Circle background (250px radius)")
    print("  • Centered Material Symbol icon (250px)")
    print("  • Named as: {icon_name}-{color_scheme}.png")

    print("\n🚀 Ready to use! Icons are located in the icons/ directory.")


if __name__ == "__main__":
    main()
