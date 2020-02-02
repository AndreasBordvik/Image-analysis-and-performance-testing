#!/usr/bin/env python3
import argparse
import sys
sys.path.append('../')  # Necessary to find the imageblurring package
from imageblurring.blur_1 import main as blur1
from imageblurring.blur_2 import main as blur2
from imageblurring.blur_3 import main as blur3
from imageblurring.blur_4 import main as blur4


def main():
    """This method adds command line user interface for the script
    using ArgumentParser from the library argparse. This file can be
    executed directly, or it can be imported via the installed
    imageblurring package with e.g from imageblurring.blur import main as blur.
    Blur() must than be called to execute this method.
    Instructions for the input arguments are provided by calling
    the script with with a --help or -h flag. The interface makes
    it possible to specify the input and output image filename.
    It also makes it possible to switch between 3 implementations
    as required/specified by the assignment 4.5 text.
    """
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-uvp", "--uvpython",
                           help="Unvectorized blur using standard python loops",
                           action="store_true")
    argparser.add_argument("-vnp", "--vnumpy",
                           help="Vectorized blur using numpy",
                           action="store_true")
    argparser.add_argument("-vnb", "--vnumba",
                           help="Vectorized blur using numba",
                           action="store_true")
    argparser.add_argument("-uvnb", "--uvnumba",
                           help="Unvectorized blur using numba",
                           action="store_true")
    argparser.add_argument("-vc", "--vcython",
                           help="Vectorized blur using cython",
                           action="store_true")
    argparser.add_argument("-uvc", "--uvcython",
                           help="Unvectorized blur using cython",
                           action="store_true")
    argparser.add_argument('infile', type=str, help='Input filename')
    argparser.add_argument('outfile', type=str, help='output filename')
    argparser.add_argument('N', type=int, help='number of blur cycles')

    args = argparser.parse_args()
    inputfile = args.infile
    outputfile = args.outfile
    blurcycles = args.N
    if (args.uvpython):
        print("Unvectorized blur using standard python loops choosen")
        blur1(inputfile, outputfile, blurcycles)
    if(args.vnumpy):
        print("Vectorized blur using numpy is choosen")
        blur2(inputfile, outputfile, blurcycles)
    if (args.vnumba):
        print("Vectorized blur using numba is choosen")
        blur3(inputfile, outputfile, blurcycles, True)
    if (args.uvnumba):
        print("Unvectorized blur using numba is choosen")
        blur3(inputfile, outputfile, blurcycles, False)
    if (args.vcython):
        print("Vectorized blur using cython is choosen")
        blur4(inputfile, outputfile, blurcycles, True)
    if (args.uvcython):
        print("Unvectorized blur using cython is choosen")
        blur4(inputfile, outputfile, blurcycles, False)
    if(not args.uvpython and not args.vnumpy and not args.vnumba
            and not args.uvnumba and not args.vcython and not args.uvcython):
        print("No blurtype i choosen, using vectorized numpy as default:")
        blur2(inputfile, outputfile, blurcycles)


if __name__ == '__main__':
    main()
