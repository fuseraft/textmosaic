import argparse
from PIL import Image, ImageDraw, ImageFont

def get_text_dimensions(text_string, font):
    """
    Using font metrics to get text size.
    """
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = ascent + descent
    return (text_width, text_height)

def create_text_image(args):
    """
    Create a text image from the provided arguments.
    """
    # Open the input image
    original_image = Image.open(args.input_path).convert("RGBA")
    width, height = original_image.size

    # Create a new image with black background
    text_image = Image.new("RGBA", (width, height), "black")

    # Create a mask for the text
    mask = Image.new("L", (width, height), 0)

    # Set up the font and draw context
    font = ImageFont.truetype(args.font_path, args.font_size)
    draw = ImageDraw.Draw(text_image)
    mask_draw = ImageDraw.Draw(mask)

    # Calculate text size and position
    text_width, text_height = get_text_dimensions(args.text, font)
    
    # Draw the text into the image multiple times to fill the image
    for y in range(0, height, text_height + 10):
        for x in range(0, width, text_width + 10):
            draw.text((x, y), args.text, font=font, fill="white")
            mask_draw.text((x, y), args.text, font=font, fill=255)  # Draw white text on the mask

    # Blend the original image with the text image using the mask
    result_image = Image.composite(original_image, text_image, mask)

    # Save or show the result
    if args.output:
        result_image.save(args.output)
        print(f"Output saved to {args.output}")
    else:
        result_image.show()

def main():
    parser = argparse.ArgumentParser(description="Create a text mosaic image.")
    parser.add_argument("input_path", help="Path to the input image")
    parser.add_argument("text", help="Text to overlay on the image")
    parser.add_argument("font_path", help="Path to the font file")
    parser.add_argument("font_size", type=int, help="Font size for the text overlay")
    parser.add_argument("--output", help="Path to save the output image (optional)", default=None)

    args = parser.parse_args()
    create_text_image(args)

if __name__ == "__main__":
    main()
