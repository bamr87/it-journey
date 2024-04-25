from gimpfu import *

def plugin_main(image, drawable, input_path):
    # Assumes image is already open in GIMP
    TARGET_WIDTH = 2.5  # inches
    TARGET_HEIGHT = 3.5  # inches
    CANVAS_WIDTH = 4    # inches
    CANVAS_HEIGHT = 4   # inches
    DPI = 300  # Typically, you should use the image resolution here

    # Load the image from the path provided
    image = pdb.gimp_file_load(input_path, input_path)
    drawable = pdb.gimp_image_get_active_layer(image)

    # Resize the image keeping aspect ratio
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

    pdb.gimp_image_scale(image, int(new_width), int(new_height))
    pdb.gimp_image_flatten(image)
    pdb.gimp_image_resize(image, CANVAS_WIDTH * DPI, CANVAS_HEIGHT * DPI,
                          (CANVAS_WIDTH * DPI - new_width) / 2, (CANVAS_HEIGHT * DPI - new_height) / 2)

    # Save the modified image
    new_path = input_path.replace(".jpg", "_modified.jpg")
    pdb.gimp_file_save(image, drawable, new_path, new_path)
    pdb.gimp_image_delete(image)

register(
    "python_fu_resize_center",
    "Resize and Center Image",
    "Resize image to 2.5x3.5 inches and center on a 4x4 inch canvas",
    "Your Name",
    "Your Name",
    "2024",
    "<Image>/Image/Resize and Center...",
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_FILE, "input_path", "Image file", "")
    ],
    [],
    plugin_main
)

main()
