#!/usr/bin/env python3
import time
import cv2
import sys
sys.path.append('../')  # Necessary to find the imageblurring package
from imageblurring.imagefunctions import writeImageToFile, \
    readImageFromFile, vectorizedFaceBlur


def detectFaces(image, cascadeFile="haarcascade_frontalface_default.xml"):
    """This function uses the cv2 module to detect faces in a image(picture),
    and prints out how many faces that are found in the image.

    The format for a parameter is:
    image (ndarray):
        A image represented in a ndarray. 3-dimensional ndarray.
    cascadeFile (String):
        A string representing the xml for parameters for face recognition.
    Returns:
        A list of all detected faces with their pixel y,x and height(h),
        width (w).
    """
    image = image.astype("uint8")
    faceCascade = cv2.CascadeClassifier(cascadeFile)
    faces = faceCascade.detectMultiScale(image,
                                         scaleFactor=1.025,
                                         minNeighbors=5,
                                         minSize=(30, 30)
                                         )

    print("Found {} faces !".format(len(faces)))
    return faces


def main(inFile="beatles.jpg", outFile="blurred_images\\blurred_faces.jpg",
         cascade="haarcascade_frontalface_default.xml"):
    """The function takes in three arguments, reads a picture from file,
    detects faces in the picture, and blurs only the faces until they are
    no longer detected in the picture. The function is using the numpy
    vectorized blur algorithm, and writes the image to a file when done.
    The function also tracks runtime for the whole process. A parameter
    xml file is required to detect faceses.

    The format for a parameter is:
    inimg (String):
        Filename, and filepath for the picture that is to be read.
    outimg (String):
        Filename, and filepath for the picture that is to be saved
        to a file.
    cascade (String):
        filname for xml file required to detect faces.
    Raises:
        RuntimeError exception if arguments are of the wrong type
    """
    image = readImageFromFile(inFile)
    image = image.astype("uint8")
    faces = detectFaces(image, cascade)
    startTime = time.time()
    while(len(faces) > 0):
        print("Blurring faces in picture......")
        for (x, y, w, h) in faces:
            yStart = y
            yStop = y + h
            xStart = x
            xStop = x + w
            image = vectorizedFaceBlur(image, xStart, xStop, yStart, yStop)
            # cv2.rectangle(image , (x, y) , (x + w, y + h) , (0,255 , 0) , 2)
        print("Detecting faces in picture.....")
        faces = detectFaces(image, cascade)
    print("All faces are blurred and the faces are no longer recognizable")
    print("Runtime numpy vectorized blur:",
          time.time() - startTime,
          " seconds")
    writeImageToFile(image, outFile)


if __name__ == '__main__':
    if (len(sys.argv) > 3):
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    elif (len(sys.argv) == 2):
        isWindows = sys.platform.startswith('win')
        winFilename = "blurred_images\\blurred_faces.jpg"
        linuxFilename = "blurred_images/blurred_faces.jpg"
        cascade = "haarcascade_frontalface_default.xml"
        outfile = winFilename if isWindows else linuxFilename
        main(sys.argv[1], outfile, cascade)
    else:
        raise RuntimeError("Wrong input argument. See README.md for help")
