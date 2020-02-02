#!/usr/bin/env python3
from imageblurring.imagemodule.imagefunctions import compareTwoImages, compareTwoImagesFromFile, readImageFromFile
from imageblurring.imagemodule.imagefunctions import vectorizedBlur, unvectorizedBlur, blur_image, padImage, unPadImage
import random
import numpy as np
import cv2
import sys
sys.path.append('../')

def test_fromFile_imageX_equals_ImageY_1(imagefile1="blurred_images\\unvectorized_blur_standardPython2.jpg",
                                        imagefile2="blurred_images\\unvectorized_blur_standardPython2.jpg"):
    assert compareTwoImagesFromFile(imagefile1,imagefile2) == True

def test_fromFile_imageX_equals_ImageY_2(imagefile1="blurred_images\\unvectorized_blur_standardPython.jpg",
                                        imagefile2="blurred_images\\unvectorized_blur_standardPython3.jpg"):
    assert compareTwoImagesFromFile(imagefile1,imagefile2) == False

def test_fromArray_imageX_equals_fromFile_ImageY(imageArray,imageFile):
    #imageFromFile = readImageFromFile(imageFile)
    #imageFromFile = imageFromFile[1:-1, 1:-1, :]  # removing pad from imageFromFile added in readImageFromFeil function.
    imageFromFile = cv2.imread(imageFile)
    imageArray = imageArray.astype("uint8")
    imageFromFile = imageFromFile.astype("uint8")
    print(np.array_equal(imageArray, imageFromFile))
    assert compareTwoImages(imageArray,imageFromFile) == True

def test_blur_image_function_in_package():
    srcImageFile = "beatles.jpg"
    blurredImageFile = "blurred_images\\blur_image_package.jpg"
    image = blur_image(srcImageFile,blurredImageFile)
    a = len(image)
    b = len(readImageFromFile(srcImageFile))
    assert (a > 0) == True
    assert (b > 0) == True


def test_maxvalue_before_and_after_blur():
    src = np.empty((240, 320, 3))
    #blurred = np.empty((src.shape[0], src.shape[1], src.shape[2]))
    random.seed(30)
    for h in range(src.shape[0]):
        for w in range(src.shape[1]):
            for c in range(src.shape[2]):
                src[h, w, c] = random.randint(0,255)

    src_blurred = np.copy(src)
    #assert src_blurred.max() == src.max() ikke nødvendig

    pad = ((1, 1), (1, 1), (0, 0))
    src = np.pad(src, pad_width=pad, mode='edge') #adding pad to src
    src = src.astype("uint32")
    src_blurred = vectorizedBlur(src)
    src = unPadImage(src) #removing pad from src
    assert src_blurred.max() < src.max() #lagre unna src max etc

def test_fromFile_avrageSrcPixelXY_equals_dstPixelXY():
    #Generating new src with random channel RBG values
    random.seed(30)
    src = np.empty((240, 320, 3))
    for h in range(src.shape[0]):
        for w in range(src.shape[1]):
            for c in range(src.shape[2]):
                src[h, w, c] = random.randint(0, 255)

    #blurring of src
    src_blurred = np.empty((src.shape[0], src.shape[1], src.shape[2]))  #
    src_blurred = vectorizedBlur(src)
    #Choosing pixel to check equality for
    yOffset = int((src.shape[0] - 2) / 2)
    xOffset = int((src.shape[1] - 2)  / 2)
    #Collecting the pixel channels containing RGB values
    xyValueBlurredImg = src_blurred[yOffset][xOffset]
    src = padImage(src)
    xyAvrageSrcImg = (src[yOffset:1+yOffset,xOffset:1+xOffset,:]     + src[1+yOffset:2+yOffset,xOffset:1+xOffset,:] +
                      src[2+yOffset:3+yOffset,xOffset:1+xOffset,:]   + src[yOffset:1+yOffset,1+xOffset:2+xOffset,:] +
                      src[1+yOffset:2+yOffset,1+xOffset:2+xOffset,:] + src[2+yOffset:3+yOffset,1+xOffset:2+xOffset,:] +
                      src[yOffset:1+yOffset,2+xOffset:3+xOffset,:]   + src[1+yOffset:2+yOffset,2+xOffset:3+xOffset,:] +
                      src[2+yOffset:3+yOffset,2+xOffset:3+xOffset,:]) / 9
    xyAvrageSrcImg = xyAvrageSrcImg[0][0] #removing 2 dimensions from the array

    assert np.array_equal(xyValueBlurredImg,xyAvrageSrcImg) == True


test_fromFile_imageX_equals_ImageY_1()
#test_fromFile_imageX_equals_ImageY_2()
test_maxvalue_before_and_after_blur()
test_fromFile_avrageSrcPixelXY_equals_dstPixelXY()
test_blur_image_function_in_package()