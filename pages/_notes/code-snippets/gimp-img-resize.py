from gimpfu import *

def resize_and_center(image_path):
    # Constants for the desired image and canvas sizes
    TARGET_WIDTH = 2.5  # inches
    TARGET_HEIGHT = 3.5  # inches
    CANVAS_WIDTH = 4    # inches
    CANVAS_HEIGHT = 4   # inches
    DPI = 300  # Change this according to your image's DPI
    # Load the image
    image = pdb.gimp_file_load(image_path, image_path)
    if not image:
        print("Failed to load image.")
        return
    drawable = pdb.gimp_image_get_active_layer(image)
    if not drawable:
        print("No drawable layer available.")
        return
    # Calculate new dimensions to maintain aspect ratio
    width = drawable.width
    height = drawable.height
    aspect_ratio = float(width) / height
    new_width, new_height = 0, 0
    if aspect_ratio > (TARGET_WIDTH / TARGET_HEIGHT):
        new_height = TARGET_HEIGHT * DPI
        new_width = new_height * aspect_ratio
    else:
        new_width = TARGET_WIDTH * DPI
        new_height = new_width / aspect_ratio
    # Resize the image
    pdb.gimp_image_scale(image, int(new_width), int(new_height))
    # Flatten the image and update the drawable reference
    flattened = pdb.gimp_image_flatten(image)
    # Resize the canvas and center the image
    pdb.gimp_image_resize(image, CANVAS_WIDTH * DPI, CANVAS_HEIGHT * DPI,
                          (CANVAS_WIDTH * DPI - new_width) / 2, (CANVAS_HEIGHT * DPI - new_height) / 2)
    # Get the new drawable after the image has been resized
    drawable = pdb.gimp_image_get_active_layer(image)
    if not drawable:
        print("Failed to get drawable after resizing.")
        return
    # Save the image to a new file path
    new_path = image_path.replace(".jpg", "_modified.jpg")
    try:
        pdb.gimp_file_save(image, drawable, new_path, new_path)
        print("Image saved to %s" % new_path)
    except Exception as e:
        print("Failed to save image: %s" % str(e))
    # Clean up
    pdb.gimp_image_delete(image)
# Example usage (replace '/path/to/your/image.jpg' with the path to your image)
# resize_and_center('/path/to/your/image.jpg')