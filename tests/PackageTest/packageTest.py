#!/usr/bin/env python3
from imageblurring.blur_1 import main as blur1
from imageblurring.blur_2 import main as blur2
from imageblurring.blur_3 import main as blur3
from imageblurring.blur_4 import main as blur4
from imageblurring.blur_faces import main as bf
from imageblurring.imagefunctions import blur_image


inFile = "beatles.jpg"
cascadeFile="haarcascade_frontalface_default.xml"
blur1(inFile, "blur1_test_image.jpg", 1)
blur2(inFile, "blur2_test_image.jpg", 15)
blur3(inFile, "blur3_test_image.jpg", 20, False)
blur4(inFile, "blur4_test_image.jpg", 20, False)
blur_image(inFile, "blur_image_test_image.jpg")
bf(inFile, "blur_faces_test_image.jpg", cascadeFile)

