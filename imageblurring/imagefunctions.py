#!/usr/bin/env python3
import cv2
import numpy as np
from numba import jit
import os
import sys


# Ex4.6
def blur_image(input, output_filename=None):
    """The function takes in two arguments, reads a picture from file,
    blurs the image based on the vectorized blur algorithm, and writes
    the image to a file if output file is specified.

    The format for a parameter is:
    inimg (String):
        Filename, and filepath for the picture that is to be read.
    outimg (String):
        Filename, and filepath for the picture that is to be saved
        to a file.
    Raises:
        FileNotFoundError if file is not found
    """
    if(input is None):
        raise FileNotFoundError("Filename is not specified")
    image = readImageFromFile(input) if isinstance(input, str) else input
    image = vectorizedBlur(image)
    if(output_filename is not None):
        writeImageToFile(image, output_filename)
    image = image.astype("uint8")
    return image


def readImageFromFile(filename="beatles.jpg"):
    """Function for reading a image from a file

    The format for a parameter is:
    filename (String): full path and filename
        Used for reading the file using cv2.
    Returns:
        Numpy ndarray of 3 dimensions from the cv2.imread function
    Raises:
        FileNotFoundError if file is not found
    """
    if((filename is None) or len(filename) < 3):
        raise FileNotFoundError("Could open or read file ead image"
                                ", or file is not spesified.")
    sourceImage = cv2.imread(filename)
    return sourceImage


def padImage(image):
    """Function for padding an Numpy image array so that to
    prevent array index out of bounds while the blur algoritm
    is applied to the image. Adds an extra columns, and rows
    arround the input image.

    The format for a parameter is:
    image (ndarray):
        A image represented in a ndarray with 3-dimensions ndarray.
    Returns:
        A ndarray of the input image containing the padding.
    """
    pad = ((1, 1), (1, 1), (0, 0))
    paddedSourceImage = np.pad(image, pad_width=pad, mode='edge')
    paddedSourceImage = paddedSourceImage.astype("uint32")
    return paddedSourceImage


def unPadImage(image):
    """Function for removing the padding performed by the
    function padImage().

    The format for a parameter is:
    image (ndarray):
        A image represented in a ndarray with 3-dimensions ndarray.
        containing a pad.
    Returns:
        A ndarray of the input image without padding.
    """
    return image[1:-1, 1:-1, :]


def writeImageToFile(image, filename=None):
    """Function for writing a image file to the harddrive

    The format for a parameter is:
    image (ndarray):
        A image represented in a ndarray with 3-dimensions ndarray.
    filename (String):
        The filename with file extention to name the file saved
        to harddrive. Filepath can also be included in the string.
    Returns:
        A ndarray representing the saved image file.
    """
    isWindows = sys.platform.startswith('win')
    if(isWindows):
        if(filename is None):
            filename = "blurred_images\\blurred_image.jpg"
        filepath = filename.split("\\")
    else:
        if(filename is None):
            filename = "blurred_images/blurred_image.jpg"
        filepath = filename.split("/")
    dst = image.astype("uint8")
    if(len(filepath) > 1):  # filename contains a path if true
        filepath = filepath[:-1]
        newDirectory = ""
        for i in filepath:
            newDirectory += i+"\\" if isWindows else i+"/"
        if not os.path.exists(newDirectory):
            os.makedirs(newDirectory)
    print("Image saved to destination:", filename)
    cv2.imwrite(filename, dst)
    return dst


def unvectorizedBlur(image):
    """Algorithm that blurs the input image and returns a new blurred image.
    The algorithm loops through all pixels, using y,x coordinates, in the
    image and calculate the mean from all the neighbours color channel.
    The color channel represent the BGR colors for each pixel.

    The format for a parameter is:
    image (ndarray):
        A image represented in a ndarray. 3-dimensional ndarray.
    Returns:
        A new ndarray representing the blurred image.
    """
    image = image.astype("uint32")
    blur = np.empty((image.shape[0], image.shape[1], image.shape[2]))
    image = padImage(image)
    for h in range(1, image.shape[0] - 1):
        for w in range(1, image.shape[1] - 1):
            for c in range(image.shape[2]):
                blur[h-1, w-1, c] = (image[h, w, c] + image[h - 1, w, c] +
                                     image[h + 1, w, c] + image[h, w - 1, c] +
                                     image[h, w + 1, c] + image[h - 1, w - 1, c] +
                                     image[h - 1, w + 1, c] + image[h + 1, w - 1, c] +
                                     image[h + 1, w + 1, c]) / 9
    return blur


def vectorizedBlur(image):
    """Algorithm that blurs the input image and returns a new blurred image.
    The algorithm uses a vectorized arithmetical operation for calculating
    the mean of all the neighbours color channel.
    The color channel represent the BGR colors for each pixel.

    The format for a parameter is:
    image (ndarray):
        A image represented in a ndarray. 3-dimensional ndarray.
    Returns:
        A new ndarray representing the blurred image.
    """
    image = image.astype("uint32")
    image = padImage(image)
    blur = (image[:-2, :-2, :] + image[1:-1, :-2, :] + image[2:, :-2, :] +
            image[:-2, 1:-1, :] + image[1:-1, 1:-1, :] + image[2:, 1:-1, :] +
            image[:-2, 2:, :] + image[1:-1, 2:, :] + image[2:, 2:, :]) / 9
    return blur


@jit(nopython=True)
def unvectorizedBlurNumba(image):
    """Numba decorated function which contains an algorithm that blurs the
    input image and returns a new blurred image. The algorithm loops through
    all pixels, using y,x coordinates, in the image and calculate the
    mean from all the neighbours color channel.
    The color channel represent the BGR colors for each pixel.

    The format for a parameter is:
    image (ndarray):
        A image represented in a ndarray. 3-dimensional ndarray.
    Returns:
        A new ndarray representing the blurred image.
    """
    blur = np.empty((image.shape[0] - 2, image.shape[1] - 2, image.shape[2]))
    for h in range(1, len(image)-1):
        for w in range(1, len(image[0])-1):
            for c in range(len(image[0][0])):
                blur[h-1, w-1, c] = (image[h, w, c] + image[h - 1, w, c] +
                                     image[h + 1, w, c] + image[h, w - 1, c] +
                                     image[h, w + 1, c] + image[h - 1, w - 1, c] +
                                     image[h - 1, w + 1, c] + image[h + 1, w - 1, c] +
                                     image[h + 1, w + 1, c]) / 9
    return blur


@jit(nopython=True)
def vectorizedBlurNumba(image):
    """Numba decorated function which contains an algorithm that blurs the
    input image and returns a new blurred image. The algorithm uses a
    vectorized arithmetical operation for calculating the mean of
    all the neighbours color channel. The color channel represent
    the BGR colors for each pixel.

    The format for a parameter is:
    image (ndarray):
        A image represented in a ndarray. 3-dimensional ndarray.
    Returns:
        A new ndarray representing the blurred image.
    """
    blurred = (image[:-2, :-2, :] + image[1:-1, :-2, :] + image[2:, :-2, :] +
               image[:-2, 1:-1, :] + image[1:-1, 1:-1, :] + image[2:, 1:-1, :] +
               image[:-2, 2:, :] + image[1:-1, 2:, :] + image[2:, 2:, :]) / 9
    return blurred


def unvectorizedFaceBlur(image, xStart, xStop, yStart, yStop):
    """Algorithm that blurs the input image and returns a new blurred image.
    The algorithm uses a none vectorized blur algorithm that loops through
    all pixels, using y,x coordinates, in the image and calculate the mean
    from all the neighbours color channel, and functions exactly like
    the unvectorizedBlur algorithm exept that this algorithm blurs only the
    area (pixels) where a face is detected. The color channel represent the
    BGR colors for each pixel.

    The format for a parameter is:
    image (ndarray):
        A image represented in a ndarray. 3-dimensional ndarray.
    xStart (int):
        The starting x coordinate to blur from
    xStop (int):
        The x coordinate to blur to
    yStart (int):
        The starting y coordinate to blur from
    yStop (int):
        The y coordinate to blur to
    Returns:
        A new ndarray representing the blurred image.
    """
    image = image.astype("uint32")
    faceblur = np.copy(image)
    for h in range(yStart, yStop - 1):
        for w in range(xStart, xStop - 1):
            for c in range(image.shape[2]):
                faceblur[h, w, c] = (image[h, w, c] + image[h - 1, w, c] +
                                     image[h + 1, w, c] + image[h, w - 1, c] +
                                     image[h, w + 1, c] + image[h - 1, w - 1, c] +
                                     image[h - 1, w + 1, c] + image[h + 1, w - 1, c] +
                                     image[h + 1, w + 1, c]) / 9
    return faceblur


def vectorizedFaceBlur(image, xStart, xStop, yStart, yStop):
    """Algorithm that blurs the input image and returns a new blurred image.
    The algorithm uses a vectorized arithmetical operation for calculating
    the mean of all the neighbours color channel, and functions exactly like
    the vectorizedBlur algorithm exept that this algorithm blurs only the
    area (pixels) where a face is detected.
    The color channel represent the BGR colors for each pixel.

    The format for a parameter is:
    image (ndarray):
        A image represented in a ndarray. 3-dimensional ndarray.
    xStart (int):
        The starting x coordinate to blur from
    xStop (int):
        The x coordinate to blur to
    yStart (int):
        The starting y coordinate to blur from
    yStop (int):
        The y coordinate to blur to
    Returns:
        A new ndarray representing the blurred image.
    """
    image = image.astype("uint32")
    faceblur = np.copy(image)
    faceblur[1+yStart:2+yStop, 1+xStart:2+xStop, :] = \
        (image[yStart:1+yStop, xStart:1+xStop, :] + image[1+yStart:2+yStop, xStart:1+xStop, :] +
         image[2+yStart:3+yStop, xStart:1+xStop, :] + image[yStart:1+yStop, 1+xStart:2+xStop, :] +
         image[1+yStart:2+yStop, 1+xStart:2+xStop, :] + image[2+yStart:3+yStop, 1+xStart:2+xStop, :] +
         image[yStart:1+yStop, 2+xStart:3+xStop, :] + image[1+yStart:2+yStop, 2+xStart:3+xStop, :] +
         image[2+yStart:3+yStop, 2+xStart:3+xStop, :]) / 9
    return faceblur


def compareTwoImages(image1, image2):
    """A function that compares two images of type ndarray.

    The format for a parameter is:
    image1 (ndarray):
        A image represented in a ndarray. 3-dimensional ndarray.
    image2 (ndarray):
        A image represented in a ndarray. 3-dimensional ndarray.
    Returns:
        True if the two arrays are equal. Returns False if not.
    """
    if(type(image1) != np.ndarray):
        image1 = np.asarray(image1)
    if (type(image2) != np.ndarray):
        image2 = np.asarray(image2)
    return np.array_equal(image1, image2)


def compareTwoImagesFromFile(filenameImage1, filenameImage2):
    """A function that compares two images read from files.

    The format for a parameter is:
    filenameImage1 (String):
        A string representing the filename and path for a picture.
    filenameImage2 (String):
        A string representing the filename and path for a picture
    Returns:
        True if the two pictures are equal. Returns False if not.
    """
    image1 = cv2.imread(filenameImage1)
    image2 = cv2.imread(filenameImage2)
    return np.array_equal(image1, image2)
