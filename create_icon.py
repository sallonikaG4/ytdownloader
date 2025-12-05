"""
Script to create a simple icon for the application
This creates a basic icon - you can replace it with a better one later
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Create a 256x256 icon
    size = 256
    img = Image.new('RGB', (size, size), color='#6366f1')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple play button and download arrow
    # Play triangle
    triangle_points = [
        (size * 0.3, size * 0.25),
        (size * 0.3, size * 0.75),
        (size * 0.7, size * 0.5)
    ]
    draw.polygon(triangle_points, fill='white')
    
    # Download arrow
    arrow_y = size * 0.85
    draw.line([(size * 0.5, arrow_y), (size * 0.5, size * 0.95)], fill='white', width=8)
    draw.line([(size * 0.45, size * 0.9), (size * 0.5, size * 0.95)], fill='white', width=8)
    draw.line([(size * 0.55, size * 0.9), (size * 0.5, size * 0.95)], fill='white', width=8)
    
    # Save as ICO
    img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("Icon created: icon.ico")
except ImportError:
    print("Pillow not installed. Creating placeholder...")
    # Create a simple text file as placeholder
    with open('icon.ico', 'wb') as f:
        f.write(b'')  # Empty placeholder
    print("Placeholder icon created. Please replace icon.ico with a proper icon file.")


