#!/usr/bin/env python3
import time
import sys
sys.path.append('../')  # Necessary to find the imageblurring package
from imageblurring.imagefunctions import readImageFromFile, \
    writeImageToFile, vectorizedBlur


def main(inimg="beatles.jpg",
         outimg="blurred_images\\vectorized_blur_numpy.jpg",
         blurCycles=1):
    """The function takes in three arguments, reads a picture from file,
    blurs the image based on the vectorized blur algorithm, and writes
    the image to a file. The function also tracks runtime for the
    algorithm that blurs the image.

    The format for a parameter is:
    inimg (String):
        Filename, and filepath for the picture that is to be read.
    outimg (String):
        Filename, and filepath for the picture that is to be saved
        to a file.
    blurCycles (int):
        integer that specifies how many cycles of blur that is to
        be applied to the same image.
    Raises:
        RuntimeError exception if arguments are of the wrong type
    """
    image = readImageFromFile(inimg)
    startTime = time.time()
    for i in range(blurCycles):
        image = vectorizedBlur(image)
    print("Runtime numpy vectorized blur:",
          time.time() - startTime, "seconds")
    writeImageToFile(image, outimg)


if __name__ == '__main__':
    if (len(sys.argv) > 3):
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif (len(sys.argv) == 3):
        main(sys.argv[1], sys.argv[2], 1)
    elif (len(sys.argv) == 2):
        isWindows = sys.platform.startswith('win')
        winFilename = "blurred_images\\blur_numpy.jpg"
        linuxFilename = "blurred_images/blur_numpy.jpg"
        outfile = winFilename if isWindows else linuxFilename
        main(sys.argv[1], outfile, 1)
    else:
        raise RuntimeError("Wrong input argument. See README.md for help")
