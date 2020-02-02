#!/usr/bin/env python3
import random
import numpy as np
import sys
sys.path.append('../')  # Necessary to find the imageblurring package
import cv2
from imageblurring.imagefunctions import vectorizedBlur, \
    blur_image, padImage


def test_maxvalue_before_and_after_blur():
    """This funciton generate a 3-dimensional numpy array with pixel
    values randomly chosen between 0 and 255. The generated
    array/image is blurred, and the assert is testing that the maximum
    value of the array has decreased after blurring.
    """
    # Arrange
    src = np.empty((240, 320, 3))
    random.seed(30)
    for h in range(src.shape[0]):
        for w in range(src.shape[1]):
            for c in range(src.shape[2]):
                src[h, w, c] = random.randint(0, 255)
    src_blurred = vectorizedBlur(src)

    # act
    srcMaxLessThenBlurredMax = src_blurred.max() < src.max()

    # assert
    assert srcMaxLessThenBlurredMax


def test_avrageSrcPixelXY_equals_dstPixelXY():
    """This funciton generate a 3-dimensional numpy array with pixel
    values randomly chosen between 0 and 255. The image is blurred and
    Y (yOffset), X (xOffset) coordinate representing a pixel is choosen.
    The assert is testing that the pixel in the blurred image is the
    average of its neighbors in the clear image.
    """
    # Arrange
    # Generating new src with random channel RBG values
    random.seed(30)
    src = np.empty((240, 320, 3))
    for h in range(src.shape[0]):
        for w in range(src.shape[1]):
            for c in range(src.shape[2]):
                src[h, w, c] = random.randint(0, 255)
    # blurring of src
    src_blurred = vectorizedBlur(src)
    # Choosing which pixel to check equality for
    yOffset = int((src.shape[0] - 2) / 2)
    xOffset = int((src.shape[1] - 2) / 2)
    # Collecting the pixel channel containing RGB values
    xyValueBlurredImg = src_blurred[yOffset][xOffset]
    src = padImage(src)
    xyAvrageSrcImg = (src[yOffset:1+yOffset, xOffset:1+xOffset, :] + src[1+yOffset:2+yOffset, xOffset:1+xOffset, :] +
                      src[2+yOffset:3+yOffset, xOffset:1+xOffset, :] + src[yOffset:1+yOffset, 1+xOffset:2+xOffset, :] +
                      src[1+yOffset:2+yOffset, 1+xOffset:2+xOffset, :] + src[2+yOffset:3+yOffset, 1+xOffset:2+xOffset, :] +
                      src[yOffset:1+yOffset, 2+xOffset:3+xOffset, :] + src[1+yOffset:2+yOffset, 2+xOffset:3+xOffset, :] +
                      src[2+yOffset:3+yOffset, 2+xOffset:3+xOffset, :]) / 9
    xyAvrageSrcImg = xyAvrageSrcImg[0][0]  # removing 2 dimensions from the array

    # act
    sourceEqualsDestination = np.array_equal(xyAvrageSrcImg, xyValueBlurredImg)

    # assert
    assert sourceEqualsDestination


def test_blur_image_function_in_package():
    """This function is testing that the blur_image in imagefunctions is able
    to read image from file, blur the image, and write the image back to a file.
    """
    # Arrange
    outputFile = "test_blur_image_package.jpg"
    blur_image("test_beatles.jpg", outputFile)
    imageReadBackFromFile = cv2.imread(outputFile)

    # act
    blurredImageFileIsCreated = True if imageReadBackFromFile is not None else False

    # assert
    assert blurredImageFileIsCreated
