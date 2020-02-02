#!/usr/bin/env python3
import time
import sys
sys.path.append('../')  # Necessary to find the imageblurring package
from imageblurring.imagefunctions import readImageFromFile, \
    writeImageToFile, vectorizedBlurNumba, unvectorizedBlurNumba, padImage


def main(inimg="beatles.jpg",
         outimg="blurred_images\\blur_numba.jpg",
         blurCycles=1,
         vectorized=False):
    """The function is using a numba (jit) decorated function to
    blur a picture. It takes in 4 arguments, reads a picture from
    file and blurs the image using the either the vectorized or
    none vectorized blur algorithm, and writes the image to a file.
    The function also tracks runtime for the algorithm that blurs
    the image.

    The format for a parameter is:
    inimg (String):
        Filename, and filepath for the picture that is to be read.
    outimg (String):
        Filename, and filepath for the picture that is to be saved
        to a file.
    blurCycles (int):
        integer that specifies how many cycles of blur that is to
        be applied to the same image.
    vectorized (bool):
        boolean that specifies which algorithm, vectorized (True)
        or none vectorized (False)
    Raises:
        RuntimeError exception if arguments are of the wrong type
    """
    image = readImageFromFile(inimg)
    image = image.astype("uint32")
    startTime = time.time()
    for i in range(blurCycles):
        if(vectorized):
            image = vectorizedBlurNumba(padImage(image))
        else:
            image = unvectorizedBlurNumba(padImage(image))

    vectOrNot = "vectorized" if vectorized else "unvectorized"
    print("Runtime Numba", vectOrNot, "blur:",
          time.time() - startTime, "seconds")
    writeImageToFile(image, outimg)


if __name__ == '__main__':
    if (len(sys.argv) > 4):
        vectorized = False
        if((sys.argv[4] == 'True') or (sys.argv[4] == 'true')):
            vectorized = True
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]), vectorized)
    elif (len(sys.argv) == 4):
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif (len(sys.argv) == 3):
        main(sys.argv[1], sys.argv[2], 1)
    elif (len(sys.argv) == 2):
        isWindows = sys.platform.startswith('win')
        winFilename = "blurred_images\\blur_numba.jpg"
        linuxFilename = "blurred_images/blur_numba.jpg"
        outfile = winFilename if isWindows else linuxFilename
        main(sys.argv[1], outfile, 1)
    else:
        raise RuntimeError("Wrong input argument. See README.md for help")
