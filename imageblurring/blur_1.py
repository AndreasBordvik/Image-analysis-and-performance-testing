#!/usr/bin/env python3
import time
import sys
sys.path.append('../')  # Necessary to find the imagefunction module
from imageblurring.imagefunctions import readImageFromFile, \
        writeImageToFile, unvectorizedBlur


def main(inimg="beatles.jpg",
         outimg="blurred_images\\unvectorized_blur_standardPython.jpg",
         blurCycles=1):
    """The function takes in three arguments, reads a picture from file,
        blurs the image based on the nonevectorized blur algorithm, and
        writes the image to a file. The function also tracks runtime for
        the algorithm that blurs the image.

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
        image = unvectorizedBlur(image)
    print("Runtime standard python unvectorized blur:",
          time.time() - startTime, "seconds")
    writeImageToFile(image, outimg)


if __name__ == '__main__':
    if (len(sys.argv) > 3):
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif (len(sys.argv) == 3):
        main(sys.argv[1], sys.argv[2], 1)
    elif (len(sys.argv) == 2):
        isWindows = sys.platform.startswith('win')
        winFilename = "blurred_images\\unvectorized_blur_standardPython.jpg"
        linuxFilename = "blurred_images/unvectorized_blur_standardPython.jpg"
        outfile = winFilename if isWindows else linuxFilename
        main(sys.argv[1], outfile, 1)
    else:
        raise RuntimeError("Wrong input argument. See README.md for help")
