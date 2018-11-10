from PIL import Image
import os


def get_input_image(filename):

    """
    return an image object with input filename
    args : path to input image as filename
    output : image object from PIL library
    """

    return Image.open(filename)  # PIL library function to create an Image object from input filename


def crop_image(image, square):

    """
    Crop an input image to boundaries of given square, centered within input image
    :param image: input image object
    :param square: length of side of crop
    :return: image object cropped and centered to input image
    """

    height = image.height
    width = image.width
    x_difference = int((image.width - square) / 2)
    y_difference = int((image.height - square) / 2)

    return image.crop((0+x_difference, 0+y_difference, width-x_difference, height-y_difference))


def load_and_crop_images(file_path, size):

    """
    Load in a directory of file paths and apply crop_image to each
    :param file_path: Directory containing all images to be cropped
    :param size: Crop size for each image
    :return: A dictionary of cropped image objects
    """

    empty = {}
    for filename in os.listdir(file_path):
        if filename.endswith(".jpg"):
            full_path = os.path.join(file_path,filename)
            img = get_input_image(full_path)
            empty[filename] = crop_image(img, size)
        else:
            print(filename + "is in an incorrect format")
    return empty


def save_to_directory(images, file_path):
    """
    Writes images in dictionary generated from load_and_crop into new folder
    :param images: Images dictionary
    :return: A directory filled with cropped images
    """

    for filename, image in images.items():
        full_path = os.path.join(file_path, filename)
        image.save(full_path)

