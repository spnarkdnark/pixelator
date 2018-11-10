from PIL import Image, ImageDraw
from random import randint
import os


def get_input_image(filename):

    """
    return an image object with input filename
    args : path to input image as filename
    output : image object from PIL library
    """

    return Image.open(filename)  # PIL library function to create an Image object from input filename


def convert_image_data(image):

    """
    Convert the image to a 2D array of RGB tuples containing color values
    :param image: PIL image object
    :return: 2D Array of RGB tuples
    """

    pixels = list(image.getdata())  # store list of values as tuples
    return [pixels[i:i + image.width] for i in range(0, len(pixels), image.width)]  # return new 2D array of RGB tuples


def get_square(corner, size, matrix):

    """
    Get a slice of a given 2D array based on square parameters
    :param corner: top left (x,y) corner of square
    :param size: size for each edge of square
    :param matrix: input matrix (2D array of pixel tuples) to be sliced and stored in new square
    :return: a square slice from input matrix
    """

    opposite_corner = (corner[0] + size, corner[1] + size)  # store opposite_corner as (x+size,y+size)
    square_row = matrix[corner[1]:opposite_corner[1]]  # store matrix y(n) slice as square_row
    square = []  # init empty square
    for item in square_row:  # loop through n sized row
        square.append(item[corner[0]:opposite_corner[0]])  # append x(n) slice to square

    return square


def get_pixel_avg(square):

    """
    Get the pixel average in the size of a given square
    :param square: array of sliced values from input image matrix built with get_square
    :return: average RGB value tuple from given square(pixel size)
    """

    red = 0  # set RGB values to 0, will be averaged out at end of function
    blue = 0
    green = 0
    pixel_square = len(square) * len(square)  # set pixel_square size for use in averaging out

    for height in range(0, len(square)):  # loop through rows using square size
        for width in range(0, len(square[0])):  # loop through columns using square size
            red += square[height][width][0]  # increment R,G,B values using tuples in square
            green += square[height][width][1]
            blue += square[height][width][2]

    # return tuple of RGB value averages as integers
    return (int(red / pixel_square), int(green / pixel_square), int(blue / pixel_square))


def draw_circle(im, x, y, pixel_size, color):

    """
    Draw a circle on the given draw_object
    :param im: input draw object
    :param x: x value for top left corner
    :param y: y value for top left corner
    :param pixel_size: diameter of circle to be drawn from (x,y) point
    :param color: fill color of circle
    :return: an ImageDraw circle
    """

    return im.ellipse([x, y, x + pixel_size, y + pixel_size], color)


def draw_rectangle(im, x, y, pixel_size, color, modifier = False, mod_type = False):

    """
    Draw a rectangle on the given draw_object
    :param im: input draw object
    :param x: x value for top left corner
    :param y: y value for top left corner
    :param pixel_size: size of square edge to be drawn from (x,y) point
    :param color: fill color of square
    :return: an ImageDraw square
    """

    if modifier:
        if mod_type == 'random':
            rand_mod = randint(1,modifier)
            return im.rectangle((x+rand_mod, y+rand_mod, x+pixel_size-rand_mod, y+pixel_size-rand_mod), color,(color[0]-20,color[1]-20,color[2]-20))
        elif mod_type == 'gridx':
            return im.rectangle((x+modifier, y, x+pixel_size-modifier, y+pixel_size), color,(color[0]-20,color[1]-20,color[2]-20))
        elif mod_type == 'gridy':
            return im.rectangle((x, y+modifier, x+pixel_size, y+pixel_size-modifier), color,(color[0]-20,color[1]-20,color[2]-20))

    else:
        return im.rectangle([x, y, x + pixel_size, y+pixel_size], color,(color[0]-20,color[1]-20,color[2]-20))


def render(file, pixel_size, modifier = False, mod_type = False):

    """
    Draw a new image object, pixelated based on pixel_size
    :param file: Input image object to be looped through, color averaged and pixelated
    :param pixel_size: How big each pixel within output photo should be
    :return: an output object ready to be shown, saved, etc.
    """

    image = get_input_image(file)  # Set image to PIL image object using get_input_image()
    width = image.width  # Set image.width and height to be used in loops
    height = image.height
    image_array = convert_image_data(image)  # Set image_array for use in get_square and get_pixel_avg
    blank_image = Image.new('RGB', image.size, (255, 255, 255))  # Create new blank image to be drawn on
    draw_object = ImageDraw.Draw(blank_image)  # Create Draw object from new blank image for Draw functions

    for x in range(0, width, pixel_size):  # loop through (x,y) values in width/height of image object
        for y in range(0, height, pixel_size):  # -pixel_size to ensure boundary isn't violated
            sq = get_square((x, y), pixel_size, image_array)  # get square slice from input image object
            color = get_pixel_avg(sq)  # calculate avg color of square at given point in image object
            draw_rectangle(draw_object, x, y, pixel_size,color, modifier,mod_type)  # draw a shape at that point in the blank_image

    return blank_image  # Return completed pixel object


def pixelate_multiple(file_path, size):

    """
    Pixelate a full directory of images
    :param file_path: Directory name
    :param size: Pixel size
    :return: A dictionary of path : object relationships
    """

    empty = {}  # Init an empty dictionary for file path/object storage

    for filename in os.listdir(file_path):  # Loop through each file in file path dir
        if filename.endswith('.jpg'):  # Make sure each file is same format (jpg for now)
            full_path = os.path.join(file_path, filename)  # Generate full path from Dir name + file name
            image = render(full_path, size)  # Return a pixelated object
            empty[filename] = image  # Store the pixelatd object in the empty dictionary

        else:
            print("Invalid File Format!")  # If not jpg, print invalid message

    return empty  # Return image dictionary


def save_to_directory(images, file_path):

    """
    Writes images in dictionary generated from load_and_crop into new folder
    :param images: Images dictionary
    :return: A directory filled with cropped images
    """

    for filename, image in images.items():
        full_path = os.path.join(file_path, filename)
        image.save(full_path)

