import argparse
import os
from PIL import Image, ImageDraw, ImageFont

def validate_file(path):
    """
    Check if a file exists at the given path.
    """
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"The file {path} does not exist.")
    return path

def positive_int(value):
    """
    Check if the value is a positive integer.
    """
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer.")
    return ivalue

def get_text_dimensions(text_string, font):
    """
    Using font metrics to get text size.
    """
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = ascent + descent
    return (text_width, text_height)

def create_text_mosaic(args):
    """
    Create a text mosaic image.
    """
    try:
        # Open the input image
        original_image = Image.open(args.input_path).convert("RGBA")
    except IOError:
        print(f"Error: Cannot open the image file at {args.input_path}.")
        return

    width, height = original_image.size
    try:
        # Create a new image with black background
        text_image = Image.new("RGBA", (width, height), "black")

        # Create a mask for the text
        mask = Image.new("L", (width, height), 0)

        # Set up the font and draw context
        font = ImageFont.truetype(args.font_path, args.font_size)
    except Exception as e:
        print(f"Error: {str(e)}")
        return

    draw = ImageDraw.Draw(text_image)
    mask_draw = ImageDraw.Draw(mask)
    text_width, text_height = get_text_dimensions(args.text, font)
    
    # Draw the text into the image multiple times to fill the image
    for y in range(0, height, text_height + 10):
        for x in range(0, width, text_width + 10):
            draw.text((x, y), args.text, font=font, fill="white")
            mask_draw.text((x, y), args.text, font=font, fill=255)  # Draw white text on the mask

    try:
        # Blend the original image with the text image using the mask
        result_image = Image.composite(original_image, text_image, mask)

        # Save or show the result
        if args.output:
            result_image.save(args.output)
            print(f"Output saved to {args.output}")
        else:
            result_image.show()
    except Exception as e:
        print(f"Error during image processing or saving: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Create a text mosaic image.")
    parser.add_argument("input_path", type=validate_file, help="Path to the input image")
    parser.add_argument("text", help="Text to overlay on the image")
    parser.add_argument("font_path", type=validate_file, help="Path to the font file")
    parser.add_argument("font_size", type=positive_int, help="Font size for the text overlay")
    parser.add_argument("--output", type=str, help="Path to save the output image (optional)", default=None)

    args = parser.parse_args()
    create_text_mosaic(args)

if __name__ == "__main__":
    main()
